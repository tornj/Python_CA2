# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtSvg import *
# from PyQt5.QtWidgets import *
import sys

from PyQt5 import QtWidgets
# from abc import abstractmethod
# import sys
from cardlib import *
from pokermodel import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


# NOTE: This is just given as an example of how to use CardView.
# It is expected that you will need to adjust things to make a game out of it.

###################
# Models
###################

# We can extend this class to create a model, which updates the view whenever it has changed.
# NOTE: You do NOT have to do it this way.
# You might find it easier to make a Player-model, or a whole GameState-model instead.
# This is just to make a small demo that you can use. You are free to modify

###################
# Card widget code:
###################

# hand = HandModel()
# hand.add_card(NumberedCard(10, Suit.Spades))
# hand.add_card(NumberedCard(10, Suit.Hearts))


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #self.Window = Window()
        self.setStyleSheet("background-image: url(cards/royal-straight-flush.jpg);")
        self.setWindowTitle("Texas hold'em")
        self.setGeometry(10, 50, 640, 475)


        LblNameP1 = QLabel("Player 1 Name: ")
        self.NameP1 = QLineEdit()

        LblNameP2 = QLabel("Player 2 Name: ")
        self.NameP2 = QLineEdit()

        LblStake = QLabel("Stake: ")
        self.Stake = QLineEdit()

        hbox1 = QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(LblNameP1)
        hbox1.addWidget(self.NameP1)
        hbox1.addStretch()

        hbox2 = QHBoxLayout()
        hbox2.addStretch()
        hbox2.addWidget(LblNameP2)
        hbox2.addWidget(self.NameP2)
        hbox2.addStretch()

        hbox3 = QHBoxLayout()
        hbox3.addStretch()
        hbox3.addWidget(LblStake)
        hbox3.addWidget(self.Stake)
        hbox3.addStretch()

        hbox = QHBoxLayout()
        self.button = QPushButton("Start")
        self.button.setStyleSheet("background : orange")
        self.button.clicked.connect(self.OpenGame)
        self.button.clicked.connect(self.close)

        hbox.addStretch()
        hbox.addWidget(self.button)
        hbox.addStretch()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox)
        #vbox.addWidget(CreateButton(['Start']))

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)


    # # Onödig då vi nu har PassingInformation
    def OpenGame(self):
        self.list_of_players = [self.NameP1.text(), self.NameP2.text()]
        model = GameModel([PlayerModel(self.list_of_players[0], self.Stake.text()), PlayerModel(self.list_of_players[1], self.Stake.text())])
        self.window = Window(model)
        self.window.show()

    # def PassingInformation(self):
    #     self.Window.PlayerName1.setText("Player " + self.NameP1.text())
    #     self.Window.PlayerName2.setText("Player " + self.NameP2.text())
    #     self.Window.DisplayInfo()


class PlayerView(QGroupBox):
    def __init__(self, player, game):
        super().__init__(player.name)

        self.setFont(QFont('BankGothic MD BT', 15))
        self.setStyleSheet('text: red')
        self.player = player
        vbox = QVBoxLayout()
        vbox.addStretch()
        #self.setLayout(vbox)
        hbox=QHBoxLayout()
        #self.setLayout(hbox)
        self.bal=QLabel('Balance:' + str(self.player.balance)) #ändra här för att koden ska funka
        self.bal.setFont(QFont('BankGothic MD BT', 15))
        self.bet=QLabel('Bet:' + str(self.player.bet))
        self.bet.setFont(QFont('BankGothic MD BT', 15))
        hbox.addWidget(self.bal)
        hbox.addStretch()
        hbox.addWidget(self.bet)
        hbox.addStretch()
        vbox.addLayout(hbox)
        card_view = CardView(player.hand, 150, 70)
        vbox.addWidget(card_view)
        #self.setLayout(hbox)
        self.player_buttons = []
        hbox3 = QHBoxLayout()
        for item in ['Fold', 'Call/Check', 'Bet/Raise']:
            button = QPushButton(item)
            button.setStyleSheet("background : white")
            self.player_buttons.append(button)
            hbox3.addWidget(button)
        vbox.addLayout(hbox3)
        vbox.addStretch()
        self.setLayout(vbox)
        self.show()
        #self.setStyleSheet("border: transparent;")

        def fold(): game.fold()
        def call_check(): game.call()

        def bet_raise():
            bet_min, bet_max = game.bet_limits()
            #game.check_all_in()
            val, ok = QInputDialog.getInt(self, 'Bet', 'Place bet:', 0, bet_min, bet_max)
            if ok:
                game.bet(val)

        self.player_buttons[0].clicked.connect(fold)
        self.player_buttons[1].clicked.connect(call_check)
        self.player_buttons[2].clicked.connect(bet_raise)

        #game.update_bet.connect(bet_raise)
        player.active_changed.connect(self.next_player)
        game.data_changed.connect(self.money_changed)
        game.disable_bet_button.connect(self.disable_button)
        self.disable_button()
        self.money_changed()
        self.next_player()

    def disable_button(self):
        self.player_buttons[2].setDisabled(True)

    def next_player(self):
        for b in self.player_buttons:
            b.setEnabled(self.player.active)

    def money_changed(self):
        self.bet.setText("Bet: " + str(self.player.bet))
        self.bal.setText("Balance: " + str(self.player.balance))


