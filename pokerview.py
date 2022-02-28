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

hand = HandModel()
hand.add_card(NumberedCard(10, Suit.Spades))
hand.add_card(NumberedCard(10, Suit.Hearts))


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.start = None  # No extra window yet
        self.Window = Window()

        self.setStyleSheet("background-image: url(cards/royal-straight-flush.jpg);")
        self.setWindowTitle("Texas hold'em")
        self.setGeometry(10, 50, 640, 475)


        LblNameP1 = QLabel("Player 1 Name: ")
        self.NameP1 = QLineEdit()

        LblNameP2 = QLabel("Player 2 Name: ")
        NameP2 = QLineEdit()

        LblStake = QLabel("Stake: ")
        Stake = QLineEdit()

        hbox1 = QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(LblNameP1)
        hbox1.addWidget(self.NameP1)
        hbox1.addStretch()

        hbox2 = QHBoxLayout()
        hbox2.addStretch()
        hbox2.addWidget(LblNameP2)
        hbox2.addWidget(NameP2)
        hbox2.addStretch()

        hbox3 = QHBoxLayout()
        hbox3.addStretch()
        hbox3.addWidget(LblStake)
        hbox3.addWidget(Stake)
        hbox3.addStretch()

        hbox = QHBoxLayout()
        self.button = QPushButton("Start")
        self.button.setStyleSheet("background : orange")
        self.button.clicked.connect(self.PassingInformation)
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

    # Onödig då vi nu har PassingInformation
    def OpenGame(self):
        self.Window.show()

    def PassingInformation(self):
        self.Window.PlayerName.setText(self.NameP1.text())
        self.Window.DisplayInfo()



class Window(QMainWindow):
    """ """
    def __init__(self):
        super().__init__()
        # changing the background color to yellow
        self.setStyleSheet("background-image: url(cards/table.png);")

        # set the title
        self.setWindowTitle("Texas hold'em")
        # setting  the geometry of window
        self.setGeometry(10, 50, 1900, 1200)


        #d = StandardDeck()

        pot = QLabel('Pot: ')
        bet = QLabel('Bet: ')
        bet2 = QLabel('Bet: ')

        bet.setAlignment(Qt.AlignCenter)
        bet2.setAlignment(Qt.AlignCenter)

        self.PlayerName = QLabel('PlayerName')


        hbox = QHBoxLayout()
        #hbox.addStretch()
        hbox.addWidget(pot)
        card_view = CardView(hand)
        hbox.addWidget(card_view)

        hbox.setAlignment(Qt.AlignCenter)

        table = HandModel()
        table.add_card(JackCard(Suit.Hearts))


        table_cards = CardView(table)

        hbox2 = QHBoxLayout()
        hbox2.addStretch()
        hbox2.addWidget(self.PlayerName)
        hbox2.addWidget(CreateButton(['Fold', 'Call', 'Raise/Bet']))
        hbox2.addStretch()



        vbox = QVBoxLayout()
        #vbox.addStretch()
        vbox.addWidget(bet2)
        vbox.addWidget(table_cards)
        vbox.addLayout(hbox)
        vbox.addWidget(bet)
        vbox.addLayout(hbox2)
        #vbox.addStretch()
        #vbox.setAlignment(Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def DisplayInfo(self):
        self.show()

        # vbox.addWidget(MoreExcitingContent(...))


class CreateButton(QWidget):
    def __init__(self, labels):
        super().__init__()
        self.labels = labels
        hbox = QHBoxLayout()
        hbox.addStretch()
        for label in labels:
            button = QPushButton(label)
            if label == "Fold":
                button.clicked.connect(hand.flip)
            # elif label == 'Start':
            #     button.clicked.connect(StartWindow.OpenGame)
            else:
                button.clicked.connect(lambda checked, label=label: print(label))
            button.setStyleSheet("background : white")
            hbox.addWidget(button)
            #hbox.setContentsMargins(0, 0, 800, 50)

        hbox.addStretch()

        self.setLayout(hbox)
        #self.resize(100, 100)


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
        :param cards_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.setStyleSheet("border: transparent;")

        self.card_spacing = card_spacing
        self.padding = padding

        self.model = card_model
        # Whenever the this window should update, it should call the "change_cards" method.
        # This can, for example, be done by connecting it to a signal.
        # The view can listen to changes:
        card_model.new_cards.connect(self.change_cards)
        # It is completely optional if you want to do it this way, or have some overreaching Player/GameState
        # call the "change_cards" method instead. z

        # Add the cards the first time around to represent the initial state.
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
            # c.setOpacity(0.5 if self.model.marked(i) else 1.0)
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

    # This is the Controller part of the GUI, handling input events that modify the Model
    # def mousePressEvent(self, event):
    #    # We can check which item, if any, that we clicked on by fetching the scene items (neat!)
    #    pos = self.mapToScene(event.pos())
    #    item = self.scene.itemAt(pos, self.transform())
    #    if item is not None:
    #        # Report back that the user clicked on the card at given position:
    #        # The model can choose to do whatever it wants with this information.
    #        self.model.clicked_position(item.position)

    # You can remove these events if you don't need them.
    # def mouseDoubleClickEvent(self, event):
    #    self.model.flip() # Another possible event. Lets add it to the flip functionality for fun!

###################
# Main test program
###################

# Lets test it out
app = QApplication(sys.argv)
w = StartWindow()
w.show()
# window = Window()
# window.show()
app.exec_()
