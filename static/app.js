let res = await fetch('/players');
const players = await res.json();
res = await fetch('/teams');
const teams = await res.json();

const svg = document.getElementById('graph');
const title = document.getElementById('titling');
const button = document.getElementById('compute');
const cont = document.getElementById('container');
let nodes = [];
let playerA = null;
let playerB = null;
let time = 0;

class PlayerNode {
    constructor(name, id, x, y) {
        this.name = name;
        this.id = id;

        this.baseX = x;
        this.baseY = y;

        this.x = x;
        this.y = y;

        this.phase = Math.random()*Math.PI*2;
        this.radius = 40;
    };

    update(t) {
        const float = 8;
        this.x = this.baseX + Math.sin(t + this.phase) * float;
        this.y = this.baseY + Math.cos(t + this.phase) * float;
    };
};

// -------------- fetching specific data --------------
function getHeadshot(playerId) {
    return `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`;
}

function getTeamLogo(teamId, season) {
    const temp = teams[teamId]
    console.log(`temp = ${temp}`)
    const match = temp.find(s => parseInt(season.substring(0, 4)) >= parseInt(s[0]));
    // return match[2];
    console.log(match)
    if (match) {
        return match[2]; // found something
    } else {
        return temp[temp.length - 1][2]; // otherwise fall back to older one
    }
}

function getTeamName(teamId, season) {
    const temp = teams[teamId]
    const match = temp.find(([s]) => parseInt(season.substring(0, 4)) >= parseInt(s));
    if (match) {
        return match[1]; // found something
    } else {
        return temp[temp.length - 1][1]; // otherwise fall back to older one
    }
}


// -------------- search boxes --------------
const fuseOptions = {
    keys: ["full_name"],
    threshold: 0.1
};

const fuse = new Fuse(players, fuseOptions);

function playerSearch(textboxId, resultsId) {
    const input = document.getElementById(textboxId);
    const container = document.getElementById(resultsId);
    
    input.addEventListener('input', (e) => {
        const query = e.target.value;
        
        checkBoxes(input.id, query);
        
        if (query == "") {
            container.innerHTML = "";
            return;
        }
        
        const result = fuse.search(query);
        showResults(result, input, container);
    });
}

function showResults(results, input, container) {
    container.innerHTML = "";
    
    results.slice(0,5).forEach((result, i) => {
        const div = document.createElement('div');
        div.setAttribute('class', 'dropdown_item');
        div.style.top = `${(i + 1) * 2}rem`; // 0.5 padding on both top + bottom -> 1 + the 1 rem automatically given
        // div.style.width = 'clamp(10rem, 13vw, 15rem)';
        div.textContent = result.item.full_name;
        
        div.addEventListener('click', () => {
            input.value = result.item.full_name;
            container.innerHTML = "";
            
            selectPlayer(input.id, result.item);
        });
        
        container.appendChild(div);
    });
}

function selectPlayer(input, player) {
    if (input == 'player_search_a') {
        if (playerB?.id == player.id) {
            document.getElementById('player_search_a').value = '';
            return
        }
        playerA = player;
        addNode(player, 'A');
    }
    
    if (input == 'player_search_b') {
        if (playerA?.id == player.id) {
            document.getElementById('player_search_b').value = '';
            return
        }
        playerB = player;
        addNode(player, 'B');
    }
}

function checkBoxes(input, text) {
    if (input == 'player_search_a' && playerA) {
        if (text != playerA.full_name) {
            removeNode(playerA.id);
            playerA = null;
        }
    }
    
    if (input == 'player_search_b' && playerB) {
        if (text != playerB.full_name) {
            removeNode(playerB.id);
            playerB = null;
        }
    }
}

playerSearch("player_search_a", "search_results_a");
playerSearch("player_search_b", "search_results_b");


// -------------- nodes + visuals -------------- 
// referenced https://codepen.io/Wryte/pen/eYNEJQ and https://codepen.io/neiltron/pen/EyadLp for the floating nodes (addNode + moveNodes), more specifically the calculations  

