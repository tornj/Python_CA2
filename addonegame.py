from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
qt_app = QApplication(sys.argv)
class GameState(QObject):
    # We might have multiple signals! One for updates
    data_changed = pyqtSignal()
    # and one for messaging
    game_message = pyqtSignal((str,))  # (x,) is the notation for a tuple with just one value!

    def __init__(self, players):
        super().__init__()
        self.running = False
        self.players = players
        self.player_turn = -1
        self.total = 0

    def start(self):
        if self.running:
            self.game_message.emit("Can't start game. Game already running")

        self.running = True
        self.player_turn = 0
        self.total = 0
        self.players[self.player_turn].set_active(True)
        self.data_changed.emit()

    def add(self, num):
        # Called when a player adds a value (this also switches the players turn)
        self.total += num
        if self.total >= 20:
            winner = self.players[self.player_turn]
            self.game_message.emit("Player {} won!".format(winner.name))
            winner.won()
            self.total = 0

        self.players[self.player_turn].set_active(False)
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.players[self.player_turn].set_active(True)
        self.data_changed.emit()


# A simple player state. It keeps track of the score.
class PlayerState(QObject):
    data_changed = pyqtSignal()

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.wins = 0
        self.active = False

    def set_active(self, active):
        self.active = active
        self.data_changed.emit()

    def won(self):
        self.wins += 1
        self.data_changed.emit()


class PlayerView(QGroupBox):
    def __init__(self, player, game):
        super().__init__(player.name)
        self.player = player
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.wins = QLabel()
        layout.addWidget(self.wins)

        self.buttons = []
        for b in range(3):
            button = QPushButton("Add {}".format(b + 1))
            self.buttons.append(button)
            layout.addWidget(button)
            # button.clicked.connect( lambda : game.add(b+1) )

        def add_1(): game.add(1)

        def add_2(): game.add(2)

        def add_3(): game.add(3)

        self.buttons[0].clicked.connect(add_1)
        self.buttons[1].clicked.connect(add_2)
        self.buttons[2].clicked.connect(add_3)

        player.data_changed.connect(self.update)
        self.update()

    def update(self):
        self.wins.setText("Wins: " + str(self.player.wins))
        for b in self.buttons:
            b.setEnabled(self.player.active)


class GameView(QWidget):
    def __init__(self, game):
        super().__init__()

        self.game = game

        layoutv = QVBoxLayout()
        self.setLayout(layoutv)

        self.total_label = QLabel("uninitialized")
        layoutv.addWidget(self.total_label)

        layouth = QHBoxLayout()
        layoutv.addLayout(layouth)

        self.player_views = []
        for p in game.players:
            player_view = PlayerView(p, game)
            self.player_views.append(player_view)
            layouth.addWidget(player_view)

        game.game_message.connect(self.alert_user)
        game.data_changed.connect(self.update)
        game.start()  # We start as soon as we get a view!
        self.update()

    def alert_user(self, text):
        # A method like this is nice to have for showing if the game is over,
        # or warn about faulty input.
        box = QMessageBox()
        box.setText(text)
        box.exec_()

    def update(self):
        self.total_label.setText("Total: " + str(self.game.total))

qt_app = QApplication.instance()

model = GameState([PlayerState("Cornelia"), PlayerState("Johannes")])

view = GameView(model)
view.show()

qt_app.exec_()