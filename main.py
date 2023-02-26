from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from game import Player, Game, Cell, get_wins
from queue import Queue


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


MARKS = Queue()
WINS = get_wins()
PLAYERS = {}
DIM = 3
GAMES = []
CONNECTIONS = []


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})


@app.post("/")
async def root_post(request: Request):
    res = await request.json()
    id_ = int(res["id"])

    if MARKS.empty:
        for mark in ["x", "o"]:
            MARKS.put(mark)

    PLAYERS[id_] = Player(id_, mark=MARKS.get())
    print(PLAYERS)
    if len(PLAYERS) == 2:
        GAMES.append(
            Game(
                wins=WINS,
                cell=Cell,
                dim=DIM,
                players=[player for player in PLAYERS.values()],
            )
        )

    return RedirectResponse(f"/game/{id_}")


@app.get("/game/{player_id}", response_class=HTMLResponse)
async def read_player(player_id: int, request: Request):
    if player_id in PLAYERS:
        return templates.TemplateResponse("game.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    CONNECTIONS.append(websocket)
    while True:
        data = await websocket.receive_json()

        g = GAMES[0]
        player = PLAYERS[int(data["player"])]
        cell_id = int(data["cell"])
        flag, comb = g.game_turn(player, cell_id)

        if flag:
            data["comb"] = comb
            data["mark"] = player.get_mark()
            for sock in CONNECTIONS:
                await sock.send_json(data)

        if g.win:
            break
