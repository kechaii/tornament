from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import QPushButton


class DragButton(QPushButton):
    def setedit(self, e):
        self.edit = e

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton and not self.signalsBlocked() and self.edit:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)
