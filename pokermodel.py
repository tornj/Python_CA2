from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *

from abc import abstractmethod
import sys

qt_app = QApplication(sys.argv)

class Window(QMainWindow):
    """ """
    def __init__(self):
        super().__init__()
        # changing the background color to yellow
        self.setStyleSheet("background-color: green;")
        # set the title
        self.setWindowTitle("Texas hold'em")
        # setting  the geometry of window
        self.setGeometry(10, 50, 1900, 900)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(CreateButton(['Fold', 'Call','Raise/Bet']))
        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        # vbox.addWidget(MoreExcitingContent(...))


class CreateButton(QWidget):
    def __init__(self, labels):
        super().__init__()
        self.labels = labels
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        for label in labels:
            button = QPushButton(label)
            button.clicked.connect(lambda checked, label=label: print(label))
            button.setStyleSheet("background-color : white")
            hbox.addWidget(button)
            hbox.setContentsMargins(0, 0, 800 , 50)
        self.setLayout(hbox)

# class TableScene(QGraphicsScene):
#     """ A scene with a table cloth background """
#     def __init__(self):
#         super().__init__()
#         self.tile = QPixmap('cards/table.png')
#         self.setBackgroundBrush(QBrush(self.tile))


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
    all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
    for suit in 'HDSC':  # You'll need to map your suits to the filenames here. You are expected to change this!
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
    return all_cards


window=Window()
window.show()
qt_app.exec_()
