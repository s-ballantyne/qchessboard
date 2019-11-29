from PySide2.QtCore import QRect
from PySide2.QtGui import QPaintEvent, QColor as QColour, QPainter, Qt, QResizeEvent, QFont, QImage
from PySide2.QtWidgets import QWidget, QBoxLayout, QSpacerItem

from math import ceil


# https://stackoverflow.com/questions/30005540/keeping-the-aspect-ratio-of-a-sub-classed-qwidget-during-resize
class AspectRatioWidget(QWidget):
	def __init__(self, widget, parent):
		super().__init__(parent)

		self._ratio = widget.size().width() / widget.size().height()
		self.setLayout(QBoxLayout(QBoxLayout.LeftToRight, self))

		self.layout().addItem(QSpacerItem(0, 0))
		self.layout().addWidget(widget)
		self.layout().addItem(QSpacerItem(0, 0))

	def resizeEvent(self, event: QResizeEvent):
		w = event.size().width()
		h = event.size().height()

		if (w / h) > self._ratio:
			self.layout().setDirection(QBoxLayout.LeftToRight)
			widget_stretch = h * self._ratio
			outer_stretch = (w - widget_stretch) / 2 + 0.5
		else:
			self.layout().setDirection(QBoxLayout.TopToBottom)
			widget_stretch = w / self._ratio
			outer_stretch = (h - widget_stretch) / 2 + 0.5

		self.layout().setStretch(0, outer_stretch)
		self.layout().setStretch(1, widget_stretch)
		self.layout().setStretch(2, outer_stretch)


class Board(QWidget):
	def __init__(self, parent, files: int = 8, ranks: int = 8):
		super().__init__(parent)

		self._drawCoordinates = True
		self._coordinateFont = QFont("Roboto", 12, QFont.Bold)
		self._coordinateAlignmentFile = Qt.AlignLeft | Qt.AlignBottom
		self._coordinateAlignmentRank = Qt.AlignLeft | Qt.AlignTop

		self._squareColours = [QColour(0xf0, 0xd9, 0xb5), QColour(0xb5, 0x88, 0x63)]

		self._files = files
		self._ranks = ranks

		self._board = [[0 for _ in range(self.files())] for _ in range(self.ranks())]

	def pieceOn(self, file: int, rank: int):
		return self._board[7 - rank][file]

	def setPiece(self, file: int, rank: int, image: str):
		self._board[7 - rank][file] = image

	def files(self):
		return self._files

	def ranks(self):
		return self._ranks

	def paintEvent(self, event: QPaintEvent):
		rect = event.rect()
		painter = QPainter(self)
		painter.setFont(self._coordinateFont)

		dx = ceil((rect.right() - rect.left()) / self.files())
		dy = ceil((rect.bottom() - rect.top()) / self.ranks())
		left, top = 0, 0
		for r in range(self.ranks()):
			for f in range(self.files()):
				square = QRect(left, top, dx, dy)
				is_dark = (f + r) % 2

				painter.fillRect(
					square,
					self._squareColours[is_dark]
				)

				if self._board[7 - r][f]:
					painter.drawImage(square, QImage(self._board[7 - r][f]))

				if self._drawCoordinates:
					if r == self.ranks() - 1:
						painter.setPen(self._squareColours[~is_dark])
						painter.drawText(square, self._coordinateAlignmentFile, "abcdefgh"[f])

					if f == 0:
						painter.setPen(self._squareColours[~is_dark])
						painter.drawText(square, self._coordinateAlignmentRank, str(8 - r))

				left += dx

			left = 0
			top += dy
