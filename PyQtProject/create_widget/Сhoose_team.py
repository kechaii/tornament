from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox, QLineEdit
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont
from PyQtProject.Const import FONTNAME
from PyQtProject.Grid import Grid


class Сhoose_team(QWidget):
    def __init__(self, main, result, q):
        super(Сhoose_team, self).__init__(main)

        self.setGeometry(QRect(0, 0, 1200, 675))

        self.main = main
        self.result = result
        self.q = q

        color = main.color_text_sap_button[main.season]

        self.style_checkbox = f'''QCheckBox {{background: transparent}}
                                                    QCheckBox::indicator {{ 
                                                                width: 95px; height: 92;}}
                                                    QCheckBox::indicator:unchecked {{
                                                                image: none}}
                                                    QCheckBox::indicator:unchecked:hover {{
                                                                image: none}}
                                                    QCheckBox::indicator:unchecked:pressed {{
                                                                image: none}}
                                                    QCheckBox::indicator:checked {{
                                                                image: none}}
                                                    QCheckBox::indicator:checked:hover {{
                                                                image: none}}
                                                    QCheckBox::indicator:checked:pressed {{
                                                                image: none}}
                                                    QCheckBox::hover {{
                                                                background: rgba(0, 0, 255, 100)}}
                                                    QCheckBox::checked {{
                                                                background: rgba(0, 255, 0, 100)}}
                                                    QCheckBox::checked::hover {{
                                                            background: rgba(0, 255, 200, 100)}}'''

        self.grids = [[] for i in range(q)]
        self.id_grid = 0

        down = QLabel('', self)
        down.move(180, 617)
        down.resize(1021, 30)
        down.setStyleSheet('background: rgb(162, 162, 162)')

        self.sidebar = QWidget(parent=self)
        self.sidebar.resize(180, 675)

        background_sidebar = QLabel('', self.sidebar)
        background_sidebar.resize(180, 675)
        background_sidebar.setStyleSheet(f'background-image: url({main.season}/background.jpg)')

        tools_widget = QWidget(self)
        tools_widget.resize(181, 502)
        tools_widget.setStyleSheet(f'background-color: {main.color_lable[main.season]}')

        name_buttons = ['Предыдущая', 'Следующая', 'Cохранить']
        self.groups = []
        self.buttons = []

        for col, i in enumerate(result):
            group = []
            for row, j in enumerate(i):
                checkbox = QCheckBox(self)
                checkbox.resize(95, 92)
                checkbox.move(250 + col * 95, 64 + row * 92)
                checkbox.setStyleSheet(self.style_checkbox)
                checkbox.clicked.connect(self.set_grid)
                group.append([j, checkbox, row + 1])
            self.groups.append(group)

        self.number_grid = QLineEdit('1 Сетка', parent=tools_widget)
        self.number_grid.resize(135, 50)
        self.number_grid.move(22, 42)
        self.number_grid.setFont(QFont(FONTNAME, 15))
        self.number_grid.setStyleSheet(f'''QLineEdit{{
                                                background: transparent;
                                                border: 4px solid {color};
                                                border-radius: 10px;
                                                selection-color: black;
                                                selection-background-color: white;
                                                color: {color}}}''')
        self.number_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.number_grid.setMaxLength(15)
        self.number_grid.textChanged.connect(self.changed_name)

        self.home = QPushButton('', parent=self.sidebar)
        self.home.resize(100, 100)
        self.home.move(40, 530)
        self.home.setStyleSheet(f'''QPushButton {{ 
                                                background-image: url({main.season}/home.png);
                                                border-radius: 10px;}}
                                                QPushButton:hover {{
                                                background-image: url({main.season}/home_dark.png)}}
                                                QPushButton:pressed {{
                                                background-image: url({main.season}/home.png)
                                                            }}''')
        self.home.clicked.connect(main.player.play)
        self.home.clicked.connect(self.close)

        self.quantity = QLabel('0 Команд', parent=tools_widget)
        self.quantity.resize(135, 50)
        self.quantity.move(22, 42 + 92)
        self.quantity.setFont(QFont(FONTNAME, 11))
        self.quantity.setStyleSheet(f'''QLabel{{
                                                background: transparent;
                                                selection-color: black;
                                                selection-background-color: white;
                                                color: {color}}}''')
        self.quantity.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.excepts = QLabel('Ошибок нет', parent=down)
        self.excepts.resize(1021, 30)
        self.excepts.setFont(QFont('Arial', 13))
        self.excepts.setStyleSheet(f'''QLabel{{
                                                    background: transparent;
                                                    selection-color: black;
                                                    selection-background-color: white;
                                                    color: black}}''')
        self.excepts.setAlignment(Qt.AlignmentFlag.AlignCenter)

        y = 42 + 92 + 92
        for i in name_buttons:
            button = QPushButton(i, parent=tools_widget)
            button.resize(135, 50)
            button.move(22, y)
            button.setStyleSheet(main.style_tools_button)
            button.clicked.connect(main.player.play)
            self.buttons.append(button)
            y += 92

        self.buttons[0].clicked.connect(self.back)
        self.buttons[1].clicked.connect(self.next)
        self.buttons[2].clicked.connect(self.save)

        self.leagues_widget = QWidget(self.sidebar)
        self.leagues_widget.resize(181, 410)

        self.leagues = QVBoxLayout(self.leagues_widget)
        self.leagues.setContentsMargins(30, 0, 0, 0)
        self.leagues.setSpacing(7)

        self.name_grid = [f'{i + 1} Сетка' for i in range(q)]

    def close(self):
        self.deleteLater()

    def back(self):
        if self.id_grid != 0:
            self.id_grid -= 1
            self.change_grid(self.id_grid)

    def next(self):
        if self.id_grid != self.q - 1:
            self.id_grid += 1
            self.change_grid(self.id_grid)

    def changed_name(self):
        self.name_grid[self.id_grid] = self.number_grid.text()

    def change_grid(self, id):
        self.number_grid.setText(self.name_grid[id])
        self.set_quantity(id)
        for en, i in enumerate(self.grids):
            for j in i:
                if en == id and j[1].isChecked():
                    j[1].setStyleSheet(self.style_checkbox)
                    j[1].setEnabled(True)
                else:
                    j[1].setStyleSheet(f'''QCheckBox {{background: transparent}}
                                                    QCheckBox::indicator {{ 
                                                                width: 95px; height: 92;}}
                                                    QCheckBox::indicator:checked {{
                                                                image: none}}
                                                    QCheckBox::checked {{
                                                            background: rgba(255, 0, 0, 100)}}''')
                    j[1].setEnabled(False)

    def set_quantity(self, id):
        name = {1: 'Команда', 2: 'Команды', 3: 'Команды',
                4: 'Команды'}
        n = len(self.grids[id])
        s = name[1] if n % 10 == 1 else 'Команд'
        self.quantity.setText(f'{len(self.grids[id])} {name[n] if n in name else s}')

    def set_grid(self):
        box = self.sender()
        for i in self.groups:
            for j in i:
                if j[1] == box:
                    if j[1].isChecked():
                        self.grids[self.id_grid].append(j)
                    else:
                        self.grids[self.id_grid].remove(j)
                    self.set_quantity(self.id_grid)

    def set_excepts(self, id, s):
        if s == 'm':
            s = f'В сетке №{id} слишком мало команд!'
        elif s == 'b':
            s = f'В сетке №{id} слишком много команд!'
        else:
            s = 'Не все команды были выбраны!'
        self.excepts.setText(s)

    def save(self):
        bools = 1
        for en, i in enumerate(self.grids):
            if 3 <= len(i) <= 24:
                self.excepts.setText('Ошибок нет')
            elif 3 > len(i):
                self.set_excepts(en + 1, 'm')
                bools = 0
                break
            elif 24 < len(i):
                self.set_excepts(en + 1, 'b')
                bools = 0
                break
        su = 0
        re_su = 0
        for i in self.grids:
            su += len(i)
        for i in self.result:
            re_su += len(i)
        if su != re_su:
            self.set_excepts(0, 'v')
            bools = 0
        if bools:
            for en, i in enumerate(self.grids):
                tab = self.main.array_league[self.main.id_league][2][1]
                tab.addTab(Grid(i, 2, self.main), self.name_grid[en])
            self.deleteLater()
