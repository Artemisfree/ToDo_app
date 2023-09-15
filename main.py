import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit,\
    QPushButton, QListWidget


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('ToDo App')
        self.setGeometry(100, 100, 400, 400)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText('Введите текст...')
        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_item)

        self.item_list = QListWidget(self)

        self.delete_button = QPushButton('Удалить выбранный', self)
        self.delete_button.clicked.connect(self.delete_item)

        layout = QVBoxLayout()
        layout.addWidget(self.text_input)
        layout.addWidget(self.item_list)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

        self.conn = sqlite3.connect('todolist.db')
        self.create_table()

        self.load_items()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS todo (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item TEXT NOT NULL)''')
        self.conn.commit()

    def add_item(self):
        item_text = self.text_input.text()
        if item_text:
            c = self.conn.cursor()
            c.execute("INSERT INTO todo (item) VALUES (?)", (item_text,))
            self.conn.commit()
            self.text_input.clear()
            self.load_items()

    def load_items(self):
        self.item_list.clear()
        c = self.conn.cursor()
        c.execute("SELECT id, item FROM todo")
        items = c.fetchall()
        for item in items:
            self.item_list.addItem(item[1])

    def delete_item(self):
        selected_item = self.item_list.currentItem()
        if selected_item:
            item_text = selected_item.text()
            c = self.conn.cursor()
            c.execute("DELETE FROM todo WHERE item=?", (item_text,))
            self.conn.commit()
            self.load_items()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = ToDoApp()
    todo_app.show()
    sys.exit(app.exec_())
