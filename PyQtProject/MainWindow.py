from PyQt6.QtWidgets import QLabel, QMainWindow, QListWidget, QPushButton, QWidget
from PyQt6.QtCore import QRect, QUrl, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from Tournament import Tournament
from PyQtProject.create_widget.Create_tournament import Create_tournament
from Const import FONTNAME
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self, tabs):
        super().__init__()

        self.setGeometry(QRect(180, 85, 1200, 675))

        self.season = 'summer'

        self.con = sqlite3.connect('Tournaments.sqlite')
        self.cur = self.con.cursor()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.open_tournaments = []

        self.valume = 0
        self.load_mp3()

        self.colors_text = {'summer': '#EDCBA5', 'winter': '#2F8AB0'}
        self.color_tab = {'summer': '#EDCBA5', 'winter': '#09525C'}
        self.color_calendar = {'summer': '#B29F89', 'winter': '#163F45'}
        self.color_text_calendar = {'summer': '#6db188', 'winter': '#2F8AB0'}
        self.color_back_tab = {'summer': '#586970', 'winter': 'white'}

        self.style_button = f'''QPushButton {{ background-image: url({self.season}/button.png);
                                             border-radius: 10px;
                                             color: {self.colors_text[self.season]}}}
                              QPushButton:hover {{
                                             background-image: url({self.season}/button_dark.png)}}
                              QPushButton:pressed {{
                                             background-image: url({self.season}/button.png)}}'''
        self.style_back_button = f'''QPushButton {{ background-image: 
                                            url({self.season}/back.png);
                                            border-radius: 10px;
                                            color: #EDCBA5}}
                                QPushButton:hover {{
                                            background-image: url({self.season}/back_dark.png)}}
                                QPushButton:pressed {{
                                            background-image: url({self.season}/back.png)}}'''
        self.style_background = f"""background-image : 
                                        url({self.season}/main_background.jpg)"""

        self.tabs = tabs

        self.author_bool = 0

        self.background = QLabel(self)
        self.background.resize(1200, 675)
        self.background.setStyleSheet(self.style_background)

        arr_data_button = [('Открыть', 180), ('Создать', 300), ('Сменить вайб', 420)]
        self.arr_button = []
        for i in arr_data_button:
            button = QPushButton(i[0], self)
            button.move(200, i[1])
            button.resize(216, 80)
            button.setFont(QFont(FONTNAME, 18))
            button.setStyleSheet(self.style_button)
            button.clicked.connect(self.player.play)
            self.arr_button.append(button)

        self.arr_button[0].clicked.connect(self.open)
        self.arr_button[1].clicked.connect(self.create)
        self.arr_button[2].clicked.connect(self.vaib)

        self.sound_bool = 0
        self.sound = QPushButton('', self)
        self.sound.resize(100, 100)
        self.sound.move(1050, 525)
        self.sound.setStyleSheet(f'''QPushButton {{ background-image: 
                                             url({self.season}/sound_off.png);
                                             border-radius: 10px;}}
                              QPushButton:hover {{
                                        background-image: url({self.season}/sound_off_dark.png)}}
                              QPushButton:pressed {{
                                        background-image: url({self.season}/sound_off.png)}}''')
        self.sound.clicked.connect(self.change_sound)

        self.cross = QPushButton('', self)
        self.cross.resize(90, 90)
        self.cross.move(1070, 30)
        self.cross.setStyleSheet(f'''QPushButton {{ background-image: 
                                             url({self.season}/cross.png);
                                             border-radius: 10px;}}
                              QPushButton:hover {{
                                        background-image: url({self.season}/cross_dark.png)}}
                              QPushButton:pressed {{
                                        background-image: url({self.season}/cross.png)}}''')
        self.cross.clicked.connect(self.close_main)

    def load_mp3(self):
        self.media = QUrl.fromLocalFile(f'mp3/{self.season}.mp3')
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0)
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(self.media)

    def change_mp3(self, valume):
        self.media = QUrl.fromLocalFile(f'mp3/{self.season}.mp3')
        self.audio_output.setVolume(valume)
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(self.media)

    def change_sound(self, bo=1):
        self.sound_bool = 1 - self.sound_bool
        if bo == '0':
            self.sound_bool = 0
        on_off = 'on' if self.sound_bool == 1 else 'off'
        self.sound.setStyleSheet(f'''QPushButton {{ background-image: 
                                                    url({self.season}/sound_{on_off}.png);
                                                    border-radius: 10px;}}
                                      QPushButton:hover {{
                                    background-image: url({self.season}/sound_{on_off}_dark.png)}}
                                      QPushButton:pressed {{
                                    background-image: url({self.season}/sound_{on_off}.png)}}''')
        self.valume = 20 if self.sound_bool == 1 else 0
        self.change_mp3(self.valume)

    def create(self):
        c = Create_tournament(self)
        c.show()

    # Открытие уже создоного турнира
    def open(self):
        self.con = sqlite3.connect('Tournaments.sqlite')
        self.cur = self.con.cursor()

        arr = sorted(self.cur.execute(f'''SELECT title, date FROM tournament'''),
                     key=lambda x: (int(x[1].split('.')[2]), int(x[1].split('.')[1]),
                                    int(x[1].split('.')[0])))
        arr = [i for i in arr if i[0] not in self.open_tournaments]
        arr_tournament = [f'{i[1]}\n{i[0]}\n' for i in arr]

        self.open_widget = QWidget(self)
        self.open_widget.setGeometry(QRect(0, 0, 1200, 675))

        background = QLabel('', self.open_widget)
        background.resize(1200, 675)
        background.setStyleSheet(f'background-image : url({self.season}/main_background.jpg)')

        home = QPushButton('', self.open_widget)
        home.move(30, 30)
        home.resize(100, 100)
        home.setFont(QFont(FONTNAME, 18))
        home.setStyleSheet(self.style_back_button)
        home.clicked.connect(self.player.play)
        home.clicked.connect(self.close_open)

        button_choose_tournament = QPushButton('Выбрать', self.open_widget)
        button_choose_tournament.move(200, 300)
        button_choose_tournament.resize(216, 80)
        button_choose_tournament.setFont(QFont(FONTNAME, 18))
        button_choose_tournament.setStyleSheet(self.style_button)
        button_choose_tournament.clicked.connect(self.player.play)
        button_choose_tournament.clicked.connect(self.chopse_tournament)

        background_table = QLabel('', self.open_widget)
        background_table.setStyleSheet(f'background-image: url({self.season}/table_mini.png)')

        self.list_tournament = QListWidget(self.open_widget)

        if self.season == 'summer':
            background_table.resize(609, 450)
            background_table.move(500, 110)
            self.list_tournament.resize(500, 343)
            self.list_tournament.move(550, 155)
        else:
            background_table.resize(650, 465)
            background_table.move(495, 90)
            self.list_tournament.resize(500, 343)
            self.list_tournament.move(570, 165)

        self.list_tournament.setFont(QFont('Arial', 15))
        self.list_tournament.setStyleSheet(f'''QListWidget {{background: transparent; 
                                                color: {self.color_tab[self.season]};
                                                font-family: {FONTNAME};
                                                font-size: 15;
                                                border: none;}}
                                            QScrollBar:vertical {{
                                                background: transparent;
                                                width: 15px;
                                                margin: 0px 3px 0px 3px;
                                                border-radius: 4px;
                                            }}
                                QScrollBar::handle:vertical {{
                                                background-color: {self.color_tab[self.season]};                    
                                                min-height: 5px;
                                                border-radius: 4px;
                                            }}
                                QScrollBar::sub-line:vertical {{
                                                margin: 0px 0px 0px 0px;
                                                height: 0px;
                                                width: 10px;
                                                subcontrol-position: top;
                                                subcontrol-origin: margin;
                                            }}
                                QScrollBar::add-line:vertical {{
                                                margin: 0px 0px 0px 0px;
                                                height: 0px;
                                                width: 10px;
                                                subcontrol-position: bottom;
                                                subcontrol-origin: margin;
                                            }}
                                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                                                background: none;
                                            }}
                                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                                            background: none;
                                            }}
                                QScrollBar:horizontal {{
                                                background: transparent;
                                                height: 8px;
                                                margin: 0px 3px 0px 3px;
                                                border-radius: 4px;
                                            }}
                                QScrollBar::handle:horizontal {{
                                                background-color: {self.color_tab[self.season]};                    
                                                min-width: 5px;
                                                border-radius: 4px;
                                            }}
                                QScrollBar::add-line:horizontal {{
                                                margin: 0px 0px 0px 0px;
                                                height: 10px;
                                                width: 0px;
                                                subcontrol-position: left;
                                                subcontrol-origin: margin;
                                            }}
                                QScrollBar::left-arrow:horizontal, 
                                QScrollBar::right-arrow:horizontal {{
                                                background: none;
                                            }}
                                QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                                            background: none;
                                            }}''')

        self.list_tournament.addItems(arr_tournament)

        self.open_widget.show()

    # Открывает турнир
    def chopse_tournament(self):
        item = self.list_tournament.selectedItems()
        if len(item) != 0:
            title = item[0].text().split('\n')[1]
            id = list(self.cur.execute(f'SELECT id FROM tournament WHERE title = "{title}"'))[0][0]
            self.open_tournaments.append(title)
            self.open_widget.deleteLater()
            self.tabs.addTab(Tournament(self.season, self.colors_text, self.media,
                                        self.valume, id), 'Турнир')
            self.tabs.setCurrentIndex(self.tabs.count() - 1)

    # Закрывает окно открытия групп)
    def close_open(self):
        self.open_widget.deleteLater()

    def close_main(self):
        self.tabs.close()

    def vaib(self):
        if self.season == 'summer':
            self.season = 'winter'
        else:
            self.season = 'summer'
        self.style_button = f'''QPushButton {{ background-image: url({self.season}/button.png);
                                                    border-radius: 10px;
                                                    color: {self.colors_text[self.season]}}}
                                      QPushButton:hover {{
                                            background-image: url({self.season}/button_dark.png)}}
                                      QPushButton:pressed {{
                                                background-image: url({self.season}/button.png)}}'''
        self.style_background = f"""background-image : 
                                        url({self.season}/main_background.jpg)"""
        self.style_back_button = f'''QPushButton {{ background-image: 
                                                    url({self.season}/back.png);
                                                    border-radius: 10px;
                                                    color: #EDCBA5}}
                                        QPushButton:hover {{
                                            background-image: url({self.season}/back_dark.png)}}
                                        QPushButton:pressed {{
                                                background-image: url({self.season}/back.png)}}'''

        self.change_sound('0')
        self.tabs.setStyleSheet(f'''QTabWidget::pane {{
                                            border-top: none;
                                            border-left: none;
                                            border-right: none;
                                            border-bottom: none;}}
                                    QTabBar::close-button 
                                            {{image: url({self.season}/close_tab.png);}}
                              QTabBar::tab {{border: 2px solid {self.colors_text[self.season]};
                                            font-family: {FONTNAME};
                                            color: {self.color_tab[self.season]};
                                            border-top-left-radius: 10px;
                                            border-top-right-radius: 10px;
                                            min-width: 16ex;
                                            min-height: 2ex;
                                            padding: 2px;
                                            background-color: {self.color_back_tab[self.season]};
                                            }}
                              QTabBar::tab:selected {{background-image: 
                              url({self.season}/tab.png)}}''')
        self.cross.setStyleSheet(f'''QPushButton {{ background-image: 
                                                url({self.season}/cross.png);
                                                 border-radius: 10px;}}
                                      QPushButton:hover {{
                                            background-image: url({self.season}/cross_dark.png)}}
                                      QPushButton:pressed {{
                                             background-image: url({self.season}/cross.png)}}''')

        for button in self.arr_button:
            button.setStyleSheet(self.style_button)
        self.background.setStyleSheet(self.style_background)
