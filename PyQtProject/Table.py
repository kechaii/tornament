import csv
from PyQt6.QtWidgets import QTableWidget, QCheckBox, QTableWidgetItem
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QColor

QUANTILY_ROW = {3: 6, 4: 9, 5: 13, 6: 18}
NAMECOLUMN = ['Номер матча', 'Корт', 'Команда 1', 'VS', 'Команда 2', 'Судит', 'Результат']


# Класс таблиц с группами
class Table(QTableWidget):
    def __init__(self, num, name, format, teams, id_group, way):
        super().__init__()

        self.setGeometry(QRect(0, 0, 1021, 645))

        self.teams, self.id_group, self.format = teams, id_group, format

        self.setStyleSheet('QTableWidget{gridline-color: black}')

        arr_name = ['Вид', 'Гандикап']
        self.check_box = []

        y = 50
        for name in arr_name:
            button = QCheckBox(name, self)
            button.move(900, y)
            button.clicked.connect(self.change_view)
            self.check_box.append(button)
            y += 25

        self.setRowCount(2)
        self.setColumnCount(9)

        item = QTableWidgetItem(name)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFont(QFont('DemiBold', 25))
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.setItem(0, 0, item)

        self.setSpan(0, 0, 1, 9)

        for en, i in enumerate(NAMECOLUMN):
            item = QTableWidgetItem(i)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(QColor(153, 153, 153))
            item.setFont(QFont('DemiBold', 13))
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.setItem(1, en, item)

        self.setSpan(1, 6, 1, 3)

        for i in range(3, 7):
            if num == i:
                with open(f'table_format/{i}_team.csv', 'r', newline='', encoding='utf-8') as file:
                    self.arr = list(csv.reader(file, delimiter=',', quotechar='"'))
                qua = QUANTILY_ROW[i]
                break

        self.setRowCount(qua)
        for i in range(qua - 1):
            self.setRowHeight(i, 50)
        self.setRowHeight(qua - 1, 40)

        item = QTableWidgetItem(f'Формат: {format}')
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor(217, 217, 217))
        item.setFont(QFont('DemiBold', 13))
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.setItem(qua - 1, 0, item)

        self.setSpan(qua - 1, 0, 1, 9)

        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 170)
        self.setColumnWidth(3, 60)
        self.setColumnWidth(4, 170)
        self.setColumnWidth(5, 170)
        self.setColumnWidth(6, 60)
        self.setColumnWidth(7, 40)
        self.setColumnWidth(8, 60)

        self.change_view()
        self.edit_result(way)

        self.cellChanged.connect(self.edit_result)

    # Смена формата Фамилий
    def change_view(self):
        for row, i in enumerate(self.arr):
            for col, j in enumerate(i):
                if col in [2, 4, 5]:
                    name1 = f'{self.teams[int(j) - 1][0][0]} {self.teams[int(j) - 1][0][1][0]}.'
                    name2 = f'{self.teams[int(j) - 1][1][0]} {self.teams[int(j) - 1][1][1][0]}.'
                    if self.check_box[0].isChecked():
                        team = f'{name1} / {name2}'
                    else:
                        team = name1
                    if col in [2, 4] and self.check_box[1].isChecked():
                        zn = ''
                        if self.teams[int(j) - 1][2][1] == 1:
                            zn = '+'
                        elif self.teams[int(j) - 1][2][1] == -1:
                            zn = '-'
                        team += '\n(' + zn + self.teams[int(j) - 1][2][0] + ')'
                else:
                    team = j
                item = QTableWidgetItem(team)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                size = 13 if col == 3 else 10
                font = 'DemiBold' if col == 3 or col == 7 else 'Arial'
                item.setFont(QFont(font, size))
                if col == 3:
                    item.setForeground(QColor(255, 0, 0))
                if col == 0:
                    item.setBackground(QColor(204, 204, 204))
                if col not in [0, 1, 6, 8]:
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.setItem(row + 2, col, item)

    # Редактирование результатов
    def edit_result(self, way='create'):
        for en in range(len(self.arr)):
            self.arr[en][1] = self.item(en + 2, 1).text()
            self.arr[en][6] = self.item(en + 2, 6).text()
            self.arr[en][8] = self.item(en + 2, 8).text()
        if way == 'open':
            with open(f'group_result/{self.id_group}_id.csv', 'r', newline='',
                      encoding='utf-8') as file:
                res = list(csv.reader(file, delimiter=',', quotechar='"'))
                for row, i in enumerate(self.arr):
                    for col, j in enumerate(i):
                        if col in [1, 6, 8]:
                            index = [1, 6, 8].index(col)
                            item = QTableWidgetItem(res[row][index])
                            item.setFont(QFont('Arial', 10))
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.setItem(row + 2, col, item)

        else:
            with open(f'group_result/{self.id_group}_id.csv', 'w', newline='',
                      encoding='utf-8') as file:
                w = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in self.arr:
                    w.writerow([i[1], i[6], i[8]])
                w.writerow([self.format])
