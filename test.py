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
            hbox.setContentsMargins(0, 0, 800, 50)
        self.setLayout(hbox)