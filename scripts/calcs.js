function popRoster() {
	var emptyRos = document.querySelector('ul[alt="roster"]');
	emptyRos.insertAdjacentHTML("beforeend", '\n\t\t<li class="">\n\t\t\t<div class="playerCard">\n\t\t\t\t<div class="playInfo">\n\t\t\t\t\t<div class="position"></div>\n\t\t\t\t\t<div class="team"></div>\n\t\t\t\t</div>\n\t\t\t\t<div class="player"></div>\n\t\t\t\t<div class="draftInfo">\n\t\t\t\t\t<div class="picks"><span>Draft Round</span><span></span></div>\n\t\t\t\t\t<div class="picks"><span>Keeper Status</span><span></span></div>\n\t\t\t\t\t<div class="picks"><span>Pick Comp</span><span></span></div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</li>');
}

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
			if (draft.children[1].children[1].innerText.includes("y")) {
				play.parentNode.className = "KEEP";
				draft.children[1].children[1].innerText = draft.children[1].children[1].innerText.replace('y','');;
			} 
			keep = Number(draft.children[1].children[1].innerText);
		} else {
			keep = 0;
			draft.children[1].children[1].insertAdjacentText("beforeend", 0);
		}
	if (keep > 0) {
		draft.children[1].style.color = "gold";
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

function faExclusion (addDate) {
	let cutDate = new Date("11/18/23");
	let FADate = new Date(addDate);
	if (FADate >= cutDate)
	{
		return 1;
	} else {
		return 0;
	}
}

function buildRoster() {
	var FAexcl;
	var name = document.querySelector("#json-lookup").dataset.jsonName;
	var request = new XMLHttpRequest();
	request.open("GET", `${name}.json`, false);
	request.send(null);
	var roster = JSON.parse(request.responseText);
	for (let n = 0; n < roster.roster.length; n++) {
		popRoster();
	}
	var card = document.getElementsByClassName("playerCard");
	var emptyRos = document.querySelector('ul[alt="roster"]');
	for (var p=0, play; play = roster.roster[p]; p++) {
		card[p].children[1].innerText = roster.roster[p].firstName + " " + roster.roster[p].lastName;
		card[p].children[0].children[0].innerText = roster.roster[p].position
		card[p].children[0].children[1].innerText = roster.roster[p].team
		card[p].children[2].children[0].children[1].innerText = roster.roster[p].draftInfo.draftRound;
		card[p].children[2].children[1].children[1].innerText = roster.roster[p].draftInfo.keep;
		FAexcl = faExclusion(roster.roster[p].addDate)
		if (FAexcl)	{
			card[p].parentNode.className = "FAexcl";
		}
	}
}

