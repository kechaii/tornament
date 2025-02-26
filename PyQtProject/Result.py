import csv
import sqlite3
from PyQt6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QListWidget
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QColor
from Const import FONTNAME


# Класс результатов Группового этапа
class Result(QTableWidget):
    def __init__(self, league, season):
        super().__init__()

        self.con = sqlite3.connect('Tournaments.sqlite')
        self.cur = self.con.cursor()

        counting = list(self.cur.execute(f'''SELECT counting FROM league
                                        WHERE id = {league[1]}'''))[0][0]

        self.setGeometry(QRect(0, 0, 1021, 645))

        self.season = season

        color_lable = {'summer': '#EDCBA5', 'winter': '#09525C'}

        self.arr_id = [(i[0], i[1], i[2]) for i in league[-1]]
        arr_error = {'Корт': [], 'Результат': []}
        self.arr_result = []
        arr_name_column = ['Место']

        self.correct = 0

        # Проверка Групп на пригодность
        for i in self.arr_id:
            with open(f'group_result/{i[0]}_id.csv', 'r', newline='', encoding='utf-8') as file:
                arr = list(csv.reader(file, delimiter=',', quotechar='"'))
                format = list(map(int, arr[-1][0].split('/')))
                new_res = []
                arr_name_column.append(i[1])
                for en, j in enumerate(arr[:-1]):
                    k, r1, r2 = j
                    k, r1, r2 = k.strip(), r1.strip(), r2.strip()
                    if not k.isdigit():
                        arr_error['Корт'].append(f'{i[1]} -- {en + 1}')
                    result_true_false = 1
                    if format[0] == 1 and r1.isdigit() and r2.isdigit():
                        r1, r2 = int(r1), int(r2)
                        if (max(r1, r2) == format[1] and min(r1, r2) in range(0, format[1] - 1) or
                                max(r1, r2) >= format[1] and max(r1, r2) - min(r1, r2) == 2):
                            result_true_false = 0
                            victor1 = 1 if r1 > r2 else 0
                            victor2 = 1 - victor1
                            new_res.append((r1 - r2, r2 - r1, victor1, victor2))
                    elif format[0] in [2, 3]:
                        r1, r2 = r1.split(), r2.split()
                        dig = all([i.isdigit() for i in r1]) and all([i.isdigit() for i in r1])
                        if dig:
                            r1 = list(map(int, r1))
                            r2 = list(map(int, r2))
                        if not dig or len(r1) < 2 or len(r2) < 2 or len(r1) != len(r2):
                            pass
                        else:
                            for k in range(len(r1)):
                                res = format[1]
                                if k == 2 and format[0] == 2:
                                    res = format[2]
                                res1, res2 = r1[k], r2[k]
                                if (max(res1, res2) == res and
                                        min(res1, res2) in range(0, res - 1) or
                                        max(res1, res2) >= res and
                                        max(res1, res2) - min(res1, res2) == 2):
                                    result_true_false = 0
                                else:
                                    result_true_false = 1
                                    break
                            if result_true_false == 0:
                                if len(r1) == 2:
                                    if not (r1[0] > r2[0] and r1[1] > r2[1] or
                                            r1[0] < r2[0] and r1[1] < r2[1]):
                                        result_true_false = 1
                                    else:
                                        victor1 = 1 if r1[1] > r2[1] else 0
                                        victor2 = 1 - victor1
                                        new_res.append((r1[0] - r2[0] + r1[1] - r2[1],
                                                        r2[0] - r1[0] + r2[1] - r1[1],
                                                        victor1, victor2))
                                else:
                                    if not (r1[0] > r2[0] and r1[1] < r2[1] or
                                            r1[0] < r2[0] and r1[1] > r2[1]):
                                        result_true_false = 1
                                    else:
                                        victor1 = 1 if r1[2] > r2[2] else 0
                                        victor2 = 1 - victor1
                                        new_res.append((r1[0] - r2[0] + r1[1] - r2[1] +
                                                        r1[2] - r2[2],
                                                        r2[0] - r1[0] + r2[1] - r1[1] +
                                                        r2[2] - r1[2], victor1, victor2))

                    if result_true_false:
                        arr_error['Результат'].append(f'{i[1]} -- {en + 1}')
                self.arr_result.append(new_res)
        # Показ ошибок при неверном заполнение Таблиц
        if len(arr_error['Результат']) + len(arr_error['Корт']) != 0:

            self.correct = 0

            background = QLabel('', self)
            background.resize(1021, 645)
            background.setStyleSheet(f'background-image : url({self.season}/main_background.jpg)')

            text_error = QLabel('', self)
            text_error.move(138, 47)
            text_error.resize(745, 550)
            text_error.setStyleSheet(f'background-image : url({self.season}/table.png)')

            create_name = [('Ошибки', 435, 90, 28), ('Корт:', 300, 150, 22),
                           ('Результат:', 620, 150, 22)]
            for i in create_name:
                lable_error = QLabel(i[0], self)
                lable_error.resize(160, 50)
                if season == 'winter' and i[0] == 'Ошибки':
                    lable_error.move(i[1], i[2] + 30)
                else:
                    lable_error.move(i[1], i[2])
                if i[0] == 'Ошибки':
                    lable_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lable_error.setFont(QFont(FONTNAME, i[3]))
                lable_error.setStyleSheet(f'background: transparent; color: {color_lable[season]}')

            create_list = [('Корт', 220), ('Результат', 580)]
            for i in create_list:
                list_error = QListWidget(self)
                list_error.resize(230, 300)
                list_error.move(i[1], 210)
                list_error.setFont(QFont(FONTNAME, 12))
                list_error.setStyleSheet(f'''QListWidget {{
                                                background: transparent;
                                                border: 4px solid {color_lable[season]};
                                                border-radius: 10px;
                                                selection-color: black;
                                                selection-background-color: white;
                                                color: {color_lable[season]}
                                                }}
                                             QScrollBar:vertical {{
                                                background: transparent;
                                                width: 15px;
                                                margin: 0px 3px 0px 3px;
                                                border-radius: 4px;
                                            }}
                                QScrollBar::handle:vertical {{
                                                background-color: {color_lable[season]};                    
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
                if len(arr_error[i[0]]) == 0:
                    name = ['Ошибок нет']
                else:
                    name = arr_error[i[0]]
                list_error.addItems(name)
        # Показ результатов после успешного Группового этапа
        else:
            self.correct = 1
            if counting == 1:
                self.rating()
            else:
                self.meetings()

            self.setStyleSheet('QTableWidget{gridline-color: black}')

            self.setRowCount(max([len(i) for i in self.arr_victories]) + 1)
            self.setColumnCount(len(arr_name_column))
            for i in range(max([len(i) for i in self.arr_victories]) + 1):
                self.setRowHeight(i, 92 if i != 0 else 39)
                if i != 0:
                    item = QTableWidgetItem(['I', 'II', 'III', 'IV', 'V', 'VI'][i - 1])
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setBackground(QColor(204, 204, 204))
                    self.setItem(i, 0, item)

            for en, i in enumerate(arr_name_column):
                width = 54 if en == 0 else 95
                self.setColumnWidth(en, width)
                item = QTableWidgetItem(i)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(QColor(153, 153, 153))
                item.setFont(QFont('DemiBold', 12))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.setItem(0, en, item)

                for col, i in enumerate(self.arr_victories):
                    for row, j in enumerate(i):
                        item = QTableWidgetItem(f'{j[0]}\n\n{j[2]}\n\n{j[1]}')
                        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                        item.setFont(QFont('Arial', 10))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.setItem(row + 1, col + 1, item)

    def rating(self):
        self.arr_victories = []
        for en, i in enumerate(self.arr_result):
            dict_result = {}
            dict_victories = {}
            teams = [f'{j[0][0]} / {j[1][0]}' for j in self.arr_id[en][-1]]
            group = self.arr_id[en][1]
            with open(f'table_format/{len(teams)}_team.csv', 'r', newline='',
                      encoding='utf-8') as file:
                format_arr = list(csv.reader(file, delimiter=',', quotechar='"'))
                format_arr = [(int(j[2]), int(j[4])) for j in format_arr]
                for k, j in enumerate(format_arr):
                    team1 = teams[j[0] - 1]
                    team2 = teams[j[1] - 1]

                    dict_result[team1] = dict_result.get(team1, 0) + i[k][0]
                    dict_result[team2] = dict_result.get(team2, 0) + i[k][1]

                    dict_victories[team1] = dict_victories.get(team1, 0) + i[k][2]
                    dict_victories[team2] = dict_victories.get(team2, 0) + i[k][3]

                arr = [(i, dict_result[i], dict_victories[i], group) for i in dict_result.keys()]
                arr = sorted(arr, key=lambda x: (x[2], x[1]))[::-1]
                self.arr_victories.append(arr)

    def meetings(self):
        pass

    # Даёт разрешение на создание сетки
    def iscorrect(self):
        if self.correct:
            return self.arr_victories
        else:
            return 0
