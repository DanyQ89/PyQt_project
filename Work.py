import io
import sqlite3
import sys
import random

from PyQt5 import uic
from PyQt5.Qt import QMainWindow, Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView, QTableWidget, QMessageBox, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QColor

# основная страница
template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MyWidget</class>
 <widget class="QWidget" name="MyWidget">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1279</width>
    <height>885</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Дела на день</string>
  </property>
  <widget class="QWidget" name="gridLayoutWidget">
   <property name="geometry">
    <rect>
     <x>40</x>
     <y>20</y>
     <width>701</width>
     <height>541</height>
    </rect>
   </property>
   <layout class="QGridLayout" name="gridLayout">
    <item row="0" column="0">
     <layout class="QVBoxLayout" name="verticalLayout">
      <item>
       <widget class="QProgressBar" name="progressBar">
        <property name="value">
         <number>24</number>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QTableWidget" name="table"/>
      </item>
     </layout>
    </item>
    <item row="0" column="1">
     <layout class="QVBoxLayout" name="verticalLayout_2">
      <item>
       <widget class="QPushButton" name="add">
        <property name="text">
         <string>Добавить задачу</string>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QPushButton" name="add_category">
        <property name="text">
         <string>Добавить категорию задач</string>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QPushButton" name="change">
        <property name="text">
         <string>Редактировать </string>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QPushButton" name="complete">
        <property name="text">
         <string>Выполнить</string>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QPushButton" name="delete_all">
        <property name="text">
         <string>Удалить все задачи</string>
        </property>
       </widget>
      </item>
     </layout>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

# страница добавления действия
template1 = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>AddAction</class>
 <widget class="QWidget" name="AddAction">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>442</width>
    <height>385</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Добавить элемент</string>
  </property>
  <widget class="QWidget" name="formLayoutWidget">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>30</y>
     <width>411</width>
     <height>111</height>
    </rect>
   </property>
   <layout class="QFormLayout" name="formLayout">
    <item row="0" column="0">
     <widget class="QLabel" name="label">
      <property name="text">
       <string>Название</string>
      </property>
     </widget>
    </item>
    <item row="0" column="1">
     <widget class="QLineEdit" name="lineEdit"/>
    </item>
    <item row="1" column="0">
     <widget class="QLabel" name="label_2">
      <property name="text">
       <string>Важность</string>
      </property>
     </widget>
    </item>
    <item row="1" column="1">
     <widget class="QComboBox" name="importance"/>
    </item>
    <item row="2" column="0">
     <widget class="QLabel" name="label_4">
      <property name="text">
       <string>Категория</string>
      </property>
     </widget>
    </item>
    <item row="2" column="1">
     <widget class="QComboBox" name="category"/>
    </item>
    <item row="3" column="1">
     <widget class="QPushButton" name="pushButton">
      <property name="text">
       <string>Добавить</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

# страница добавления жанра
template2 = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>AddCategory</class>
 <widget class="QMainWindow" name="AddCategory">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>469</width>
    <height>205</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>240</x>
      <y>100</y>
      <width>201</width>
      <height>51</height>
     </rect>
    </property>
    <property name="text">
     <string>Добавить</string>
    </property>
   </widget>
   <widget class="QWidget" name="horizontalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>0</y>
      <width>431</width>
      <height>80</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="horizontalLayout">
     <item>
      <widget class="QLabel" name="label">
       <property name="text">
        <string>Название</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QLineEdit" name="title"/>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>469</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


# # Создаем соединение с базой данных
# conn = sqlite3.connect('actions_database.sql')
#
# # Создаем курсор
# cur = conn.cursor()
#
# # Создаем таблицу categories
# cur.execute("""
# CREATE TABLE categories (
#    id   INTEGER PRIMARY KEY AUTOINCREMENT
#                 UNIQUE
#                 NOT NULL,
#    title        UNIQUE
#                 NOT NULL
# );
# """)
#
# # Создаем таблицу Actions
# cur.execute("""
# CREATE TABLE Actions (
#    id        INTEGER PRIMARY KEY AUTOINCREMENT
#                      NOT NULL,
#    name      STRING NOT NULL,
#    category  INTEGER NOT NULL
#                      REFERENCES categories (id),
#    importance STRING NOT NULL
# );
# """)
#
# # Закрываем соединение
# conn.close()


