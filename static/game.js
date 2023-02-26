let url = "ws://127.0.0.1:8000/ws";
let socket = new WebSocket(url);

socket.addEventListener('message', (event) => {
    data = JSON.parse(event.data);
    console.log(data);
    cell_id = parseInt(data.cell);
    mark = data.mark;
    comb = data.comb;
    cell = document.getElementById(cell_id);
    cell.innerText = mark;
    setColor(cellIds=comb);
});

function cellEvent(event, mark="o") {
    id = this.id;
    cell = document.getElementById(id);
    if (!cell.innerText) {
        plyer_id = document.URL.split("/").slice(-1)[0];
        socket.send(JSON.stringify(
            {
                "cell": id,
                "player": plyer_id
            }
        ));
    }
}

function setColor(cellIds, color="red") {
    if (cellIds) {
        cellIds.forEach(element => {
            cell = document.getElementById(element);
            cell.style.backgroundColor = color
        });
    }
}

function createCells(container, dim) {
    let counter = 1

    for (let i = 0; i < dim; i++) {
        let row = document.createElement("div");
        row.className = "row";

        for (let j = 0; j < dim; j++) {
            let cell = document.createElement("div");
            cell.className = "cell";
            cell.id = counter;
            cell.onclick = cellEvent;
            
            row.appendChild(cell);
            counter += 1;
        }
        container.appendChild(row);
    }
}


window.onload = function() {
    let gameDiv = document.getElementsByClassName("game");

    let container = document.createElement("div");
    container.className = "container"

    let retry = document.createElement("div");
    retry.className = "retry"
    retry.innerText = "RETRY"
    
    createCells(container=container, dim=3)
    
    gameDiv[0].appendChild(container);
    gameDiv[0].appendChild(retry);
    // sendMessage();
    // setColor([1, 2, 3], color="#FFB6C1")

    console.log("Hi");
}