function addNode(player, side) {
    if (nodes.some(n => n.id == player.id)) {
        return;
    }
    
    fadeOut();
    
    let x;
    const rect = cont.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2.45;
    const offset = 180;
    
    if (side == 'A') {
        x = cx - offset;
    } else {
        x = cx + offset;
    }
    const y = cy;
    
    const node = new PlayerNode(player.full_name, player.id, x, y);
    node.side = side;
    const img = document.createElement('img');
    img.src = getHeadshot(player.id);
    img.style.backgroundColor = '#ffffff9b';
    img.className = 'floating_node';
    document.body.appendChild(img);
    
    node.el = img;
    nodes.push(node);
    
    // console.log(nodes);
}

function removeNode(playerId) {
    const node = nodes.find(node => node.id == playerId);
    
    if (node.el) {
        node.el.remove();
    }
    
    nodes = nodes.filter(node => node.id != playerId);
    
    if (nodes.length == 0) {
        fadeIn();
    }
    
    // console.log(nodes);
}

function renderGraph() {
    nodes.forEach(node => {
        const radius = node.radius;
        node.el.style.transform = `translate(${node.x - radius}px, ${node.y - radius}px)`;
    })
}

function moveNodes() {
    const titleRect = title.getBoundingClientRect();
    const contRect = cont.getBoundingClientRect();
    const cy = titleRect.top + titleRect.height / 2;
    const cx = contRect.left + contRect.width / 2;
    const offset = 150;
    
    nodes.forEach((node) => {
        if (node.side == 'A') {
            node.baseX = cx - offset;
        } else {
            node.baseX = cx + offset;
        }
        node.baseY = cy;
    })
}

function animate() {
    time += 0.02;
    
    moveNodes();
    nodes.forEach(node => node.update(time));
    renderGraph();
    requestAnimationFrame(animate);
}

function fadeIn() {
    title.classList.remove('fade_out');
}

function fadeOut() {
    title.classList.add('fade_out');
}

window.addEventListener('resize', () => {
    const rect = cont.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2.45;
    const offset = 180;
    
    nodes.forEach((node) => {
        if (node.size == 'A') {
            node.baseX = cx - offset;
        } else {
            node.baseX = cx + offset;
        }
        node.baseY = cy;
    })
})

animate();


// -------------- connection cards --------------
const cardContainer = document.getElementById('card_container');

button.addEventListener('click', async () => {
    // let start = document.getElementById('player_search_a')
    // console.log(playerA.id);
    // console.log(playerB.id);
    const traversal = document.forms.traversal_input.traversal.value;
    if (playerA == null || playerB == null)  {
        return
    }
    
    const res = await fetch(`/search?start=${playerA.id}&end=${playerB.id}&traversal=${traversal}`);
    const path = await res.json();
    
    console.log(path);
    
    displayPath(path);
})

function displayPath(path) {
    const playerIds = path.slice(0, -1).map(p => p[0]).concat(path[path.length - 1]);
    const edges = path.slice(0, -1).map(p => ({
        teamId: p[1],
        season: p[2]
    }));
    const degreeLabel = `${edges.length} degree(s) of separation.`
    let cards = degreeLabel;
    edges.forEach((edge, i) => {
        console.log(i)
        const id1 = playerIds[i];
        const id2 = playerIds[i + 1];
        console.log(id1);
        console.log(id2);
        
        const name1 = players.find(p => p.id == id1).full_name;
        const name2 = players.find(p => p.id == id2).full_name;
        
        const team = edge.teamId;
        const season = edge.season;
        console.log(`season asked for: ${season}`);
        console.log(typeof(edge.season));
        const teamImg = getTeamLogo(team, season);
        const teamName = getTeamName(team, season);
        
        cards += `
        <div class="path_card" style="animation-delay: ${i * 0.08}s">
        <div class="card_profile">
        <img class="card_pic" src="${getHeadshot(id1)}"/>
        <span class="card_profile_name">${name1}</span>
        </div>
        <div class="card_connection"><img class="card_pic" src="${teamImg}"/> <span class="connection_details">${teamName} (${season})</span></div>
        <div class="card_profile">
        <img class="card_pic" src="${getHeadshot(id2)}"/>
        <span class="card_profile_name">${name2}</span>
        </div>
        </div>
        `;
    });
    
    showCards(cards);
}

function showCards(html) {
    cardContainer.innerHTML = html;
}