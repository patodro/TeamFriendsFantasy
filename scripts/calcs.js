function PickComp() {
	var roster = document.getElementsByClassName("playerCard");
	var draft;
	var drRound;
	var keep;
	var comp;
	var stt; 
	
	for (var i=0, play; play = roster[i]; i++) {
		draft = play.getElementsByClassName("draftInfo")[0];
		if (draft.children[0].children[1].innerText === "--") {
			drRound = 14;
		} else {
			drRound = Number(draft.children[0].children[1].innerText);
		}
		
		if (draft.children[1].children[1].innerText) {
			keep = Number(draft.children[1].children[1].innerText);
		} else {
			keep = 0;
			draft.children[1].children[1].insertAdjacentText("beforeend", 0);
		}
		
		
		let stt = keep + 1;
		let comp = drRound - stt;
		
		draft.children[2].children[1].insertAdjacentHTML("beforeend", comp);
		
		draftExclusion(play, comp);
		
	}
}

function draftExclusion (player, comp) {
	if (comp <= 2) {
		player.parentNode.className = "DRexcl";
	}
}

function buildRoster() {
	var name = document.querySelector("#json-lookup").dataset.jsonName;
	var request = new XMLHttpRequest();
	request.open("GET", `${name}.json`, false);
	request.send(null);
  var roster = JSON.parse(request.responseText);
  document.getElementsByClassName("playerCard")[0].children[1].innerText = roster.roster[0].firstName;
}