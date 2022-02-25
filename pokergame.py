from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from abc import abstractmethod
import sys

app = QApplication(sys.argv)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.labels = labels
        # self.buttons = buttons

        cBtn = QPushButton("Call/Check")
        betBtn = QPushButton("bet")
        foldBtn = QPushButton("fold")

        balanceLbl = QLabel("Balance")
       #backCard = QSvgRenderer('')
        #card = QGraphicsView.("cards/cards/Red_Back_2.svg")
        # card = QLabel("HandCard1")
        # card.setPixmap(QtGui.QPixmap("cards/cards/Red_Back_2.svg"))
        # card = QGraphicsSvgItem()
        # rend = QSvgRenderer("cards/cards/Red_Back_2.svg")
        # card.setSharedRenderer(rend)

        card2 = QLabel("HandCard2")

        card3 = QLabel("Card1")
        card4 = QLabel("Card2")
        card5 = QLabel("Card3")


        betPlayer1 = QLabel("Bet: ")
        betPlayer1.setAlignment(Qt.AlignCenter)
        betPlayer2 = QLabel("Bet: ")
        betPlayer2.setAlignment(Qt.AlignCenter)

        pot = QLabel("Pot: ")

        hbox1 = QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(foldBtn)
        hbox1.addWidget(cBtn)
        hbox1.addWidget(betBtn)
        hbox1.addStretch()

        hbox2 = QHBoxLayout()
        hbox2.addStretch()
        hbox2.addWidget(balanceLbl)
        #hbox2.addWidget(card)
        hbox2.addWidget(card2)
        hbox2.addStretch()

        hbox3 = QHBoxLayout()
        hbox3.addStretch()
        hbox3.addWidget(pot)
        hbox3.addWidget(card3)
        hbox3.addWidget(card4)
        hbox3.addWidget(card5)
        hbox3.addStretch()

        vbox = QVBoxLayout()
        vbox.addStretch()

        vbox.addWidget(betPlayer2)
        vbox.addLayout(hbox3)
        vbox.addWidget(betPlayer1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox1)

        self.setLayout(vbox)


        self.setGeometry(100, 100, 600, 450)
        self.setWindowTitle("Texas hold'em")
        #self.setStyleSheet("background-color: green;")
        self.setStyleSheet("background-image: url(cards/table.png);")

win = MyWindow()
win.show()
app.exec_()








#win.show()

# window = QWidget()
# window.setStyleSheet("background-color: green;")

#
# hbox = QHBoxLayout()
# hbox.addStretch(1)
# hbox.addWidget(cButton)
# hbox.addWidget(betBtn)
# hbox.addWidget(foldBtn)
# window.setAlignment(Qt.AlignCenter)
#
# vbox = QVBoxLayout()
# vbox.addStretch(1)
# vbox.addLayout(hbox)
#
# window.setLayout(vbox)
# window.setWindowTitle('Poker Game')
# window.show()



