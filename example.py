import sys

from PySide2.QtWidgets import QMainWindow, QApplication

from qchessboard import Board, AspectRatioWidget

app = QApplication(sys.argv)

window = QMainWindow()
board = Board(window)
board.resize(800, 800)

window.resize(1000, 1000)
window.setCentralWidget(AspectRatioWidget(board, window))
window.show()

sys.exit(app.exec_())
