#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import random
import datetime
import json

# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5 import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QImage, QBrush, QPalette, QFontDatabase
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTableWidget, QAbstractItemView, QHeaderView, QGridLayout, \
    QMessageBox, QTableWidgetItem, QApplication


class OverwatchWinrateTracker(QWidget):
    score_win_n, score_lose_n, score_draw_n = 0, 0, 0
    winrate_n = 0

    def __init__(self, parent=None):
        super(OverwatchWinrateTracker, self).__init__(parent)

        # главное окно
        # self.setGeometry(300, 300, 300, 220)
        self.setFixedSize(500, 600)
        self.setWindowTitle('Overwatch Winrate Tracker')
        self.setWindowIcon(QIcon('ico.png'))
        # self.center()

        # фон
        bg_file = 'bg\\' + str(random.randrange(1, 9)) + '.png'
        oImage = QImage(bg_file)
        # sImage = oImage.scaled(QSize(500, 600))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(oImage))  # 10 = Windowrole
        self.setPalette(palette)

        # стили
        # self.setStyleSheet('QPushButton {border: None; background-repeat: None; background-position: center}'
        QFontDatabase.addApplicationFont('ttf/BigNoodleToo.ttf')
        self.setStyleSheet(
            '#mainBatton {border: None; background-repeat: None; background-position: center}'
            '#mainQlale {background-position: center; font-family:BigNoodleToo; font-size:80px; color: #cc0000}'
            'QTableWidget {font-size:16px}')

        # win_button
        win_button = QPushButton(self)
        win_button.setMaximumSize(150, 120)
        win_button.setMinimumSize(150, 120)
        win_button.setObjectName('mainBatton')
        win_button.setStyleSheet("""
            QPushButton {background-image: url(bt/win1.png)}
            QPushButton:hover { background-image: url(bt/win2.png) }
            """)
        win_button.clicked.connect(self.button_win_clicked)

        # lose_button
        lose_button = QPushButton(self)
        lose_button.setMaximumSize(150, 120)
        lose_button.setObjectName('mainBatton')
        lose_button.setStyleSheet("""
            QPushButton {background-image: url(bt/lose1.png)}
            QPushButton:hover {background-image: url(bt/lose2.png)}
            """)
        lose_button.clicked.connect(self.button_lose_clicked)

        # draw_button
        draw_button = QPushButton(self)
        draw_button.setMaximumSize(150, 120)
        draw_button.setObjectName('mainBatton')
        draw_button.setStyleSheet("""
            QPushButton {background-image: url(bt/draw1.png)}
            QPushButton:hover {background-image: url(bt/draw2.png)}
            """)
        draw_button.clicked.connect(self.button_draw_clicked)

        # лейблы    mainQlale
        self.win_lable = QLabel(str(self.score_win_n), self)
        self.win_lable.setObjectName('mainQlale')
        self.win_lable.setAlignment(Qt.AlignCenter)

        self.lose_lable = QLabel(str(self.score_lose_n), self)
        self.lose_lable.setObjectName('mainQlale')
        self.lose_lable.setAlignment(Qt.AlignCenter)

        self.draw_lable = QLabel(str(self.score_draw_n), self)
        self.draw_lable.setObjectName('mainQlale')
        self.draw_lable.setAlignment(Qt.AlignCenter)

        self.winrate_lable = QLabel('Winrate:  %', self)
        self.winrate_lable.setObjectName('mainQlale')
        self.winrate_lable.setAlignment(Qt.AlignCenter)

        # таблица
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(2)
        # self.history_table.setRowCount(3)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setHorizontalHeaderLabels(["Time", "Result"])

        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.history_table.setColumnWidth(0, 180)
        self.history_table.setColumnWidth(1, 90)

        # self.history_table.horizontalHeader().setDefaultSectionSize(140)
        # self.history_table.setHorizontalHeader().setDefaultSectionSize(140)
        self.history_table.verticalHeader().hide()
        self.history_table.verticalHeader().setDefaultSectionSize(24)

        # self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # кнопки нижнии
        self.his_bt_del = QPushButton('del', self)
        self.his_bt_del.clicked.connect(self.history_del)

        self.his_bt_stat = QPushButton('stat', self)
        self.his_bt_stat.clicked.connect(self.open_stat_window)

        self.his_bt_save = QPushButton('save', self)
        self.his_bt_save.clicked.connect(self.save_datafile)

        self.his_bt_exit = QPushButton('exit', self)
        self.his_bt_exit.clicked.connect(self.closeEvent)

        # упаквка
        self.grid = QGridLayout(self)
        self.grid.setVerticalSpacing(10)

        self.grid.addWidget(win_button, 0, 0)
        self.grid.addWidget(lose_button, 0, 1)
        self.grid.addWidget(draw_button, 0, 2)

        self.grid.addWidget(self.win_lable, 1, 0)
        self.grid.addWidget(self.lose_lable, 1, 1)
        self.grid.addWidget(self.draw_lable, 1, 2)

        self.grid.addWidget(self.winrate_lable, 2, 0, 1, 3)

        self.grid.addWidget(self.history_table, 5, 0, 5, 2)

        self.grid.addWidget(self.his_bt_del, 5, 2)
        self.grid.addWidget(self.his_bt_stat, 6, 2)
        self.grid.addWidget(self.his_bt_save, 7, 2)
        self.grid.addWidget(self.his_bt_exit, 8, 2)

        # self.setLayout(grid)

    # ===============================================

    def button_win_clicked(self):
        self.score_win_n += 1
        self.win_lable.setText(str(self.score_win_n))
        self.winrate_considers()
        self.history_newline('Win')

    def button_lose_clicked(self):
        self.score_lose_n += 1
        self.lose_lable.setText(str(self.score_lose_n))
        self.winrate_considers()
        self.history_newline('Lose')

    def button_draw_clicked(self):
        self.score_draw_n += 1
        self.draw_lable.setText(str(self.score_draw_n))
        self.winrate_considers()
        self.history_newline('Draw')

    def winrate_considers(self):
        if (self.score_win_n + self.score_lose_n + self.score_draw_n) == 0:
            self.winrate_n = 0
        else:
            tmp = int((self.score_win_n / (self.score_win_n + self.score_lose_n + self.score_draw_n)) * 100)
            # print(tmp)
            # label_winrate['text'] = 'winrate: ' + str(score_win_n) + str(score_lose_n) + str(int(tmp)) + ' %'
            self.winrate_n = tmp
        tmp = 'Winrate: ' + str(self.winrate_n) + ' %'
        self.winrate_lable.setText(tmp)

    def open_stat_window(self):
        # достать данные
        history_arr = self.history_arr()
        datafile = self.load_datafile()

        if history_arr == None and datafile == None:
            fulldata = None
        elif history_arr == None and datafile != None:
            fulldata = datafile
        elif history_arr != None and datafile == None:
            fulldata = history_arr
        elif history_arr != None and datafile != None:
            fulldata = datafile + list(reversed(history_arr))

        print(history_arr)
        print(datafile)
        print(fulldata)

        if fulldata != None:
            self.stat_window = OWTStatWindow(fulldata)
            self.stat_window.show()

    def closeEvent(self, z):
        data = self.history_arr()
        if data != None:
            ask = QMessageBox.question(
                self, 'Save data',
                'Сохранить новые данные?',
                QMessageBox.Save | QMessageBox.Close,
                QMessageBox.Save)
            print(ask)
            if ask == QMessageBox.Save:
                self.save_datafile()
        print('exit')
        # self.close()
        # app.quit()
        sys.exit()

    # ===============================================

    def history_newline(self, res):
        now_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        now_datetime = QTableWidgetItem(now_datetime)
        now_datetime.setTextAlignment(Qt.AlignHCenter)
        res = QTableWidgetItem(res)
        res.setTextAlignment(Qt.AlignHCenter)
        self.history_table.insertRow(0)
        self.history_table.setItem(0, 0, now_datetime)
        self.history_table.setItem(0, 1, res)
        # print(self.history_table.rowCount())

    def history_del(self):
        if self.history_table.currentRow() != -1:
            res = self.history_table.item(self.history_table.currentRow(), 1).text()
            if res == 'Win':
                self.score_win_n -= 1
                self.win_lable.setText(str(self.score_win_n))
                self.winrate_considers()
            elif res == 'Lose':
                self.score_lose_n -= 1
                self.lose_lable.setText(str(self.score_lose_n))
                self.winrate_considers()
            elif res == 'Draw':
                self.score_draw_n -= 1
                self.draw_lable.setText(str(self.score_draw_n))
                self.winrate_considers()

            self.history_table.removeRow(self.history_table.currentRow())
        self.history_table.setCurrentCell(-1, -1)

    def history_arr(self):
        if self.history_table.rowCount() == 0:
            return None
        else:
            res_arr = []
            for row_n in range(self.history_table.rowCount()):
                # print(self.history_table.item(row_n, 0).text())
                tmp_arr = []
                tmp_arr.append(self.history_table.item(row_n, 0).text())
                tmp_arr.append(self.history_table.item(row_n, 1).text())
                res_arr.append(tmp_arr)
            return res_arr

    def save_datafile(self):
        data = self.history_arr()
        if data != None:
            with open('treacker.txt', 'a') as file:
                for st in reversed(data):
                    json.dump(st, file)
                    file.write("\n")

    def load_datafile(self):
        try:
            with open('treacker.txt') as file:
                file_data = []
                for line in file:
                    file_data.append(json.loads(line))
                    # print(line)
                    # file_data.append([line[:line.find(',')], line[line.find(',') + 1:-1]])

                return file_data
        except:
            # messagebox.showerror("Ошибка", "Отсутствует файл с данным")
            print('no file')
            return None


