from PyQt6.QtWidgets import QLabel, QPushButton, QWidget, QLineEdit, QSpinBox, QCalendarWidget, \
    QFrame
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QFont
from PyQtProject.Tournament import Tournament
from PyQtProject.Const import FONTNAME, QUANTILY_LEAGUE


# Класс для создания турнира
class Create_tournament(QWidget):
    def __init__(self, main):
        super(Create_tournament, self).__init__(main)

        self.setGeometry(QRect(0, 0, 1200, 675))

        background = QLabel('', self)
        background.resize(1200, 675)
        background.setStyleSheet(main.style_background)

        self.main = main

        button_save_tournament = QPushButton('Сохранить', self)
        button_save_tournament.move(200, 300)
        button_save_tournament.resize(216, 80)
        button_save_tournament.setFont(QFont(FONTNAME, 18))
        button_save_tournament.setStyleSheet(main.style_button)
        button_save_tournament.clicked.connect(main.player.play)
        button_save_tournament.clicked.connect(self.save_tournament)

        home = QPushButton('', self)
        home.move(30, 30)
        home.resize(100, 100)
        home.setFont(QFont(FONTNAME, 18))
        home.setStyleSheet(main.style_back_button)
        home.clicked.connect(main.player.play)
        home.clicked.connect(self.close_create)

        background_table = QLabel('', self)
        background_table.setStyleSheet(f'background-image: url({main.season}/table_mini.png)')

        self.title_widget = QLineEdit('Название', self)
        self.title_widget.resize(400, 65)
        self.title_widget.move(555, 170)
        self.title_widget.setStyleSheet(f'''QLineEdit {{
                                                        background: transparent;
                                                    border: 4px solid {main.color_tab[main.season]};
                                                        border-radius: 10px;
                                                        selection-color: black;
                                                        selection-background-color: white;
                                                        color: {main.color_tab[main.season]}
                                                        }}''')

        self.title_widget.setFont(QFont(FONTNAME, 15))

        self.quantity_widget = QSpinBox(self)
        self.quantity_widget.resize(90, 65)
        self.quantity_widget.move(970, 170)
        self.quantity_widget.setMinimum(1)
        self.quantity_widget.setFont(QFont(FONTNAME, 15))
        self.quantity_widget.setStyleSheet(f'''QSpinBox {{
                                                        background: transparent;
                                                    border: 4px solid {main.color_tab[main.season]};
                                                        border-radius: 10px;
                                                        selection-color: black;
                                                        selection-background-color: white;
                                                        color: {main.color_tab[main.season]}
                                                        }}
                                                      QSpinBox::up-button {{ 
                                                        width: 40px; height: 30px; }}
                                                      QSpinBox::down-button {{ 
                                                        width: 40px; height: 30px; }}''')
        self.quantity_widget.setMaximum(QUANTILY_LEAGUE)

        if main.season == 'summer':
            background_table.resize(609, 450)
            background_table.move(500, 110)
        else:
            background_table.resize(650, 465)
            background_table.move(495, 90)

        self.frame = QFrame(parent=self)
        self.frame.setGeometry(QRect(600, 250, 400, 240))
        self.frame.setStyleSheet(f'''QFrame {{
                                                border-radius: 10px;
                                                background-color: {main.color_tab[main.season]};
                                                }}''')
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.show()

        self.calendar = QCalendarWidget(parent=self.frame)
        self.calendar.resize(390, 230)
        self.calendar.move(5, 5)
        self.calendar.setStyleSheet(f'''QCalendarWidget QWidget{{
                                                            background: 
                                                            {main.color_tab[main.season]};
                                                    color: {main.color_text_calendar[main.season]};
                                                            alternate-background-color: 
                                                            {main.color_tab[main.season]};
                                                            selection-color: black;
                                                            selection-background-color: white;
                                                            }}
                                                QCalendarWidget QMenu{{
                                                            font-family: {FONTNAME}}}
                                                #qt_calendar_prevmonth,
                                                #qt_calendar_nextmonth{{
                                                            border: none;}}
                                                QCalendarWidget QAbstractItemView:disabled{{
                                                color: {main.color_calendar[main.season]}}}''')
        self.calendar.setFont(QFont(FONTNAME, 15))
        self.calendar.setNavigationBarVisible(True)
        self.calendar.setDateEditEnabled(True)
        self.calendar.setAutoFillBackground(False)
        self.calendar.show()

    # Сохранение Турнира
    def save_tournament(self):
        date = self.calendar.selectedDate()
        self.date = f'{date.day()}.{date.month()}.{date.year()}'
        self.title_tournament = self.title_widget.text()
        self.quantity_league = self.quantity_widget.value()
        try:
            self.main.cur.execute(f"""INSERT 
                                         INTO tournament(title, date, quantity) VALUES
                                         ('{self.title_tournament}', 
                                         '{self.date}', {self.quantity_league})""")

            self.main.con.commit()
            self.id_tournament = self.main.cur.execute(f'''SELECT id FROM tournament 
                                                        WHERE title = "{self.title_tournament}"''')
            self.id_tournament = list(self.id_tournament)[0][0]
            self.deleteLater()
            self.frame.deleteLater()
            self.calendar.deleteLater()
            self.main.open_tournaments.append(self.title_tournament)
            self.main.tabs.addTab(
                Tournament(self.main.season, self.main.colors_text, self.main.media,
                           self.main.valume, self.id_tournament), 'Турнир')
            self.main.tabs.setCurrentIndex(self.main.tabs.count() - 1)

        except Exception:
            self.title_widget.setText('Название занято')

    def close_create(self):
        self.deleteLater()
        self.frame.deleteLater()
        self.calendar.deleteLater()
