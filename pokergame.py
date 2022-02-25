from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from abc import abstractmethod
import sys




class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))
        self.show()

Table_scene = TableScene()


# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # changing the background color to yellow
#         self.setStyleSheet("background-color: green;")
#
#         # set the title
#         self.setWindowTitle("Texas hold'em")
#
#         # setting  the geometry of window
#         self.setGeometry(0, 0, 400, 300)
#
#         # creating a label widget
#         self.label = QLabel("texas hold'em", self)
#
#         # moving position
#         self.label.move(100, 100)
#
#         # setting up border
#         self.label.setStyleSheet("border: 1px solid black;")
#
#         # show all the widgets
#         self.show()


# create the instance of our Window
# window = Window()
# create pyqt5 app
App = QApplication(sys.argv)

# start the app
sys.exit(App.exec())