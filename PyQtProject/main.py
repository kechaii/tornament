import sys
from PyQt6.QtWidgets import QApplication
from TabWidget import TabsWidgets

# Запуск программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TabsWidgets()
    window.show()
    sys.exit(app.exec())
