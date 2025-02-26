from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import QRect
from PyQtProject.create_widget.Drag import DragButton


# Класс сетки
class Grid(QWidget):
    def __init__(self, result, n, main):
        super().__init__()
        self.setGeometry(QRect(0, 0, 1021, 645))

        self.edit_bool = 0
        self.queue_game = []
        self.main = main

        self.rating = []
        if n == 1:
            q = max([len(i) for i in result])
            for i in range(q):
                ar = [j[i] for j in result if len(j) > i]
                self.rating.extend(
                    [[j[0], j[-1]] for j in reversed(sorted(ar, key=lambda x: (x[2], x[1])))])
        else:
            arr = [(i[0][0], i[2], i[0][2], i[0][1]) for i in result]
            arr = list(sorted(arr, key=lambda x: (-x[1], x[2], x[3])))[::-1]
            self.rating = [[i[0], i[-1]] for i in arr]
        quantity = len(self.rating)

        grids = [0, 8, 12, 16, 24]

        # Координаты для всех кнопок
        self.coords = {8: {1: [(40, 17), (40, 135)], 2: [(40, 169), (40, 287)],
                           3: [(40, 321), (40, 438)], 4: [(40, 473), (40, 590)],
                           5: [(210, 55), (210, 245)], 6: [(210, 359), (210, 549)],
                           7: [(880, 3), (880, 153)], 8: [(880, 440), (880, 588)],
                           9: [(712, 56), (757, 246)], 10: [(757, 360), (712, 550)],
                           11: [(390, 122), (562, 162)], 12: [(390, 435), (562, 473)],
                           13: [(415, 283), (545, 283)], 14: [(415, 352), (545, 352)]},

                       12: {1: [(40, 45), (40, 140)], 2: [(40, 170), (40, 265)],
                            3: [(40, 295), (40, 390)], 4: [(40, 423), (40, 518)],
                            5: [(180, 10), (180, 102)], 6: [(180, 143), (180, 234)],
                            7: [(180, 321), (180, 412)], 8: [(180, 460), (180, 550)],
                            9: [(894, 104), (894, 196)], 10: [(894, 223), (894, 315)],
                            11: [(894, 395), (894, 486)], 12: [(894, 512), (894, 568)],
                            13: [(745, 128), (745, 300)], 14: [(739, 416), (739, 590)],
                            15: [(307, 32), (316, 200)], 16: [(328, 345), (324, 522)],
                            17: [(690, 29), (616, 217)], 18: [(674, 345), (609, 518)],
                            19: [(418, 98), (538, 138)], 20: [(428, 410), (551, 452)],
                            21: [(428, 260), (560, 260)], 22: [(428, 326), (560, 326)]},
                       16: [], 24: []}

        # Имена для всех кнопок
        self.name = {8: {1: [1, 8], 2: [4, 5], 3: [3, 6], 4: [2, 7],
                         5: ['W1', 'W2'], 6: ['W3', 'W4'], 7: ['L4', 'L2'], 8: ['L3', 'L1'],
                         9: ['W7', 'L6'], 10: ['L5', 'W8'], 11: ['W5', 'W9'], 12: ['W6', 'W10'],
                         13: ['L11', 'L12'], 14: ['W11', 'W12']},
                     12: {1: [8, 9], 2: [5, 12], 3: [6, 11], 4: [7, 10], 5: [1, 'W1'], 6: [4, 'W2'],
                          7: ['W3', 3], 8: ['W4', 2], 9: ['L5', 'L4'], 10: ['L6', 'L3'],
                          11: ['L7', 'L2'], 12: ['L8', 'L1'], 13: ['W9', 'W10'], 14: ['W11', 'W12'],
                          15: ['W5', 'W6'], 16: ['W7', 'W8'],
                          17: ['L16', 'W13'], 18: ['L15', 'W14'], 19: ['W15', 'W17'],
                          20: ['W16', 'W18'], 21: ['L19', 'L20'], 22: ['W19', 'W20']},
                     16: {},
                     24: {}}
        self.name_sub = self.name.copy()
        self.buttons = {}
        self.text_button = {}

        for en, i in enumerate(grids[1:]):
            if grids[en] < quantity <= i:
                self.create_grid(i)
                break

    # Создание сетки
    def create_grid(self, num):

        self.grid = QLabel('', self)
        self.grid.resize(1021, 645)
        self.num_grid = num
        if num == 8:
            self.grid.move(0, -10)
        self.grid.setStyleSheet(f'background-image: url(grid_im/grid_{num}.jpg)')

        for i in self.name[num].keys():
            self.buttons[i] = []
            self.text_button[i] = []
            for j in range(2):
                name = str(self.name[num][i][j])
                if name.isdigit():
                    if int(name) <= len(self.rating):
                        team = self.rating[int(name) - 1][0].split()[0]
                        group = self.rating[int(name) - 1][1].split()[1]
                    else:
                        team = '--'
                        group = ''
                    button = DragButton(team, self)
                else:
                    button = DragButton(name, self)
                button.setedit(0)
                button.resize(100, 30)
                coord = self.coords[num][i][j]
                button.move(coord[0], coord[1])
                if button.text()[0] in ['W', 'L', '-']:
                    button.setStyleSheet('background: transparent')
                    button.blockSignals(True)
                button.clicked.connect(self.click_button)
                self.buttons[i].append(button)
                self.text_button[i].append(group)
        self.check()

    # Нажатие на одну из команд
    def click_button(self):
        if not self.edit_bool:
            but = self.sender()
            for i in self.buttons.keys():
                if but in self.buttons[i]:
                    wi = lo = 0
                    if but == self.buttons[i][0] and not self.buttons[i][1].signalsBlocked():
                        lo = 1
                    elif but == self.buttons[i][1] and not self.buttons[i][0].signalsBlocked():
                        wi = 1
                    if wi != 0 or lo != 0:
                        win, lose = self.buttons[i][wi].text(), self.buttons[i][lo].text()
                        for j in range(2):
                            self.buttons[i][j].setStyleSheet('background: transparent')
                            self.buttons[i][j].blockSignals(True)
                        self.queue_game.append([[f'W{i}', win], [f'L{i}', lose]])
                        self.change_grid(win, lose, i)

    # Изменение сетки
    def change_grid(self, win, lose, i):
        for j in self.buttons.keys():
            for k in range(2):
                if self.buttons[j][k].text() == f'W{i}':
                    self.buttons[j][k].setText(win)
                    if win != '--':
                        self.buttons[j][k].setStyleSheet('background-color: white)')
                        self.buttons[j][k].blockSignals(False)
                if self.buttons[j][k].text() == f'L{i}':
                    self.buttons[j][k].setText(lose)
                    if lose != '--':
                        self.buttons[j][k].setStyleSheet('background-color: white)')
                        self.buttons[j][k].blockSignals(False)
                if self.queue_game and self.buttons[j][k].text() in [win, lose]:
                    if not self.buttons[j][k].signalsBlocked():
                        name = self.name_sub[self.num_grid][j][k]
                        if self.name_sub[self.num_grid][j][k][0] == 'W':
                            if self.queue_game[-1][0][1] == win:
                                self.queue_game[-1][0][0] = name
                            if self.queue_game[-1][1][1] == win:
                                self.queue_game[-1][1][0] = name
                        else:
                            if self.queue_game[-1][0][1] == lose:
                                self.queue_game[-1][0][0] = name
                            if self.queue_game[-1][1][1] == lose:
                                self.queue_game[-1][1][0] = name
        self.check()

    # Проверка правильности сетки
    def check(self):
        for i in self.buttons.keys():
            team_1 = self.buttons[i][0]
            team_2 = self.buttons[i][1]
            if team_1.text() == '--' and team_2.text() == '--':
                team_1.setText('---')
                team_2.setText('---')
                self.change_grid('--', '--', i)
                break
            elif team_1.text() == '--' and not team_2.signalsBlocked():
                self.buttons[i][1].setStyleSheet('background: transparent')
                self.buttons[i][1].blockSignals(True)
                self.change_grid(team_2.text(), '--', i)
                break
            elif not team_1.signalsBlocked() and team_2.text() == '--':
                self.buttons[i][0].setStyleSheet('background: transparent')
                self.buttons[i][0].blockSignals(True)
                self.change_grid(team_1.text(), '--', i)
                break

    def back(self):
        if self.queue_game:
            if type(self.queue_game[-1]) is list:
                coor_win, win = self.queue_game[-1][0]
                coor_lose, lose = self.queue_game[-1][1]
                flag = 0
                for i in self.buttons:
                    if (win == self.buttons[i][0].text() and
                            coor_win == self.name_sub[self.num_grid][i][0]):
                        flag = 1
                        self.back_grid(i, 0, coor_win)
                    elif (win == self.buttons[i][1].text() and
                          coor_win == self.name_sub[self.num_grid][i][1]):
                        flag = 1
                        self.back_grid(i, 1, coor_win)
                    if (lose == self.buttons[i][0].text() and
                            coor_lose == self.name_sub[self.num_grid][i][0]):
                        flag = 1
                        self.back_grid(i, 0, coor_lose)
                    elif (lose == self.buttons[i][1].text() and
                          coor_lose == self.name_sub[self.num_grid][i][1]):
                        flag = 1
                        self.back_grid(i, 1, coor_lose)
                if not flag:
                    self.back_grid_final(int(coor_win[1:]))
            else:
                button1, button2 = self.queue_game[-1]
                text1, text2 = button1.text(), button2.text()
                button1.setText(text2)
                button2.setText(text1)
            del self.queue_game[-1]

    def back_grid(self, i, n, coor):
        surname = self.buttons[i][n].text()
        title = coor
        self.buttons[i][n].setText(title)
        self.buttons[i][n].blockSignals(True)
        self.buttons[i][n].setStyleSheet('background-color: transparent')
        num = int(title[1:])
        if self.buttons[num][0].text() == surname:
            num_team = 0
            self.buttons[num][0].blockSignals(False)
            self.buttons[num][0].setStyleSheet('background-color: white)')
        else:
            num_team = 1
            self.buttons[num][1].blockSignals(False)
            self.buttons[num][1].setStyleSheet('background-color: white)')
        if self.buttons[num][1 - num_team].text() == '--':
            self.back_grid(num, num_team, self.name_sub[self.num_grid][num][num_team])
        else:
            self.buttons[num][1 - num_team].blockSignals(False)
            self.buttons[num][1 - num_team].setStyleSheet('background-color: white)')

    def back_grid_final(self, mach):
        for i in range(2):
            self.buttons[mach][i].blockSignals(False)
            self.buttons[mach][i].setStyleSheet('background-color: white)')

    def format_team(self):
        pass

    def result(self):
        pass

    def edit(self):
        self.edit_bool = 1 - self.edit_bool

        if self.edit_bool:
            color = self.main.color_green[self.main.season]
        else:
            color = self.main.colors_text[self.main.season]
        self.main.buttons[6].setStyleSheet(f'''{self.main.style_tools_button}
                                        QPushButton {{
                                background-image: url({self.main.season}/button_on_tools.png);
                                color: {color};
                                font: 10pt "Groboldov";
                                border-radius: 10px;}}''')

        self.setAcceptDrops(self.edit_bool)
        for i in self.buttons.values():
            for btn in i:
                btn.setedit(self.edit_bool)

    def dragEnterEvent(self, e):
        if not e.source().signalsBlocked():
            e.accept()

    def dropEvent(self, e):
        x0, y0 = e.position().x(), e.position().y()
        button1 = e.source()
        button2 = 0
        flag = 0
        for i in self.buttons.values():
            for btn in i:
                x, y = btn.x(), btn.y()
                w, h = btn.width(), btn.height()
                if x <= x0 <= x + w and y <= y0 <= y + h and not btn.signalsBlocked():
                    button2 = btn
                    flag = 1
                    break
            if flag:
                text1, text2 = button1.text(), button2.text()
                button1.setText(text2)
                button2.setText(text1)
                self.queue_game.append((button1, button2))
                break
