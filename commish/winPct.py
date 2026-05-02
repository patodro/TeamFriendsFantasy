import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

# Read the CSV file
df = pd.read_csv('dataStore/winpct.csv')

# Filter for years 2011 to present (2025)
df_filtered = df[df['Year'] >= 2011].copy()

# Get player columns (all except Gm and Year)
player_cols = [col for col in df.columns if col not in ['Gm', 'Year']]

# Ignore managers who did not have a team in the most recent season
latest_year = df_filtered['Year'].max()
active_players = [col for col in player_cols if pd.notna(df_filtered.loc[df_filtered['Year'] == latest_year, col].iloc[0]) and df_filtered.loc[df_filtered['Year'] == latest_year, col].iloc[0] != '']

# Calculate win percentage for each player-year combination
# Win % = Games Won / Total Games Played
plot_data = []

for year in sorted(df_filtered['Year'].unique()):
    year_row = df_filtered[df_filtered['Year'] == year].iloc[0]
    total_games = year_row['Gm']
    
    for player in active_players:
        wins = year_row[player]
        if pd.notna(wins) and wins != '':
            win_pct = float(wins) / float(total_games)
            plot_data.append({
                'Year': year,
                'Player': player,
                'WinPct': round(win_pct, 3),
                'Wins': int(wins),
                'Games': int(total_games)
            })

# Create DataFrame for plotting
plot_df = pd.DataFrame(plot_data)

# Create interactive line chart
fig = px.line(
    plot_df, 
    x='Year', 
    y='WinPct', 
    color='Player',
    markers=True,
    title='Win Pct by Season',
    labels={'WinPct': 'Win %', 'Year': 'Season'},
    hover_data=['Wins', 'Games']
)

# Update layout for better readability
fig.update_layout(
    height=600,
    hovermode='x unified',
    legend_title='Manager',
    xaxis=dict(tickmode='linear', tick0=2011, dtick=1),
    yaxis=dict(range=[0, 1], tickformat='.0%'),
    template='plotly_dark'
)

# Add horizontal line at 0.500 for reference
fig.add_hline(y=0.5, line_dash="dash", line_color="gray", annotation_text=".500")

# Save to HTML file
output_file = 'dataStore/activeWinPct.html'
plot(fig, filename=output_file)#, auto_open=True)

print(f"Chart saved to: {output_file}")
print(f"Total data points: {len(plot_df)}")
print(f"Players tracked: {plot_df['Player'].nunique()}")