# ===============================================

# окно статистики

class OWTStatWindow(QWidget):

    def __init__(self, fulldata, parent=None):
        super(OWTStatWindow, self).__init__(parent)

        # self.setGeometry(300, 300, 0, 0)
        self.setFixedWidth(350)
        self.setMinimumHeight(500)
        self.setWindowTitle('Overwatch Winrate Tracker')
        self.setWindowIcon(QIcon('ico.png'))

        QFontDatabase.addApplicationFont('ttf/BigNoodleToo.ttf')
        self.setStyleSheet(
            'QLabel {background-position: center; font-family:BigNoodleToo; font-size:35px; color: #cc0000}'
            'QTableWidget {font-size:16px}')

        stat_game_n = len(fulldata)
        win = sum([1 for i in fulldata if i[1] == 'Win'])
        stat_winrate = int((win / stat_game_n) * 100)
        # label_st = 'games: ' + str(stat_game_n) + ', winrate: ' + str(stat_winrate)

        # верх лейбл
        self.lable_stat_game_n = QLabel('games: ' + str(stat_game_n), self)
        self.lable_stat_game_n.setAlignment(Qt.AlignCenter)
        self.lable_stat_winrate = QLabel('winrate: ' + str(stat_winrate) + '%', self)
        self.lable_stat_winrate.setAlignment(Qt.AlignCenter)

        # таблица
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(2)
        # self.history_table.setRowCount(3)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.history_table.setHorizontalHeaderLabels(["Time", "Result"])

        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.history_table.setColumnWidth(0, 180)
        self.history_table.setColumnWidth(1, 90)

        # self.history_table.horizontalHeader().setDefaultSectionSize(140)
        # self.history_table.setHorizontalHeader().setDefaultSectionSize(140)

        self.history_table.verticalHeader().hide()
        self.history_table.verticalHeader().setDefaultSectionSize(24)

        # отрисовка в таблицу
        if fulldata != None:
            for i in fulldata:
                date = i[0]
                date = QTableWidgetItem(date)
                date.setTextAlignment(Qt.AlignHCenter)
                res = i[1]
                res = QTableWidgetItem(res)
                res.setTextAlignment(Qt.AlignHCenter)
                self.history_table.insertRow(0)
                self.history_table.setItem(0, 0, date)
                self.history_table.setItem(0, 1, res)

        # упаквка
        self.grid = QGridLayout(self)
        # self.grid.setVerticalSpacing(10)

        self.grid.addWidget(self.lable_stat_game_n, 0, 0)
        self.grid.addWidget(self.lable_stat_winrate, 0, 1)
        self.grid.addWidget(self.history_table, 1, 0, 1, 0)


# ===============================================

if __name__ == '__main__':
    app = QApplication(sys.argv)

    tracker = OverwatchWinrateTracker()
    tracker.show()

    sys.exit(app.exec_())
