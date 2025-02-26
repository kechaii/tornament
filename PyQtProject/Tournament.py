from random import shuffle
from PyQt6.QtWidgets import QWidget, QPushButton, QTabWidget, QCheckBox, \
    QComboBox, QLabel, QRadioButton, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import sqlite3
from Const import FONTNAME, NAME_LETTER, FORMAT_GAME, FORMAT_GROUP, FORMAT_GROUP_ONLY
from Table import Table
from Result import Result
from Grid import Grid
from PyQtProject.create_widget.Create_league import Create_league
from PyQtProject.create_widget.Create_grid import Create_grid


# Класс турнира
class Tournament(QWidget):
    def __init__(self, season, color_text, media, valume, id):
        super().__init__()

        self.setGeometry(QRect(0, 0, 1200, 675))

        self.con = sqlite3.connect('Tournaments.sqlite')
        self.cur = self.con.cursor()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(valume)
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(media)

        self.season = season

        self.colors_text = color_text
        self.color_lable = {'summer': '#EDCBA5', 'winter': '#09525C'}
        self.color_text_sap_button = {'summer': '#9f4331', 'winter': '#3092b9'}
        self.color_league = {'summer': '#9f4331', 'winter': '#09525C'}
        self.color_green = {'summer': '#59BA7A', 'winter': '#39B950'}

        self.style_button = f'''QPushButton {{ background-image: url({self.season}/button.png);
                                                          border-radius: 10px;
                                                          color: {self.colors_text[self.season]}}}
                                           QPushButton:hover {{
                                                          background-image: 
                                                          url({self.season}/button_dark.png)}}
                                           QPushButton:pressed {{
                                                          background-image: 
                                                          url({self.season}/button.png)}}'''
        self.style_radiobutton = f'''QRadioButton {{color: 
                                            {self.color_league[self.season]}}}
                                            QRadioButton::indicator::unchecked {{
                                                   image: url({self.season}/off_radio_button.png);}}
                                            QRadioButton::indicator:unchecked:hover {{
                                              image: url({self.season}/off_radio_button_dark.png);}}
                                            QRadioButton::indicator:unchecked:pressed {{
                                                  image: url({self.season}/off_radio_button.png);}}
                                            QRadioButton::indicator::checked {{
                                                    image: url({self.season}/on_radio_button.png)}}
                                            QRadioButton::indicator:checked:hover {{
                                              image: url({self.season}/on_radio_button_dark.png);}}
                                            QRadioButton::indicator:checked:pressed {{
                                                image: url({self.season}/on_radio_button.png);}}'''
        self.style_radiobutton_league = f'''QRadioButton {{color: 
                                                {self.color_lable[self.season]}}}
                                            QRadioButton::indicator::unchecked {{
                                               image: url({self.season}/off_radio_button.png);}}
                                            QRadioButton::indicator:unchecked:hover {{
                                           image: url({self.season}/off_radio_button_dark.png);}}
                                            QRadioButton::indicator:unchecked:pressed {{
                                                  image: url({self.season}/off_radio_button.png);}}
                                            QRadioButton::indicator::checked {{
                                                  image: url({self.season}/on_radio_button.png)}}
                                            QRadioButton::indicator:checked:hover {{
                                            image: url({self.season}/on_radio_button_dark.png);}}
                                            QRadioButton::indicator:checked:pressed {{
                                             image: url({self.season}/on_radio_button.png);}}'''
        self.style_checkbox_on_table = f'''QCheckBox {{color: {self.color_lable[self.season]}}}
                            QCheckBox::indicator:unchecked {{
                                        image: url({self.season}/off_check_box.png);}}
                            QCheckBox::indicator:unchecked:hover {{
                                        image: url({self.season}/off_check_box_dark.png);}}
                            QCheckBox::indicator:unchecked:pressed {{
                                        image: url({self.season}/off_check_box.png)}}
                            QCheckBox::indicator:checked {{
                                        image: url({self.season}/on_check_box.png);}}
                            QCheckBox::indicator:checked:hover {{
                                        image: url({self.season}/on_check_box_dark.png);}}
                            QCheckBox::indicator:checked:pressed {{
                                        image: url({self.season}/on_check_box_dark.png);}}'''
        self.style_checkbox = f'''QCheckBox {{color: {self.color_text_sap_button[self.season]}}}
                                    QCheckBox::indicator:unchecked {{
                                                image: url({self.season}/off_check_box.png);}}
                                    QCheckBox::indicator:unchecked:hover {{
                                                image: url({self.season}/off_check_box_dark.png);}}
                                    QCheckBox::indicator:unchecked:pressed {{
                                                image: url({self.season}/off_check_box.png)}}
                                    QCheckBox::indicator:checked {{
                                                image: url({self.season}/on_check_box.png);}}
                                    QCheckBox::indicator:checked:hover {{
                                                image: url({self.season}/on_check_box_dark.png);}}
                                    QCheckBox::indicator:checked:pressed {{
                                            image: url({self.season}/on_check_box_dark.png);}}'''
        self.style_background = f"""background-image : 
                                                url({self.season}/main_background.jpg)"""
        self.style_tools_button = f'''QPushButton {{
                                    background-image: url({self.season}/button_on_tools.png);
                                    color: {self.colors_text[self.season]};
                                    font: 10pt "Groboldov";
                                    border-radius: 10px;}}
                                QPushButton:hover {{
                                    background-image: url({self.season}/button_on_tools_dark.png)}}
                                QPushButton:pressed {{
                                    background-image: url({self.season}/button_on_tools.png)
                                }}'''

        self.style_tab = f'''QTabBar::tab {{
                                            border-top-left-radius: 0px;
                                            border-top-right-radius: 0px;
                                            border-bottom-left-radius: 13px;
                                            background-color: rgb(162, 162, 162);
                                            min-width: 11ex;
                                            border-bottom-right-radius: 13px;}}'''
        self.style_combobox = f'''QComboBox{{
                                                background: transparent;
                                                border: 4px solid {self.color_lable[self.season]};
                                                border-radius: 10px;
                                                selection-color: black;
                                                selection-background-color: white;
                                                color: {self.color_lable[self.season]}}}'''
        self.style_back_button = f'''QPushButton {{ background-image: url({self.season}/back.png);
                                                                  border-radius: 10px;
                                                            color: {self.colors_text[self.season]}}}
                                                   QPushButton:hover {{
                                                                  background-image: 
                                                                  url({self.season}/back_dark.png)}}
                                                   QPushButton:pressed {{
                                                                  background-image: 
                                                                  url({self.season}/back.png)}}'''

        self.sidebar = QWidget(parent=self)
        self.sidebar.resize(180, 675)

        background_sidebar = QLabel('', self.sidebar)
        background_sidebar.resize(180, 675)
        background_sidebar.setStyleSheet(f'background-image: url({self.season}/background.jpg)')

        self.tools_button = QPushButton('', parent=self.sidebar)
        self.tools_button.resize(100, 100)
        self.tools_button.move(40, 530)
        self.tools_button.setStyleSheet(f'''QPushButton {{ 
                                                background-image: url({self.season}/tools.png);
                                                border-radius: 10px;}}
                                                QPushButton:hover {{
                                                background-image: url({self.season}/tools_dark.png)}}
                                                QPushButton:pressed {{
                                                background-image: url({self.season}/tools.png)
                                                }}''')
        self.tools_button.clicked.connect(self.player.play)
        self.tools_button.clicked.connect(self.tools)

        self.what_tools = 0

        self.arr_tools_widget = []

        for i in range(2):
            tools_widget = QWidget(self)
            tools_widget.resize(181, 502)
            tools_widget.setStyleSheet(f'background-color: {self.color_lable[self.season]}')
            tools_widget.hide()
            self.arr_tools_widget.append(tools_widget)

        name_buttons = ['Добавить Лигу', 'Добавить Группу', 'Результат', 'Создать Сетку',
                        'Показать Сетки']
        name_buttons_grid = ['Наазд', 'Редактировать', 'Формат', 'Результат', 'Показать Группы']
        self.buttons = []
        for i in range(2):
            y = 42
            for name in name_buttons if i == 0 else name_buttons_grid:
                button = QPushButton(name, parent=self.arr_tools_widget[i])
                button.resize(135, 50)
                button.move(22, y)
                button.setStyleSheet(self.style_tools_button)
                button.clicked.connect(self.player.play)
                self.buttons.append(button)

                y += 92

        self.buttons[0].clicked.connect(self.add_league)
        self.buttons[1].clicked.connect(self.add_group)
        self.buttons[2].clicked.connect(self.result)
        self.buttons[3].clicked.connect(self.create_grid)
        self.buttons[4].clicked.connect(self.show_grid)
        self.buttons[5].clicked.connect(self.back)
        self.buttons[6].clicked.connect(self.edit)
        self.buttons[7].clicked.connect(self.format)
        self.buttons[8].clicked.connect(self.result_grid)
        self.buttons[9].clicked.connect(self.show_groups)

        self.leagues_widget = QWidget(self.sidebar)
        self.leagues_widget.resize(181, 410)

        self.leagues = QVBoxLayout(self.leagues_widget)
        self.leagues.setContentsMargins(30, 0, 0, 0)
        self.leagues.setSpacing(7)

        self.background_table = QLabel('', self)
        self.background_table.resize(1021, 675)
        self.background_table.move(180, 0)
        self.background_table.setStyleSheet('background-color: white')
        self.background_table.show()

        # Список содержащий id Лиги, TabWidget для лиги, группы лиги
        self.array_league = []

        # Открытие турнира
        self.open(id)

    # Открытие sidebar
    def tools(self):
        if self.arr_tools_widget[self.what_tools].isVisible():
            self.arr_tools_widget[self.what_tools].hide()
        else:
            self.arr_tools_widget[self.what_tools].show()

    # Открытие турнира
    def open(self, id):
        self.id_tournament = id
        self.title_tournament, self.quantity_league = list(self.cur.execute(f'''SELECT title, 
                                            quantity FROM tournament
                                                    WHERE id = {id}'''))[0]
        id_leagues = [i[0] for i in self.cur.execute(f'''SELECT id FROM league
                                          WHERE id_tournament = {id}''')]
        for i in id_leagues:
            title = list(self.cur.execute(f'SELECT title FROM league WHERE id = {i}'))[0][0]

            button = QRadioButton(title, self.sidebar)
            button.setStyleSheet(self.style_radiobutton)
            button.setFont(QFont(FONTNAME, 15))
            button.clicked.connect(self.player.play)
            button.clicked.connect(self.change_league)

            self.click_league = 0

            arr_tabs = []
            for j in range(2):
                tab = QTabWidget(parent=self)
                tab.move(180, 0)
                tab.resize(1021, 645)
                tab.setMovable(True)
                tab.setTabPosition(QTabWidget.TabPosition.South)
                tab.setStyleSheet(self.style_tab)
                if i == 0:
                    tab.show()
                arr_tabs.append(tab)
            arr_tabs[1].currentChanged.connect(self.cur_grid)
            quantity = list(self.cur.execute(f'''SELECT quantity FROM league
                                            WHERE id = {i}'''))[0][0]
            id_groups = [j[0] for j in self.cur.execute(f'''SELECT id FROM groupp
                                          WHERE id_league = {i}''')]
            arr_groups = []
            arr_surname_name = [[], [], []]
            for j in id_groups:
                name = list(self.cur.execute(f'''SELECT title FROM groupp
                                                 WHERE id = {j}'''))[0][0]
                format = list(self.cur.execute(f'''SELECT format FROM groupp
                                                 WHERE id = {j}'''))[0][0]
                quantity_team = list(self.cur.execute(f'''SELECT quantity FROM groupp
                                                 WHERE id = {j}'''))[0][0]

                teams = []
                id_teams = [j[0] for j in self.cur.execute(f'''SELECT id FROM team
                                          WHERE id_group = {j}''')]
                for k in id_teams:
                    id_players = list(self.cur.execute(f'''SELECT id_1_player, id_2_player FROM
                                                               team WHERE id = {k}'''))[0]
                    player_1 = list(self.cur.execute(f'''SELECT surname, name FROM player
                                                         WHERE id = {id_players[0]}'''))[0]
                    player_2 = list(self.cur.execute(f'''SELECT surname, name FROM player
                                                         WHERE id = {id_players[1]}'''))[0]
                    handicap, sign = list(self.cur.execute(f'''SELECT handicap, sign FROM team
                                                         WHERE id = {k}'''))[0]

                    arr_surname_name[0].append(f'{player_1[0]} {player_1[1]}')
                    arr_surname_name[0].append(f'{player_2[0]} {player_2[1]}')
                    arr_surname_name[1].append(f'{player_1[0]} {player_2[0]}')
                    arr_surname_name[2].append((handicap, sign))

                    teams.append((player_1, player_2, (handicap, sign)))
                arr_tabs[0].addTab(Table(quantity_team, name, format, teams, j, 'open'), name)
                arr_groups.append((j, name, teams))

            self.array_league.append([button, i, arr_tabs, quantity, arr_surname_name, 0,
                                      arr_groups])
            self.leagues.addWidget(button)
            button.click()

    # Добавление Лиги в открытый турнир
    def add_league(self):
        if self.leagues.count() + 1 <= self.quantity_league:
            self.make_league()

    # Добавление Группы в открытую лигу
    def add_group(self):
        if len(self.array_league) != 0:
            if self.click_league and self.array_league[self.id_league][3] > len(
                    self.array_league[self.id_league][-1]):
                self.make_groups()

    # Результаты группового этапа
    def result(self):
        if len(self.array_league) != 0:
            if self.click_league and self.array_league[self.id_league][3] == len(
                    self.array_league[self.id_league][-1]):
                tab = self.array_league[self.id_league][2][0]
                for i in range(tab.count()):
                    if tab.tabText(i) == 'Результат':
                        tab.removeTab(i)
                        break
                result = Result(self.array_league[self.id_league], self.season)
                tab.addTab(result, 'Результат')
                self.array_league[self.id_league][2][0].setCurrentIndex(tab.count() - 1)
                self.array_league[self.id_league][5] = result.iscorrect()

    # Создание сетки
    def create_grid(self):
        if len(self.array_league) != 0:
            result = self.array_league[self.id_league][5]
            if result != 0:
                if self.type == 2:
                    c = Create_grid(self, result)
                    c.show()
                else:
                    tab = self.array_league[self.id_league][2][1]
                    tab.addTab(Grid(result, 1, self), 'Сетка')

    def edit(self):
        grid = self.array_league[self.id_league][2][1].currentWidget()
        if grid:
            grid.edit()

    def back(self):
        grid = self.array_league[self.id_league][2][1].currentWidget()
        if grid:
            grid.back()

    def result_grid(self):
        grid = self.array_league[self.id_league][2][1].currentWidget()
        if grid:
            grid.result()

    def format(self):
        grid = self.array_league[self.id_league][2][1].currentWidget()
        if grid:
            grid.format_team()

    def cur_grid(self):
        grid = self.array_league[self.id_league][2][1].currentWidget()
        if grid:
            s = grid.edit_bool
            if s:
                color = self.color_green[self.season]
            else:
                color = self.colors_text[self.season]
            self.buttons[6].setStyleSheet(f'''{self.style_tools_button}
                                            QPushButton {{
                                    background-image: url({self.season}/button_on_tools.png);
                                    color: {color};
                                    font: 10pt "Groboldov";
                                    border-radius: 10px;}}''')

    # Создание Лиги
    def make_league(self):
        c = Create_league(self)
        c.show()

    # Смена Турнира
    def change_league(self):
        for i in self.array_league:
            i[2][0].hide()
            i[2][1].hide()
        self.click_league = 0
        e = 1
        for en, i in enumerate(self.array_league):
            if i[0].isChecked():
                self.id_league = en
                e = 0
                self.type = list((self.cur.execute(f'''SELECT type FROM league
                                    WHERE id = {self.array_league[self.id_league][1]}''')))[0][0]
                i[2][self.what_tools].show()
                self.click_league = 1
                break
        if e or self.array_league[self.id_league][2][0].count() == 0:
            self.background_table.setStyleSheet('background: white')
        else:
            self.background_table.setStyleSheet('background: rgb(162, 162, 162)')

    # Создание Групп
    def make_groups(self, k=1):
        self.parameters_groups = QWidget(parent=self)
        self.parameters_groups.setGeometry(QRect(0, 0, 1200, 675))

        self.teams_groups = QWidget(parent=self)
        self.teams_groups.setGeometry(QRect(0, 0, 1200, 675))

        widgets = [self.parameters_groups, self.teams_groups]

        for i in widgets:
            background = QLabel('', i)
            background.resize(1200, 675)
            background.setStyleSheet(self.style_background)

            background_table = QLabel('', i)
            background_table.setStyleSheet(f'background-image: url({self.season}/table_mini.png)')

            if self.season == 'summer':
                background_table.resize(609, 450)
                background_table.move(500, 110)
            else:
                background_table.resize(650, 465)
                background_table.move(495, 90)

        for i in widgets:
            button_save_groups = QPushButton('Сохранить' if i == self.teams_groups else 'Выбрать',
                                             i)
            button_save_groups.move(200, 300)
            button_save_groups.resize(216, 80)
            button_save_groups.setFont(QFont(FONTNAME, 18))
            button_save_groups.setStyleSheet(self.style_button)
            button_save_groups.clicked.connect(self.player.play)
            if i == self.teams_groups:
                button_save_groups.clicked.connect(self.check_true_input)
            else:
                button_save_groups.clicked.connect(self.go_team)

        quantity_group = self.array_league[self.id_league][3]
        formats = FORMAT_GROUP_ONLY if self.type == 2 else FORMAT_GROUP
        if k == 1:
            quantity_group = 1
        self.team = QComboBox(self.parameters_groups)
        self.team.addItems(formats[quantity_group])
        self.team.setStyleSheet(self.style_combobox)
        self.team.setFont(QFont(FONTNAME, 16))

        self.format = QComboBox(self.parameters_groups)
        self.format.addItems(FORMAT_GAME)
        self.format.setStyleSheet(self.style_combobox)
        self.format.setFont(QFont(FONTNAME, 16))

        self.true_input = QLabel('', self.teams_groups)
        self.true_input.resize(267, 100)
        self.true_input.move(672, 50)
        self.true_input.setFont(QFont(FONTNAME, 13))
        self.true_input.setStyleSheet(f'''background-image: url({self.season}/background_lable.png);
                                      color: {self.color_lable[self.season]}''')
        self.true_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.list_team = QTextEdit(self.teams_groups)
        self.list_team.resize(520, 344)
        self.list_team.move(550, 160)
        self.list_team.setFont(QFont(FONTNAME, 13))
        self.list_team.setStyleSheet(f'''QTextEdit {{ background-color: transparent; 
                                                color: {self.color_lable[self.season]}; 
                                                border: 0px solid #ccc; 
                                                selection-background-color: white;
                                                selection-color: black}}
                                         QScrollBar:vertical {{
                                                background: transparent;
                                                width: 15px;
                                                margin: 0px 3px 0px 3px;
                                                border-radius: 4px;
                                            }}
                                QScrollBar::handle:vertical {{
                                                background-color: {self.color_lable[self.season]};                    
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
                                            }}''')

        self.the_draw = QCheckBox('Жеребьевка', self.parameters_groups)
        self.the_draw.setFont(QFont(FONTNAME, 20))
        self.the_draw.setStyleSheet(self.style_checkbox_on_table)
        self.the_draw.clicked.connect(self.player.play)

        for i in range(2):
            back = QPushButton('', widgets[i])
            back.move(50, 50)
            back.resize(100, 100)
            back.setStyleSheet(self.style_back_button)
            back.clicked.connect(self.player.play)
            if i == 0:
                back.clicked.connect(self.close_param)
            else:
                back.clicked.connect(self.close_team)

        if self.season == 'summer':
            self.team.resize(510, 60)
            self.team.move(550, 180)

            self.the_draw.resize(400, 60)
            self.the_draw.move(690, 350)

            self.format.resize(510, 60)
            self.format.move(550, 275)
        else:
            self.team.resize(500, 60)
            self.team.move(570, 180)

            self.the_draw.resize(400, 60)
            self.the_draw.move(710, 350)

            self.format.resize(500, 60)
            self.format.move(570, 275)

        self.parameters_groups.show()

    def go_team(self):
        self.teams_groups.show()
        self.parameters_groups.hide()

    def close_param(self):
        self.parameters_groups.deleteLater()
        self.teams_groups.deleteLater()

    def close_team(self):
        self.teams_groups.hide()
        self.parameters_groups.show()

    # Проверка введенных команд
    def check_true_input(self):
        arr_league = self.array_league[self.id_league][4]
        quantity = [int(i) for i in self.team.currentText().split('-')]
        arr_team = [i for i in self.list_team.toPlainText().split('\n') if i != '']
        arr_players, arr_surnames, arr_handicap = [], [], []
        try:
            if sum(quantity) > len(arr_team):
                raise TypeError(f'"{len(arr_team)}"\nСлишком мало команд!')
            if sum(quantity) < len(arr_team):
                raise TypeError(f'"{len(arr_team)}"\nСлишком много команд!')
            for en, i in enumerate(arr_team):
                team = i.split()

                if len(team) != 6 or team[2] != '/':
                    raise TypeError(f'Строка: {en + 1}\nНекорректный ввод!')

                if team[0] == team[3] and team[1] == team[4]:
                    raise TypeError(f'Строка: {en + 1}\nОдинаковые участники!')

                if (team[0] + ' ' + team[3] in arr_surnames or
                        team[0] + ' ' + team[3] in arr_league[1]):
                    raise TypeError(f'Строка: {en + 1}\nФамилии уже встречались!')

                if (team[0] + ' ' + team[1] in arr_players or
                        team[0] + ' ' + team[1] in arr_league[0]):
                    raise TypeError(f'Строка: {en + 1}\nПервый участник уже записан!')

                if (team[3] + ' ' + team[4] in arr_players or
                        team[3] + ' ' + team[4] in arr_league[0]):
                    raise TypeError(f'Строка: {en + 1}\nВторой участник уже записан!')

                handicap = team[5]
                if handicap != '0':
                    if not handicap[1:].isdigit() or handicap[0] not in ['+', '-']:
                        raise TypeError(f'Строка: {en + 1}\nНеправильный гандикап!')
                    if int(handicap) >= 20:
                        raise TypeError(f'Строка: {en + 1}\nГандикап слишком большой!')
                    if int(handicap) <= -20:
                        raise TypeError(f'Строка: {en + 1}\nГандикап слишком маленький!')

                for j in ['W', 'L', '-']:
                    if j in team[0] or j in team[1] or j in team[3] or j in team[4]:
                        raise TypeError(f'Строка: {en + 1}\nИспользован символ: «{j}»!')

                arr_players.extend([team[0] + ' ' + team[1], team[3] + ' ' + team[4]])
                arr_surnames.append(team[0] + ' ' + team[3])

                sign = 0
                if handicap != '0':
                    sign = 1 if handicap[0] == '+' else -1
                    handicap = handicap[1:]

                arr_handicap.append((handicap, sign))

        except TypeError as error:
            self.true_input.setText(str(error))
            return 0
        if len(arr_team) != 0:
            self.array_league[self.id_league][4][0].extend(arr_players)
            self.array_league[self.id_league][4][1].extend(arr_surnames)
            self.array_league[self.id_league][4][2].extend(arr_handicap)
            self.save_groups(arr_team, quantity)
        else:
            self.true_input.setText('0 это Слишком мало команд!')

    # Сохранение Групп
    def save_groups(self, arr_team, arr):
        if self.the_draw.isChecked():
            shuffle(arr_team)
        q = 0
        size_group = len(self.array_league[self.id_league][-1])
        for i in range(len(arr)):
            name = f'Группа {NAME_LETTER[i + size_group]}'
            self.cur.execute(f"""INSERT INTO groupp(title, id_league, format, quantity) 
                                SELECT '{name}', id, 
                                '{self.format.currentText()}', {arr[i]} FROM league
                                WHERE id = {self.array_league[self.id_league][1]}""")
            self.con.commit()
            id_group = list(self.cur.execute(f"""SELECT id FROM groupp
                                                 WHERE title = '{name}' and id_league = 
                                                 {self.array_league[self.id_league][1]}"""))[0][0]
            teams = []
            for j in range(arr[i]):
                players = [(arr_team[q].split()[0], arr_team[q].split()[1]),
                           (arr_team[q].split()[3], arr_team[q].split()[4])]

                handicap = arr_team[q].split()[5]
                sign = 0
                if handicap != '0':
                    sign = 1 if handicap[0] == '+' else -1
                    handicap = handicap[1:]

                teams.append(((players[0][0], players[0][1]),
                              (players[1][0], players[1][1]), (handicap, sign)))

                q += 1
                for k in players:
                    if len(list(self.cur.execute(f"""SELECT id FROM player
                                    WHERE name = '{k[1]}' and surname = '{k[0]}'"""))) == 0:
                        self.cur.execute(f"""INSERT INTO player(name, surname)
                                                VALUES ('{k[1]}', '{k[0]}')""")
                        self.con.commit()
                self.cur.execute(f"""INSERT INTO team(id_1_player, id_2_player, id_group, 
                                        handicap, sign)
                                         VALUES(
                                         (SELECT id FROM player
                                          WHERE name = '{players[0][1]}' and 
                                          surname = '{players[0][0]}'),
                                         (SELECT id FROM player
                                          WHERE name = '{players[1][1]}' and 
                                          surname = '{players[1][0]}'),
                                         (SELECT id FROM groupp
                                          WHERE title = '{name}' 
                                          and id_league = 
                                          {self.array_league[self.id_league][1]}), {handicap}, 
                                            {sign})""")
                self.con.commit()
            self.array_league[self.id_league][-1].append((id_group, name, teams))
            self.array_league[self.id_league][2][0].addTab(
                Table(arr[i], name, self.format.currentText(), teams, id_group, 'create'),
                name)
        self.parameters_groups.deleteLater()
        self.teams_groups.deleteLater()
        if not self.array_league[self.id_league][0].isChecked():
            self.array_league[self.id_league][0].click()
        else:
            self.background_table.setStyleSheet('background: rgb(162, 162, 162)')

    def show_grid(self):
        if self.array_league:
            if self.array_league[self.id_league][2][1].count() != 0:
                self.array_league[self.id_league][2][1].show()
                self.array_league[self.id_league][2][0].hide()
                self.arr_tools_widget[0].hide()
                self.arr_tools_widget[1].show()
                self.what_tools = 1

    def show_groups(self):
        self.array_league[self.id_league][2][0].show()
        self.array_league[self.id_league][2][1].hide()
        self.arr_tools_widget[1].hide()
        self.arr_tools_widget[0].show()
        self.what_tools = 0
