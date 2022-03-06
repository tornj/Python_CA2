from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from abc import abstractmethod
from pokermodel import GameModel
from pokerview import *
import sys


def Main():
    app = QApplication(sys.argv)
    w = StartWindow()
    w.show()
    app.exec_()

if __name__ == '__main__':
    Main()











