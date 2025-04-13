import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt


# Функция для транслитерации кириллицы в латиницу
def transliterate(text):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ë': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
        'Е': 'E', 'Ë': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    result = ""
    for char in text:
        result += translit_dict.get(char, char)
    return result


class Window1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        label1 = QLabel('Транслитерация')
        label1.setAlignment(Qt.AlignCenter)  # Выравниваем по центру.
        button = QPushButton('Транслитерировать', self)  # Создаем кнопку.
        button.clicked.connect(self.transliterate_text)  # Привязываем кнопку к функции транслитератора.
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Введите имя на кириллице")
        self.result_label = QLabel('', self)

        layout = QVBoxLayout()  # Вертикальный макет, в который мы будем класть наши виджеты.
        layout.addWidget(label1)  # Добавляем надпись.
        layout.addWidget(self.input_field)  # Добавляем поле для ввода.
        layout.addWidget(button)  # Добавляем кнопку.
        layout.addWidget(self.result_label)
        self.setLayout(layout)  # Устанавливаем наш макет в окно.


    def transliterate_text(self):
        input_text = self.input_field.text()
        transliterated_text = transliterate(input_text)
        self.result_label.setText(transliterated_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window1()
    ex.resize(300, 150)
    ex.show()
    sys.exit(app.exec_())


