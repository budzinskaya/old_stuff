import sys
import os
import string
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QTextEdit,
    QDockWidget,
    QLineEdit,
    QAction,
    QMessageBox,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Удалятор знаков препинания")

        # главный виджет QTextEdit для отображения и редактирования текста
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit) # это будет центральный виджет

        # QDockWidget для ввода пути к файлу
        dock_widget = QDockWidget("Путь к файлу", self)
        self.path_line_edit = QLineEdit(dock_widget) # ввод пути к файлу
        dock_widget.setWidget(self.path_line_edit) # устанавливаем QLineEdit в QDockWidget
        self.addDockWidget(1, dock_widget) # засовывем виджет в главное окно (эриа 1 это слева так, можно поиграть циферками)

        # создаем действия для меню (вызов функции ниже)
        self.create_actions()

        # состояние наших переменных в начальном окне
        self.deleted_count = 0 # колво удаленных знаков препинания (пока ноль)
        self.cleaned_text = ""  # очищенный текст (пока пустой)

    def create_actions(self):
        open_action = QAction("Открыть файл", self)
        open_action.triggered.connect(self.open_file) # подключаем действие к методу открывания файла

        remove_punctuation_action = QAction("Удалить знаки препинания", self)
        remove_punctuation_action.triggered.connect(self.remove_punctuation) # подключаем к удалятору пунктуации, ниже аналогично

        continue_action = QAction("Продолжить", self)
        continue_action.triggered.connect(self.open_next_window)
        # добавляем действия в меню
        self.menuBar().addAction(open_action)
        self.menuBar().addAction(remove_punctuation_action)
        self.menuBar().addAction(continue_action)

    def open_file(self):
        file_path = self.path_line_edit.text() # получаем путь к файлу из QLineEdit
        if os.path.exists(file_path): # если файл по пути существует
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_edit.setPlainText(content) # посылаем текст в QTextEdit
        else:
            QMessageBox.warning(self, "Ошибка", "Файл не найден!")

    def remove_punctuation(self):
        original_text = self.text_edit.toPlainText()
        # считаем количество удаляемых знаков препинания. можно переделать!
        self.deleted_count = sum(1 for char in original_text if char in string.punctuation)
        self.cleaned_text = ''.join(char for char in original_text if char not in string.punctuation)
        self.text_edit.setPlainText(self.cleaned_text)
        QMessageBox.information(self, "Завершено", f"Удалено знаков препинания: {self.deleted_count}")

    def open_next_window(self):
        # новое окно с результатами
        self.next_window = NextWindow(self.cleaned_text, self.deleted_count)
        self.next_window.show()
        self.hide()


class NextWindow(QWidget):
    def __init__(self, cleaned_text, deleted_count):
        super().__init__()
        self.setWindowTitle("Результаты")

        self.label = QLabel(f"Удалено знаков препинания: {deleted_count}", self)
        self.save_button = QPushButton("Сохранить текст", self)
        self.back_button = QPushButton("Назад", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.save_button)
        layout.addWidget(self.back_button)

        self.save_button.clicked.connect(self.save_text)
        self.back_button.clicked.connect(self.back_to_main)

        self.cleaned_text = cleaned_text

    def save_text(self):
        # открываем диалог для выбора места сохранения файла
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt);;All Files (*)")
        # если путь к файлу выбран
        if file_path:
            # сохраняем текст в файл
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.cleaned_text)
            # показываем сообщение об успешном сохранении
            QMessageBox.information(self, "Успех", "Текст успешно сохранен!")

    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())