class Window(QMainWindow):
    """ """
    def __init__(self, game):
        super().__init__()
        # changing the background color to yellow
        self.setStyleSheet("background-image: url(cards/table.png);")
        self.game = game
        # set the title
        self.setWindowTitle("Texas hold'em")
        # setting  the geometry of window
        self.setGeometry(10, 50, 1900, 1000)
        self.pot = QLabel('Pot: ')
        self.pot.setStyleSheet('border: 1px inset grey ')
        self.pot.setAlignment(Qt.AlignCenter)
        self.pot.setFont(QFont('BankGothic MD BT', 30))
        hbox4=QHBoxLayout()
        hbox4.addStretch()
        hbox4.addWidget(self.pot)
        hbox4.addStretch()
        hbox2 = QHBoxLayout()
        hbox2.addStretch()
        self.table_cards = CardView(game.table_cards, 150, 110)
        hbox2.addWidget(self.table_cards)
        hbox2.addStretch()
        hbox3 = QHBoxLayout()

        self.player_views = []
        for p in game.players:
            player_view = PlayerView(p, game)
            self.player_views.append(player_view)
            hbox3.addWidget(player_view)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch()
        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        game.game_message.connect(self.alert_user)
        game.data_changed.connect(self.pot_changed)
        game.update_table_cards.connect(self.change_table_cards)
        game.Start()
        #self.update()

    def change_table_cards(self):
        self.table_cards.change_cards()

    def DisplayInfo(self):
        self.show()

    def pot_changed(self):
        self.pot.setText("Pot: " + str(self.game.pot))

    def alert_user(self, text):
        box = QMessageBox()
        box.setText(text)
        box.exec_()

class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))

class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position

def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    suit_name = ["Hearts", "Spades", "Clubs", "Diamonds"]
    all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
    #for suit_file, suit in zip("HDSC", range(4)):
    for suit in suit_name:
    # Check the order of the suits here!!!
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit[0]
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
    return all_cards


class CardView(QGraphicsView):
    """ A View widget that represents the table area displaying a players cards. """

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    # size = back_card.defaultSize()
    # size.scale(1000, 1000, Qt.KeepAspectRatio)

    all_cards = read_cards()

    def __init__(self, card_model: CardModel, card_spacing: int = 250, padding: int = 10):
        """
        Initializes the view to display the content of the given model
        :param card_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.setStyleSheet("border: transparent;")
        self.card_spacing = card_spacing
        self.padding = padding
        self.model = card_model
        card_model.new_cards.connect(self.change_cards)
        self.change_cards()

    def change_cards(self):
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit.name)

            #renderer = self.back_card if self.model.flipped() else self.all_cards[graphics_key]

            if self.model.flipped():
                renderer = self.back_card
            else:
                renderer = self.all_cards[graphics_key]

            c = CardItem(renderer, i)

            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)
            # We could also do cool things like marking card by making them transparent if we wanted to!
            #c.setOpacity(0.5 if self.model.marked(i) else 1.0)
            self.scene.addItem(c)

        self.update_view()

    def update_view(self):
        scale = (self.viewport().height()-2*self.padding)/313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding//scale, -self.padding//scale,
                          self.viewport().width()//scale, self.viewport().height()//scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we gotta adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)

