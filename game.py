def get_wins(dim: int = 3):
    start, step = 1, 1
    rows = [range(0, dim, step), range(start, dim * dim, dim)]

    wins = [
        [i for i in range(start, dim * dim + start, dim + step)],
        [i for i in range(dim, dim * dim, dim - step)],
    ]

    for q in range(len(rows)):
        for w in range(len(rows)):
            if q != w:
                for i in rows[q]:
                    wins.append([j + i for j in rows[w]])
    return wins


class Player:
    def __init__(self, id_: int, mark: str):
        self.id = id_
        self.mark = mark

    def get_id(self):
        return self.id

    def get_mark(self):
        return self.mark

    def __eq__(self, other):
        return isinstance(other, Player) and self.get_id() == other.get_id()


class Cell:
    def __init__(self, mark: str):
        self.mark = mark

    def get_mark(self):
        return self.mark

    def set_mark(self, mark: str):
        self.mark = mark

    def __eq__(self, other):
        return isinstance(other, Cell) and self.get_mark() == other.get_mark()

    def __str__(self):
        return self.mark


class Game:
    def __init__(
        self,
        wins: list,
        cell: Cell,
        players: list[Player],
        dim: int = 3,
        mark: str = "-",
    ):
        self.start = 1
        self.cell = cell(mark)
        self.dim = dim
        self.current_player, self.other_player = players
        self.fields = {
            i + self.start: cell(mark=mark) for i in range(self.dim * self.dim)
        }
        self.wins = wins
        self.win_comb = []
        self.win = None

    def _set_field(self, key: int, mark: str):
        self.fields[key].set_mark(mark)

    def _swap_players(self):
        self.current_player, self.other_player = self.other_player, self.current_player

    def _wins_check(self, mark: str):
        for w in self.wins:
            if [str(self.fields[key]) for key in w].count(mark) == self.dim:
                return w
        return

    def game_turn(self, player: Player, cell: int):
        if player is self.current_player and self.fields[cell] == self.cell:
            mark = player.get_mark()
            self._set_field(cell, mark)
            self.win_comb = self._wins_check(mark)
            self.win = player.get_id() if self.win_comb else None
            if self.win:
                print("win", self.win, "\n")
            else:
                self._swap_players()
            return True, self.win_comb
        else:
            pass
        return False, False

    def __str__(self):
        fields = self.fields
        dim = self.dim
        start = self.start
        rows = ""
        for i in range(start, len(fields), dim):
            rows += "".join([str(fields[i]) for i in range(i, i + dim)]) + "\n"
        return rows.rstrip("\n")


if __name__ == "__main__":
    dim = 3
    wins = get_wins(dim=dim)
    p1 = Player(id_=1, mark="x")
    p2 = Player(id_=2, mark="o")
    g = Game(wins=wins, cell=Cell, dim=dim, players=[p1, p2])

    for q, w in zip(wins[2], wins[3]):
        g.game_turn(p1, q)
        g.game_turn(p2, w)
        if g.win:
            break

    print(str(g))
