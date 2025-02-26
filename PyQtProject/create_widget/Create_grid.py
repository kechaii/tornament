from PyQt6.QtWidgets import QWidget, QPushButton, QSpinBox, QLabel, QRadioButton
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont
from PyQtProject.Const import FONTNAME
from PyQtProject.create_widget.Сhoose_team import Сhoose_team


class Create_grid(QWidget):
    def __init__(self, main, result):
        super(Create_grid, self).__init__(main)

        self.setGeometry(QRect(0, 0, 1200, 675))

        self.main = main
        self.result = result

        background = QLabel('', self)
        background.resize(1200, 675)
        background.setStyleSheet(main.style_background)

        self.create_button = QPushButton('Создать', self)
        self.create_button.move(200, 300)
        self.create_button.resize(216, 80)
        self.create_button.setStyleSheet(main.style_button)
        self.create_button.setFont(QFont(FONTNAME, 18))
        self.create_button.clicked.connect(main.player.play)
        self.create_button.clicked.connect(self.create)

        background_table = QLabel('', self)
        background_table.setStyleSheet(f'background-image: url({main.season}/table_mini.png)')
        if main.season == 'summer':
            background_table.resize(609, 450)
            background_table.move(500, 110)
        else:
            background_table.resize(650, 465)
            background_table.move(495, 90)

        self.true_input = QLabel('', self)
        self.true_input.resize(267, 100)
        self.true_input.move(672, 50)
        self.true_input.setFont(QFont(FONTNAME, 17))
        self.true_input.setStyleSheet(f'''background-image: url({main.season}/background_lable.png);
                                                      color: {main.color_lable[main.season]}''')
        self.true_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        s = sum([len(i) for i in result])
        max_grids = s // 3
        self.min_grids = max(s // 24 if s // 24 * 24 == s else int(s // 24) + 1, 1)

        self.quantity_grid = QSpinBox(self)
        self.quantity_grid.resize(400, 70)
        self.quantity_grid.move(615, 230)
        self.quantity_grid.setMinimum(self.min_grids)
        self.quantity_grid.setMaximum(max_grids)
        self.quantity_grid.setFont(QFont(FONTNAME, 18))
        self.quantity_grid.setStyleSheet(f'''QSpinBox{{
                                                background: transparent;
                                                border: 4px solid {main.color_lable[main.season]};
                                                border-radius: 10px;
                                                selection-color: black;
                                                selection-background-color: white;
                                                color: {main.color_lable[main.season]}}}''')

        arr = [('Автоматически', 330), ('Вручную', 424)]
        self.radio_buttons = []
        for i in arr:
            button = QRadioButton(i[0], self)
            button.resize(400, 60)
            button.move(685, i[1])
            button.setFont(QFont(FONTNAME, 20))
            button.setStyleSheet(main.style_radiobutton_league)
            button.clicked.connect(main.player.play)
            button.clicked.connect(self.set_min)
            self.radio_buttons.append(button)
        self.radio_buttons[0].click()

        back = QPushButton('', self)
        back.move(50, 50)
        back.resize(100, 100)
        back.setStyleSheet(main.style_back_button)
        back.clicked.connect(main.player.play)
        back.clicked.connect(self.close)

    def set_min(self):
        name = self.sender().text()
        if name == 'Вручную':
            if self.min_grids == 1:
                self.quantity_grid.setMinimum(2)
        else:
            self.quantity_grid.setMinimum(self.min_grids)

    def close(self):
        self.deleteLater()

    def create(self):
        for i in range(self.main.array_league[self.main.id_league][2][0].count()):
            if self.main.array_league[self.main.id_league][2][0].tabText(i) == 'Результат':
                index = i
                break
        self.main.array_league[self.main.id_league][2][0].setCurrentIndex(index)

        self.deleteLater()

        widget = Сhoose_team(self.main, self.result, self.quantity_grid.value())
        widget.show()
