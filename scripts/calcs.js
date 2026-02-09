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

function faExclusion(year, addDate) {
  // -------------------------------------------------
  // 1️⃣ Resolve the year (default = current year)
  // -------------------------------------------------
  const targetYear =
    typeof year === "number" ? year : new Date().getFullYear();

  // -------------------------------------------------
  // 2️⃣ Map of known cutoff dates (ISO‑8601 format)
  // -------------------------------------------------
  const cutoffMap = {
    2025: "2025-11-22",
    2024: "2024-11-16",
    2023: "2023-11-18",
    2022: "2022-11-19",
    2021: "2021-11-20"
  };

  // -------------------------------------------------
  // 3️⃣ Pick the appropriate cutoff, falling back to 2025‑11‑22
  // -------------------------------------------------
  const isoCutoff = cutoffMap[targetYear] ?? "2025-11-22";
  const cutDate = new Date(isoCutoff); // guaranteed valid ISO string

  // -------------------------------------------------
  // 4️⃣ Convert the incoming date to a Date object
  // -------------------------------------------------
  const FADate = addDate instanceof Date ? addDate : new Date(addDate);

  // Defensive guard: if parsing failed, treat as “not eligible”
  if (Number.isNaN(FADate.getTime())) {
    console.warn("faExclusion: invalid addDate supplied");
    return 0;
  }

  // -------------------------------------------------
  // 5️⃣ Comparison – return 1 if on/after cutoff, else 0
  // -------------------------------------------------
  return FADate >= cutDate ? 1 : 0;
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

function buildDraft(year) {
	var pick;
	var player;
	var pos;
	var team;
	var owner;
	var keep;
	var request = new XMLHttpRequest();
	request.open("GET", `${year}draft.json`, false);
	request.send(null)
	var draft = JSON.parse(request.responseText);
	for (let i=0; i < draft.draft.length; i++) {
		pick = draft.draft[i].round +"."+ draft.draft[i].pick;
		player = draft.draft[i].player.name;
		pos = draft.draft[i].player.pos;
		team = draft.draft[i].player.team;
		keep = draft.draft[i].player.keep;
		owner = draft.draft[i].owner
		dbpk = document.querySelector('th[pk="'+pick+'"]')
		if (keep > 0) {
			dbpk.id = "keep";
		} else {
			dbpk.id = pos;
		}
		dbpk.insertAdjacentHTML("beforeend",'<div class="playerCard"><div class="playerInfo"><div class="position"></div><div class="team"></div></div>\n\t\t\t\t\t\t<div class="player"></div></div>');
		card = dbpk.getElementsByClassName("playerCard")[0];
		card.getElementsByClassName("player")[0].insertAdjacentText("beforeend",player);
		card.getElementsByClassName("playerInfo")[0].children[0].insertAdjacentText("beforeend",pos);
		card.getElementsByClassName("playerInfo")[0].children[1].insertAdjacentText("beforeend",team);
		if (owner != dbpk.closest('table').firstElementChild.children[0].children[dbpk.cellIndex].innerText) {
			card.insertAdjacentHTML("afterbegin",'<div class="pickTrade">*-></div>');
			card.getElementsByClassName("pickTrade")[0].insertAdjacentText("beforeend",owner+"*")
		}
	}
}

function buildWikiDraft(year) {
	var pick;
	var player;
	var pos;
	var team;
	var owner;
	var keep;
	var request = new XMLHttpRequest();
	request.open("GET", `${year}draft.json`, false);
	request.send(null)
	var draft = JSON.parse(request.responseText);
	for (let i=0; i < draft.draft.length; i++) {
		pick = draft.draft[i].round +"."+ draft.draft[i].pick;
		player = draft.draft[i].player.name;
		pos = draft.draft[i].player.pos;
		team = draft.draft[i].player.team;
		keep = draft.draft[i].player.keep;
		owner = draft.draft[i].owner;
		row = document.getElementById(pick)
        if (keep != 0) {
            row.className = "keep";
        }
		row.cells.namedItem("player").innerText = player
        row.cells.namedItem("player").className = pos
		row.cells.namedItem("team").innerText = team
		row.cells.namedItem("pos").innerText = pos
        row.cells.namedItem("pos").className = pos
        row.cells.namedItem("owner").innerText = owner
	}
}

function buildWikiRoster(year=null) {
	var FAexcl;
    var drRound;
    var keep;
    var stt;
    var cmp;
	var name = document.querySelector("#json-lookup").dataset.jsonName;
    var emptyRos = document.getElementById('tblRoster').getElementsByTagName('tbody')[0];
	var request = new XMLHttpRequest();
	request.open("GET", `${name}.json`, false);
	request.send(null);
	var roster = JSON.parse(request.responseText);
	for (let n = 0; n < roster.roster.length; n++) {
		// Insert row at end of tbody
        var newRow = emptyRos.insertRow(-1)
        
        // Build cells in the newRow
        var pos = newRow.insertCell(0);
        var play = newRow.insertCell(1);
        var team = newRow.insertCell(2);
        var rd = newRow.insertCell(3);
        var add = newRow.insertCell(4);
        var kp = newRow.insertCell(5);
        var comp = newRow.insertCell(6);
        
        // Populate row with player info from JSON db file
        pos.textContent = roster.roster[n].position;
        play.textContent = roster.roster[n].firstName + " " + roster.roster[n].lastName;
        team.textContent = roster.roster[n].team;
        rd.textContent = roster.roster[n].draftInfo.draftRound;
        add.textContent = roster.roster[n].addDate;
        kp.textContent = roster.roster[n].draftInfo.keep;
        
        // Check if player has FA Exclusion
        FAexcl = faExclusion(year, roster.roster[n].addDate)
        if (FAexcl)	{
			newRow.className = "FAexcl";
		}
        
        //FA add equivalence
        if (rd.textContent === "--") {
			drRound = 14;
		} else {
			drRound = Number(rd.textContent);
		}
        
        // Keeper with 'y' present indicates an active keeper selection
        if (kp.textContent) {
			if (kp.textContent.includes("y")) {
				newRow.className = "KEEP";
				kp.textContent = kp.textContent.replace('y','');;
			} 
			keep = Number(kp.textContent);
		} else {
			keep = 0;
		}
        
        if (keep > 0) {
            kp.style.color = "gold";
        }
		
		let stt = keep + 1;
        let cmp = drRound - stt;
		
		comp.textContent = cmp;
		if (cmp <= 2) {
            newRow.className = "DRexcl";
        }
	}
}

function draftBorder() {
    document.addEventListener('DOMContentLoaded', () => {
        const table = document.querySelector('.draft-table');
        const interval = parseInt(getComputedStyle(table).getPropertyValue('--interval'), 10) || 3;
        
        //Loop over all rows and add the class where needed
        table.querySelectorAll('tr').forEach((row, index) => {
            //index is zero-based; +1 makes it human-friendly -1 to account for header
            if ((index) % interval === 0) {
                row.classList.add('border-row');
            }
        });
    });
}
function findHighest(data) {
	if (!data.length) return null; // Handle empty array case
	//Reduce keeps the entry with the larger score each iteration
	return data.reduce((max, item) => (item.score > max.score ? item : max));
}
function hiScore(season) {
	const table = document.getElementById('hiScores');
	if (!table) return; // Exit if table not found

	if (season.length === 0) {
		table.textContent = "No scores available.";
		return;
	}

	var request = new XMLHttpRequest();
	request.open("GET", `dataStore/${season}scores.json`, false);
	request.send(null);
	var scores = JSON.parse(request.responseText);

	//Loop thru scores and populate table rows
	scores.forEach(week => {
		var rowID = `hi${week.week}`;
		hiRow = document.getElementById(rowID);
		hiRow.innerHTML = "<b>Week "+week.week+": </b>"+week.team+" - "+week.score;
	})
	best = findHighest(scores);
	var bestID = `hi${best.week}`;
	bestRow = document.getElementById(bestID);
	bestRow.style.color = "gold";
}