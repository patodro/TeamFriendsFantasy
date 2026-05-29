import os
import json
import paramiko
from pathlib import Path
from datetime import datetime

# --- CONFIGURATION ---
LOCAL_DIR = Path(__file__).resolve().parent
REMOTE_DIR = "/var/www/html"  # Adjust to your server path
SERVER_HOST = "landmine"
SERVER_PORT = 22
USERNAME = "patodro"
PASSWORD = "fireball"
SSH_KEY_PATH = Path.home() / ".ssh" / "id_rsa" 

def connect_sftp():
    """Establish SFTP connection."""
    transport = paramiko.Transport((SERVER_HOST, SERVER_PORT))
    
    try:
        if SSH_KEY_PATH.exists():
            key = paramiko.RSAKey.from_private_key_file(str(SSH_KEY_PATH))
            transport.connect(username=USERNAME, pkey=key)
        else:
            # Fallback to env var for password
            transport.connect(username=USERNAME, password=PASSWORD)
            
        return paramiko.SFTPClient.from_transport(transport)
    except Exception as e:
        print(f"Connection failed: {e}")
        raise

def get_remote_file_list(sftp, remote_base_dir):
    """
    Recursively walk the remote directory and return a dict:
    { '/absolute/remote/path': {'mtime': float, 'size': int} }
    """
    remote_files = {}
    
    def walk_remote(dir_path):
        try:
            entries = sftp.listdir_attr(dir_path)
        except FileNotFoundError:
            return

        for entry in entries:
            full_path = f"{dir_path}/{entry.filename}"
            
            # Skip . and ..
            if entry.filename in ('.', '..'):
                continue
            
            # If it's a directory, recurse
            if entry.st_mode & 0o40000: # S_IFDIR
                walk_remote(full_path)
            else:
                # Store mtime and size
                remote_files[full_path] = {
                    'mtime': entry.st_mtime,
                    'size': entry.st_size
                }
    
    walk_remote(remote_base_dir)
    return remote_files

def needs_update(local_path, remote_info):
    """
    Determine if local file needs to be uploaded.
    Returns True if:
    1. Remote file doesn't exist.
    2. Local file is newer (higher mtime).
    3. Sizes differ (safety check for corruption).
    """
    if not remote_info:
        return True # New file
    
    local_stat = local_path.stat()
    local_mtime = int(local_stat.st_mtime)
    local_size = local_stat.st_size
    
    remote_mtime = int(remote_info['mtime'])
    remote_size = remote_info['size']
    
    # Check if local is strictly newer
    if local_mtime > remote_mtime:
        return True
    
    # Safety check: if mtime is close but sizes differ, force update
    # (Sometimes clock skew causes mtime issues)
    if abs(local_mtime - remote_mtime) < 1 and local_size != remote_size:
        return True
        
    return False

def upload_file(sftp, local_path, remote_path):
    """Upload a file to the given remote path, creating directories as needed."""
    try:
        # Ensure remote directory exists
        remote_dir = "/".join(remote_path.split("/")[:-1])
        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            # Create directory recursively (paramiko mkdir is not recursive)
            create_remote_dirs(sftp, remote_dir, REMOTE_DIR)
            
        sftp.put(str(local_path), remote_path)
        print(f"✓ Uploaded: {local_path.name} -> {remote_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to upload {local_path}: {e}")
        return False

def create_remote_dirs(sftp, target_dir, base_dir):
    """Helper to create nested directories on remote server."""
    # Split path into parts relative to base
    try:
        rel_parts = Path(target_dir).relative_to(base_dir).parts
    except ValueError:
        # If target is not under base, just try to create it
        rel_parts = Path(target_dir).parts

    current_path = base_dir
    for part in rel_parts:
        current_path = f"{current_path}/{part}"
        try:
            sftp.stat(current_path)
        except FileNotFoundError:
            sftp.mkdir(current_path)

def main():
    print("Connecting to server...")
    sftp = connect_sftp()
    
    try:
        # 1. Get current state of remote server
        print(f"Scanning remote directory: {REMOTE_DIR}...")
        remote_files = get_remote_file_list(sftp, REMOTE_DIR)
        print(f"Found {len(remote_files)} files on server.")
        
        # 2. Scan local directory
        files_to_sync = []
        for root, dirs, files in os.walk(LOCAL_DIR):
            # Skip compiled Python cache directories entirely
            if Path(root).name == "__pycache__":
                continue

            for file in files:
                if file.startswith('.'): continue
                
                local_path = Path(root) / file
                
                # Calculate corresponding remote path
                relative_path = local_path.relative_to(LOCAL_DIR)
                if LOCAL_DIR.stem == "TeamFriendsFantasy":
                    remote_path = f"{REMOTE_DIR}/{'/'.join(relative_path.parts)}"
                else:
                    remote_path = f"{REMOTE_DIR}/{LOCAL_DIR.stem}/{'/'.join(relative_path.parts)}"
                
                # Check if update is needed
                if needs_update(local_path, remote_files.get(remote_path)):
                    files_to_sync.append((local_path, remote_path))
        
        if not files_to_sync:
            print("Server is already up to date with local Desktop.")
            return

        print(f"\n{len(files_to_sync)} file(s) need updating.")
        
        # 3. Perform uploads
        success_count = 0
        for local_path, remote_path in files_to_sync:
            if upload_file(sftp, local_path, remote_path):
                success_count += 1
        
        print(f"\nSync complete. {success_count} files transferred.")
        
    except Exception as e:
        print(f"Error during sync: {e}")
    finally:
        sftp.close()

if __name__ == "__main__":
    main()