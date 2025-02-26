from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QCheckBox, QSpinBox, \
    QRadioButton, QTabWidget
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont
from PyQtProject.Const import FONTNAME, NAME_LEAGUE, NAME_LETTER, QUANTILY_GROUP, QUANTILY_GROUP_ONLY


class Create_league(QWidget):
    def __init__(self, main):
        super(Create_league, self).__init__(main)

        self.setGeometry(QRect(0, 0, 1200, 675))

        self.main = main

        background = QLabel('', self)
        background.resize(1200, 675)
        background.setStyleSheet(main.style_background)

        button_save_league = QPushButton('Сохранить', self)
        button_save_league.move(200, 300)
        button_save_league.resize(216, 80)
        button_save_league.setFont(QFont(FONTNAME, 18))
        button_save_league.setStyleSheet(main.style_button)
        button_save_league.clicked.connect(main.player.play)
        button_save_league.clicked.connect(self.save_league)

        background_table = QLabel('', self)
        background_table.setStyleSheet(f'background-image: url({main.season}/table_mini.png)')
        if main.season == 'summer':
            background_table.resize(609, 450)
            background_table.move(500, 110)
        else:
            background_table.resize(650, 465)
            background_table.move(495, 90)

        self.title_format = QComboBox(self)
        self.title_format.resize(190, 50)
        self.title_format.move(615, 170)
        self.title_format.addItems(NAME_LEAGUE)
        self.title_format.setFont(QFont(FONTNAME, 15))
        self.title_format.setStyleSheet(main.style_combobox)

        self.letter_league = QComboBox(self)
        self.letter_league.resize(190, 50)
        self.letter_league.move(825, 170)
        self.letter_league.addItems(NAME_LETTER)
        self.letter_league.addItem('Без буквы')
        self.letter_league.setFont(QFont(FONTNAME, 15))
        self.letter_league.setStyleSheet(main.style_combobox)
        self.letter_league.activated.connect(self.change_quantity)

        self.create_groups = QCheckBox('Создать с группами', self)
        self.create_groups.resize(400, 60)
        self.create_groups.move(150, 399)
        self.create_groups.setFont(QFont(FONTNAME, 20))
        self.create_groups.setStyleSheet(main.style_checkbox)
        self.create_groups.clicked.connect(main.player.play)

        self.true_input = QLabel('', self)
        self.true_input.resize(267, 100)
        self.true_input.move(672, 50)
        self.true_input.setFont(QFont(FONTNAME, 17))
        self.true_input.setStyleSheet(f'''background-image: url({main.season}/background_lable.png);
                                              color: {main.color_lable[main.season]}''')
        self.true_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.quantity_widget = QSpinBox(self)
        self.quantity_widget.resize(400, 50)
        self.quantity_widget.move(615, 280)
        self.quantity_widget.setFont(QFont(FONTNAME, 15))
        self.quantity_widget.setMinimum(1)
        self.quantity_widget.setStyleSheet(f'''QSpinBox{{
                                                background: transparent;
                                                border: 4px solid {main.color_lable[main.season]};
                                                border-radius: 10px;
                                                selection-color: black;
                                                selection-background-color: white;
                                                color: {main.color_lable[main.season]}}}''')
        self.quantity_widget.setMaximum(QUANTILY_GROUP)

        self.counting_rating = QRadioButton('Счёт по рейтингу', self)
        self.counting_rating.click()
        self.counting_rating.resize(400, 60)
        self.counting_rating.move(615, 350)
        self.counting_rating.setFont(QFont(FONTNAME, 20))
        self.counting_rating.setStyleSheet(main.style_radiobutton_league)
        self.counting_rating.clicked.connect(main.player.play)

        self.counting_meetings = QRadioButton('Счёт по личным встречам', self)
        self.counting_meetings.resize(400, 60)
        self.counting_meetings.move(615, 444)
        self.counting_meetings.setFont(QFont(FONTNAME, 20))
        self.counting_meetings.setStyleSheet(main.style_radiobutton_league)
        self.counting_meetings.clicked.connect(main.player.play)

        back = QPushButton('', self)
        back.move(50, 50)
        back.resize(100, 100)
        back.setStyleSheet(main.style_back_button)
        back.clicked.connect(main.player.play)
        back.clicked.connect(self.close_leagues)

        self.show()

    def close_leagues(self):
        self.deleteLater()

    def change_quantity(self, index):
        if index == 26:
            self.quantity_widget.setMaximum(QUANTILY_GROUP_ONLY)
        else:
            self.quantity_widget.setMaximum(QUANTILY_GROUP)

    # Сохранение Турнира
    def save_league(self):
        text2 = self.letter_league.currentText() if len(
            self.letter_league.currentText()) == 1 else ''

        type = 2 if text2 == '' else 1

        self.main.title_league = f'{self.title_format.currentText()} {text2}'
        self.main.quantity_group = self.quantity_widget.value()

        quantity = self.main.quantity_group
        check = self.main.cur.execute(f'''SELECT id FROM league
        WHERE title = '{self.main.title_league}' and id_tournament = {self.main.id_tournament}''')

        if len(list(check)) == 0:
            counting = 1 if self.counting_rating.isChecked() else 2
            self.main.cur.execute(f'''INSERT INTO league(title, id_tournament, quantity, 
                            counting, type)
                            SELECT '{self.main.title_league}', id, {self.main.quantity_group}, 
                            {counting}, {type}
                            FROM tournament WHERE id = {self.main.id_tournament}''')
            self.main.id_league = list(self.main.cur.execute(f'''SELECT id FROM league
                    WHERE title = '{self.main.title_league}' and id_tournament = 
                        {self.main.id_tournament}'''))[0][0]
            self.main.con.commit()

            button = QRadioButton(self.main.title_league, self.main.sidebar)
            button.setStyleSheet(self.main.style_radiobutton)
            button.setFont(QFont(FONTNAME, 15))
            button.clicked.connect(self.main.change_league)

            self.main.click_league = 0
            arr_tabs = []
            for i in range(2):
                tab = QTabWidget(parent=self.main)
                tab.move(180, 0)
                tab.resize(1021, 645)
                tab.setMovable(True)
                tab.setTabPosition(QTabWidget.TabPosition.South)
                tab.setStyleSheet(self.main.style_tab)
                if i == 0:
                    tab.show()
                arr_tabs.append(tab)

            self.main.leagues.addWidget(button)

            self.main.array_league.append(
                [button, self.main.id_league, arr_tabs, quantity, [[], [], []], 0, []])

            button.click()
            if self.create_groups.isChecked():
                self.main.make_groups(2)
            self.deleteLater()

        else:
            self.true_input.setText('Название занято')