# класс основной страницы
class Actions(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        # экземпляры класса
        self.addA = AddAction(self)
        self.redA = AddAction(self)
        self.addC = AddCategory(self)
        self.compl = Completed_Day(self)
        # подключение к бд
        self.con = sqlite3.connect('actions_database.sql.db')
        self.cur = self.con.cursor()
        # длина начальной таблицы
        a = self.cur.execute("""SELECT * FROM ACTIONS""").fetchall()
        self.len_last = len(a)
        self.value = len(a)
        # цветовая палитра
        self.green = '#00ff00'
        self.black = '#2c2c2c'
        # прогресс бар
        self.progressBar.setMaximum(self.value)
        self.progressBar.setValue(0)
        self.progressBar.setStyleSheet(
            f'background: {self.black}; color: {self.green}; border: 10px solid {self.black};'
            f' font-weight: bold; font-size: 15px'
        )
        self.initUI()

    # выполнение всех задач
    def all_is_completed(self):
        self.compl = Completed_Day(self)
        self.compl.show()

    # удаление всех элементов с предварительной проверкой на случайное нажатие
    def del_all(self):
        valid = QMessageBox()
        valid.setText('Вы действительно хотите удалить все элементы?')
        first = valid.addButton('Да', QMessageBox.YesRole)
        second = valid.addButton('Нет', QMessageBox.NoRole)
        valid.setStyleSheet(f'background: {self.black}; color: {self.green}; border: 10px solid {self.black};'
                            f' font-weight: bold; font-size: 15px')
        valid.exec_()

        if valid.clickedButton() == first:
            self.progressBar.setMaximum(0)
            self.progressBar.setValue(0)
            self.cur.execute("""
          DELETE FROM ACTIONS
          """)
            self.con.commit()
            self.renew()

    # добавление категории
    def addCategory(self):
        self.addC = AddCategory(self)
        self.addC.show()

    # выполнение задачи
    def completeAct(self):
        row = self.table.currentRow()
        if row > -1:
            item = self.table.item(row, 0).text()
            self.cur.execute(f"""
            DELETE FROM ACTIONS
            WHERE id = '{item}'
            """)
            self.con.commit()
            self.renew()

    # обновление бд и прогресс бара
    def renew(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Категория', 'Важность'])
        res = self.cur.execute("""
        SELECT actions.id, actions.name, title, actions.importance FROM CATEGORIES
        INNER JOIN Actions ON actions.category = categories.id 
        """).fetchall()
        len_now = len(res)
        if self.progressBar.value() == self.progressBar.maximum():
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(0)
            self.len_last = 0
        if len_now > self.len_last and not self.progressBar.value():
            self.len_last += 1
            self.progressBar.setMaximum(len_now)
        elif len_now < self.len_last:
            self.len_last -= 1
            v = self.progressBar.value()
            self.progressBar.setValue(v + 1)
        elif self.len_last != len_now:
            self.len_last += 1
            m = self.progressBar.maximum() + 1
            self.progressBar.setMaximum(m)
        if self.progressBar.value() == self.progressBar.maximum() != 0:
            self.all_is_completed()
        self.table.setRowCount(len(res))
        for i in range(len(res)):
            el = res[i]
            for g in range(len(res[0])):
                self.table.setItem(i, g, QTableWidgetItem(str(el[g])))

    # редактирование элемента бд
    def redAct(self):
        row = self.table.currentRow()
        if row > -1:
            item = self.table.item(row, 0).text()
            self.redA = AddAction(self, action_id=item)
            self.redA.show()

    # добавление элемента в бд
    def addAct(self):
        self.addA = AddAction(self)
        self.addA.show()

    def initUI(self):
        self.renew()
        # подключаем css ко всем элементам главной страницы
        for i in [self.add, self.change, self.add_category, self.delete_all]:
            i.setStyleSheet(
                f'background: {self.black}; color: {self.green}; border: 10px solid {self.black};'
                f' font-weight: bold; font-size: 15px')
        self.complete.setStyleSheet(
            f'background: {self.green}; color: {self.black}; border: 10px solid {self.black};'
            f' font-weight: bold; font-size: 15px')
        self.setStyleSheet(
            f'background: {self.black}; color: {self.green}; border: 10px solid {self.black};'
            f' font-weight: bold; font-size: 15px')
        self.table.setStyleSheet(f'background: {self.black}; color: {self.green}; border: 10px solid {self.black};'
                                 f' font-weight: bold; font-size: 15px')
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setVisible(True)
        header.setStyleSheet("""
            QTableView QHeaderView::section {
                background-color: #2c2c2c;
                color: #00ff00;
                border: 1px solid #2c2c2c;
                font-size: 40px;
                font-weight: cursive;
            }
        """)
        # подключаем нажатие на кнопки
        self.add.clicked.connect(self.addAct)
        self.complete.clicked.connect(self.completeAct)
        self.change.clicked.connect(self.redAct)
        self.table.doubleClicked.connect(self.redAct)
        self.add_category.clicked.connect(self.addCategory)
        self.delete_all.clicked.connect(self.del_all)
        # подключаем считывание курсора
        self.setMouseTracking(True)
        # запрещаем пользователю вводить с клавиатуры
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)


# класс страницы добавления действия
class AddAction(QMainWindow):
    def __init__(self, parent=None, action_id=None):
        super().__init__(parent)
        f = io.StringIO(template1)
        uic.loadUi(f, self)
        self.action_id = action_id
        if action_id:
            self.pushButton.setText('Сохранить')
        # подключение к бд, длина, словарь с категориями и их id
        self.con = sqlite3.connect('actions_database.sql.db')
        self.cur = self.con.cursor()
        self.d = {}
        res = self.cur.execute("""
        SELECT id, title FROM categories
        """).fetchall()
        for i in res:
            k = i[0]
            z = i[1]
            self.d[z] = k
        self.green = '#00ff00'
        self.black = '#2c2c2c'
        self.setFixedSize(500, 500)
        self.initUI()

    # добавляем названия в comboBox
    def renew(self):
        res = self.cur.execute("""
        SELECT DISTINCT title FROM categories
        LEFT JOIN ACTIONS ON actions.category = CATEGORIES.id
        ORDER BY title
        """).fetchall()
        for i in res:
            self.category.addItem(i[0])
        for i in ['Срочно и важно', 'Срочно и неважно', 'Не срочно и важно', 'Не срочно и неважно']:
            self.importance.addItem(i)
        self.pushButton.clicked.connect(self.run)

    # определитель между редактированием и добавлением
    def run(self):
        if self.action_id:
            self.red()
        else:
            self.add()

    # проверка на добавление
    def add_check(self, t):
        names = map(lambda x: x[0].lower(), self.cur.execute("""SELECT name FROM actions"""))
        if t and t not in names and len(t) > 1:
            return True
        return False

    # добавление
    def add(self):
        text = self.lineEdit.text()
        importance = self.importance.currentText()
        category = self.category.currentText()
        if self.add_check(text):
            self.cur.execute(F"""
            INSERT OR REPLACE INTO ACTIONS(name, category, importance)
            VALUES{(text, self.d[category], importance)}
            """)
            self.con.commit()
            self.parent().renew()
            self.close()
        else:
            self.statusBar().showMessage('Заполните все поля и создайте уникальное название дела')

    # редактирование
    def red(self):
        text = self.lineEdit.text()
        importance = self.importance.currentText()
        category = self.category.currentText()

        if self.action_id and text:
            self.cur.execute(f"""
            UPDATE Actions 
            SET name = '{text}', category = '{self.d[category]}', importance = '{importance}'
            WHERE id = {self.action_id}
            """)
            self.con.commit()
            self.parent().renew()
            self.close()

    def initUI(self):
        self.renew()
        # устанавливаем css
        self.setStyleSheet(
            f'background: {self.black}; color: {self.green}; border: 10px solid {self.black};'
            f' font-weight: bold; font-size: 15px')
        # если редактирование, то добавляем на место ввода текста старые значения
        if self.action_id:
            res = self.cur.execute(f"""
                    SELECT actions.name, title, actions.importance FROM CATEGORIES
                    INNER JOIN Actions ON actions.category = categories.id 
                    WHERE actions.id = '{self.action_id}'
                    """).fetchone()
            self.lineEdit.setText(res[0])
            self.category.setCurrentText(str(res[1]))
            self.importance.setCurrentText(str(res[2]))


# Класс добавления категории
class AddCategory(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        f = io.StringIO(template2)
        uic.loadUi(f, self)
        # бд
        self.initUI()
        self.con = sqlite3.connect('actions_database.sql.db')
        self.cur = self.con.cursor()

    # проверка категории
    def category_check(self, text):
        cats = list(map(lambda x: x[0].lower(), self.cur.execute("""
        SELECT DISTINCT title FROM CATEGORIES
        LEFT JOIN ACTIONS ON ACTIONS.category = categories.id
        """).fetchall()))
        if text and len(text) > 1 and text not in cats:
            return True
        return False

    # добавляем категорию
    def add(self):
        text = self.title.text()
        if self.category_check(text):
            self.cur.execute(f"""
            INSERT INTO categories(title)
            VALUES('{text}')
            """)
            self.con.commit()
            self.parent().renew()
            self.close()
        else:
            self.statusBar().showMessage("Некорректное название категории")

    def initUI(self):
        # подключаем кнопку
        self.pushButton.clicked.connect(self.add)


class Completed_Day(QMainWindow):
    # добавляем атрибуты класса и подключаем картинку
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.label = QLabel('', self)
        self.pixmap = QPixmap('cat_photo.jpg')
        self.color = None
        self.btn = QPushButton('P\nA\nR\nT\nY\n \nT\nI\nM\nE\n!\n!\n!\n', self)

        self.initUI()

    #Смена цвета (в разработке)

    # def color_change(self):
    #     image = self.pixmap.toImage()
    #     width = image.width()
    #     height = image.height()
    #     r = random.randint(0, 255)
    #     g = random.randint(0, 255)
    #     b = random.randint(0, 255)
    #     for y in range(height):
    #         for x in range(width):
    #             pix = image.pixelColor(y, x)
    #             pix.setRed(r)
    #             pix.setGreen(0)
    #             pix.setBlue(0)
    #             image.setPixel(y, x, pix.rgb())
    #             # image.setPixelColor(x, y, color)
    #     self.pixmap = QPixmap.fromImage(image)
    #     self.label.setPixmap(self.pixmap)

    # задаем параметры окна, создаем кнопку и двигаем картинку
    def initUI(self):
        self.setFixedSize(self.pixmap.width() + 100, self.pixmap.height())
        self.setWindowTitle('Поздравляем с окончанием всех задач!')
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        self.label.move(0, 0)
        self.label.setPixmap(self.pixmap)
        self.btn.setStyleSheet(f"""font-weight: 40px""")
        self.btn.resize(100, self.pixmap.height())
        self.btn.move(self.pixmap.width(), 0)
        # self.btn.clicked.connect(self.color_change)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Actions()
    ex.show()
    sys.exit(app.exec_())
