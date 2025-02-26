from PyQt6.QtWidgets import QTabWidget
from MainWindow import MainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QRect

FONTNAME = 'Groboldov'


class TabsWidgets(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(180, 85, 1200, 675)
        self.setWindowTitle('The new century')
        self.setTabsClosable(True)

        self.addTab(MainWindow(self), 'Главное меню')
        self.setTabBarAutoHide(True)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet(f'''QTabWidget::pane {{
                                            border-top: none;
                                            border-left: none;
                                            border-right: none;
                                            border-bottom: none;}}
                               QTabBar::close-button {{image: url(summer/close_tab.png);}}
                               QTabBar::tab {{border: 3px solid #EDCBA5;
                                            font-family: {FONTNAME};
                                            color: #EDCBA5;
                                            border-top-left-radius: 10px;
                                            border-top-right-radius: 10px;
                                            min-width: 16ex;
                                            min-height: 2ex;
                                            background-color: #586970;
                                            padding: 2px;}}
                               QTabBar::tab:selected {{background-image: url(summer/tab.png)}}''')

        self.tabCloseRequested.connect(self.close_tab)

    # Закрытие вкладки
    def close_tab(self, index):
        if self.tabText(index) != 'Главное меню':
            name_tournament = self.widget(index).title_tournament
            self.widget(0).open_tournaments.remove(name_tournament)
            self.removeTab(index)
