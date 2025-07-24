import sys
import base64
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QAction, QMenu, QMenuBar, QDialog, QLabel,
    QSizePolicy, QActionGroup, QShortcut
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeySequence
from PyQt5.QtCore import Qt, QSize

# Base64 иконка стерки (bcspicon.png) в 96x96
bcspicon_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAADT0lEQVR4nO2dP2sUQRjGf8Y/EEE7QZMjn8IIVikttNFGtBYLe1trQYKfQmNrZWUlBg2o30AQEtE64IH/zuJ2NCGXc2d35n3fyz0/mCqXndnnuX12d/bdGxBCCCGEEEIIIYQw45hhXyeAM8Bxwz4j8APYBX5P+qOFAReBO8Bl4Bxw0qDPSAyBr8Ar4AnwzqrjBeAB8A0YqTFibMZj4HQPXVvz0HjnZqk9Bxa7S/t/bgbYyehtHeqcAwbAG2C5wraPEkNgbaHChh8h8duwCNwtvdFb+B/as9Q+lowgRU8+w5IRpOjJp9iVkKKnYysRQYqeHpSIIEWPI4oexwhS9BSgTwQpehxR9JRr2QyAbcMB7gDXgU3DPjebPi32M5sNQyF2gEtNv0vAlkGfW01fAKvNGMIYYBk9O40Ae6ltwl7xE7VNaI1l9EwSP1HLhEniJ2qa0Bqr6PnE4eInSpswTfzEajM2FwOsoucncK3lmEqZ0Eb8xNVmjKYGLGN71fM6Q5C+JuSIv9SMzfwIsLzq2StM25u8ribkil/r5D8VzxuumiZEEX+qAdbRYyVUJPGnGuARPbWPhGjiH2pAtLmeEia8JZ74Ew2IED2lv71RxZ9owFPDzruYkHMkvG9aVPEPGBAtevqacAE43/KzHuLvMyBq9BxmQttvdRu8xN9nQJSrnhwTSjyR8xT/rwGzWs3c1wRv8UcAK9SZ5bM0oUscRRB/BPAiwCD6tg+Mn1e0ZdD8j/e4RzXK00UmiiDfBugk7G4A6DLU3QDdiDkbAJqKcJ2KSGgyztmAqFE0N9PREC+K5uqBTCLKVdFcPpKEGFE01w/lQWUpXbZd1ABQYVafPooYoNLEf325lCaCinMTLsW5CZWnO5ang17QcH9BA/SKkrsBoJf03A3Qa6rOBkC8uaJZbp2JMlc0000/1uFMn7KUbeB+qYGI7iiKnCIooSjqQYnKOEVREBRFThGUUBTlU/SHWxVF+XwpXR29ATwrvM2jzMtaP1+fUwIyrwyBtVobvwF8J8BJLnBb76xuS+4BvwLsaMRWfQmTxG3gs/HORW4HFvGxWMZqhfEyVlcYnx9OGfQZianLWFku5LYAnGW8oNs8MXUhNyGEEEIIIYQQQghD/gCPRh6vZ78JXgAAAABJRU5ErkJggg==
"""

def icon_from_base64(data):
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(data))
    return pixmap

class ResizableIconButton(QPushButton):
    def __init__(self, pixmap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_pixmap = pixmap
        self.setIcon(QIcon(self._base_pixmap))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setObjectName("backspace_btn")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        side = min(size.width(), size.height())
        icon_size = QSize(int(side * 0.55), int(side * 0.55))  # иконка чуть меньше
        self.setIconSize(icon_size)

class MintCalculator(QMainWindow):
    ROUND_RADIUS = 5
    SPECIAL_CHARS = "+-*/%,"
    THEMES = {
        "Темно-зеленая": """
            QMainWindow { background-color: #2b3a20; color: white; }
            QLineEdit { background-color: #404040; color: white; border: none; font-size: 24px; }
            QPushButton {
                background-color: #454545; color: white;
                border: 1px solid #5a5a5a;
                border-radius: %dpx;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #686868;
            }
            QPushButton#equal_btn {
                background-color: #6db442;
                color: white;
            }
            QPushButton#equal_btn:hover {
                background-color: #7fd04c;
            }
            QPushButton#backspace_btn {
                background-color: #f04a50;
            }
            QPushButton#backspace_btn:hover {
                background-color: #ff4e57;
            }
            QToolBar {
                background-color: #334422;
                border: none;
            }
            QMenuBar {
                background-color: #334422;
                color: white;
            }
            QMenu {
                background-color: #2b3a20;
                color: white;
            }
            QMenu::item:selected {
                background-color: #5a8a3a;
                color: white;
            }
        """ % ROUND_RADIUS,

        "Светло-зеленая": """
            QMainWindow { background-color: #e6f0d6; color: black; }
            QLineEdit { background-color: #d8e7c8; color: black; border: none; font-size: 24px; }
            QPushButton {
                background-color: #d2e0b8; color: black;
                border: 1px solid #a0b05c;
                border-radius: %dpx;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #aed168;
            }
            QPushButton#equal_btn {
                background-color: #6db442;
                color: white;
            }
            QPushButton#equal_btn:hover {
                background-color: #7fd04c;
            }
            QPushButton#backspace_btn {
                background-color: #e55353;
                color: white;
            }
            QPushButton#backspace_btn:hover {
                background-color: #ff4e57;
            }
            QToolBar {
                background-color: #a4bc7d;
                border: none;
            }
            QMenuBar {
                background-color: #a4bc7d;
                color: black;
            }
            QMenu {
                background-color: #d8e7c8;
                color: black;
            }
            QMenu::item:selected {
                background-color: #a4bc7d;
                color: black;
            }
        """ % ROUND_RADIUS,

        "Темная": """
            QMainWindow { background-color: #3e3e3e; color: white; }
            QLineEdit { background-color: #404040; color: white; border: none; font-size: 24px; }
            QPushButton {
                background-color: #454545; color: white;
                border: 1px solid #5a5a5a;
                border-radius: %dpx;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #686868;
            }
            QPushButton#equal_btn {
                background-color: #6db442;
                color: white;
            }
            QPushButton#equal_btn:hover {
                background-color: #7fd04c;
            }
            QPushButton#backspace_btn {
                background-color: #f04a50;
            }
            QPushButton#backspace_btn:hover {
                background-color: #ff4e57;
            }
            QToolBar {
                background-color: #2f2f2f;
                border: none;
            }
            QMenuBar {
                background-color: #2f2f2f;
                color: white;
            }
            QMenu {
                background-color: #3e3e3e;
                color: white;
            }
            QMenu::item:selected {
                background-color: #5a5a5a;
                color: white;
            }
        """ % ROUND_RADIUS,

        "Светлая": """
            QMainWindow { background-color: #f0f0f0; color: black; }
            QLineEdit { background-color: #ffffff; color: black; border: none; font-size: 24px; }
            QPushButton {
                background-color: #e0e0e0; color: black;
                border: 1px solid #b0b0b0;
                border-radius: %dpx;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
            QPushButton#equal_btn {
                background-color: #6db442;
                color: white;
            }
            QPushButton#equal_btn:hover {
                background-color: #7fd04c;
            }
            QPushButton#backspace_btn {
                background-color: #e55353;
                color: white;
            }
            QPushButton#backspace_btn:hover {
                background-color: #ff4e57;
            }
            QToolBar {
                background-color: #d0d0d0;
                border: none;
            }
            QMenuBar {
                background-color: #d0d0d0;
                color: black;
            }
            QMenu {
                background-color: #ffffff;
                color: black;
            }
            QMenu::item:selected {
                background-color: #c0c0c0;
                color: black;
            }
        """ % ROUND_RADIUS,

        "Darcula Dark": """
            QMainWindow { background-color: #2b2b2b; color: #a9b7c6; }
            QLineEdit { background-color: #313335; color: #a9b7c6; border: none; font-size: 24px; }
            QPushButton {
                background-color: #3c3f41; color: #a9b7c6;
                border: 1px solid #555555;
                border-radius: %dpx;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #4e5254;
            }
            QPushButton#equal_btn {
                background-color: #689f38;
                color: white;
            }
            QPushButton#equal_btn:hover {
                background-color: #8bc34a;
            }
            QPushButton#backspace_btn {
                background-color: #b71c1c;
                color: white;
            }
            QPushButton#backspace_btn:hover {
                background-color: #d32f2f;
            }
            QToolBar {
                background-color: #212121;
                border: none;
            }
            QMenuBar {
                background-color: #212121;
                color: #a9b7c6;
            }
            QMenu {
                background-color: #2b2b2b;
                color: #a9b7c6;
            }
            QMenu::item:selected {
                background-color: #616161;
                color: #a9b7c6;
            }
        """ % ROUND_RADIUS,

        "Darcula Light": """
            QMainWindow { background-color: #f0f0f0; color: #3c3f41; }
            QLineEdit { background-color: #ffffff; color: #3c3f41; border: none; font-size: 24px; }
            QPushButton {
                background-color: #e0e0e0; color: #3c3f41;
                border: 1px solid #a0a0a0;
                border-radius: %dpx;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
            QPushButton#equal_btn {
                background-color: #689f38;
                color: white;
            }
            QPushButton#equal_btn:hover {
                background-color: #8bc34a;
            }
            QPushButton#backspace_btn {
                background-color: #e55353;
                color: white;
            }
            QPushButton#backspace_btn:hover {
                background-color: #ff4e57;
            }
            QToolBar {
                background-color: #d0d0d0;
                border: none;
            }
            QMenuBar {
                background-color: #d0d0d0;
                color: #3c3f41;
            }
            QMenu {
                background-color: #ffffff;
                color: #3c3f41;
            }
            QMenu::item:selected {
                background-color: #c0c0c0;
                color: #3c3f41;
            }
        """ % ROUND_RADIUS,
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mint Calculator")
        self.resize(355, 545)
        self.setMinimumSize(355, 545)

        self.current_theme = "Темно-зеленая"
        self.setStyleSheet(self.THEMES[self.current_theme])

        self._initUI()
        self._createMenu()
        self._connectShortcuts()

    def _initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(5, 5, 5, 0)
        v_layout.setSpacing(5)
        central_widget.setLayout(v_layout)

        self.input_field = QLineEdit()
        self.input_field.setReadOnly(True)
        self.input_field.setAlignment(Qt.AlignRight)
        self.input_field.setStyleSheet("background-color: #404040; color: white; font-size: 24px;")
        self.input_field.setFixedHeight(50)
        v_layout.addWidget(self.input_field)

        self.grid = QGridLayout()
        self.grid.setSpacing(6)
        v_layout.addLayout(self.grid)

        buttons_layout = [
            ["backspace", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ",", "%", "equal"]
        ]

        self.buttons = {}
        backspace_pixmap = icon_from_base64(bcspicon_base64)

        for row, row_data in enumerate(buttons_layout):
            for col, btn_text in enumerate(row_data):
                if btn_text == "backspace":
                    btn = ResizableIconButton(backspace_pixmap)
                    btn.setObjectName("backspace_btn")
                else:
                    btn = QPushButton()
                    btn.setFont(QFont("Segoe UI", 16))
                    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                    if btn_text == "equal":
                        btn.setText("=")
                        btn.setObjectName("equal_btn")
                    else:
                        btn.setText(btn_text)

                self.grid.addWidget(btn, row, col)
                self.buttons[btn_text] = btn

        for i in range(4):
            self.grid.setColumnStretch(i, 1)
        for i in range(5):
            self.grid.setRowStretch(i, 1)

        # Сигналы кнопок
        for key, btn in self.buttons.items():
            if key == "backspace":
                btn.clicked.connect(self._backspace)
            elif key == "equal":
                btn.clicked.connect(self._calculate)
            else:
                btn.clicked.connect(self._btn_clicked)

    def _createMenu(self):
        menubar = self.menuBar()
        self.setMenuBar(menubar)

        settings_menu = menubar.addMenu("Настройки")

        create_win_action = QAction("Создать окно", self)
        create_win_action.triggered.connect(self._create_new_window)
        settings_menu.addAction(create_win_action)
        settings_menu.addSeparator()

        theme_menu = QMenu("Выбор темы", self)
        settings_menu.addMenu(theme_menu)

        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)

        for theme_name in self.THEMES.keys():
            action = QAction(theme_name, self, checkable=True)
            if theme_name == self.current_theme:
                action.setChecked(True)
            action.triggered.connect(lambda checked, t=theme_name: self._change_theme(t))
            theme_menu.addAction(action)
            theme_group.addAction(action)

        settings_menu.addSeparator()

        about_action = QAction("О программе", self)
        about_action.triggered.connect(self._show_about)
        settings_menu.addAction(about_action)

        author_action = QAction("Об авторе", self)
        author_action.triggered.connect(self._show_author)
        settings_menu.addAction(author_action)

    def _connectShortcuts(self):
        shortcuts = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "+": "+", "-": "-", "*": "*", "/": "/",
            "%": "%", ",": ",",
            "(": "(", ")": ")",
            "Backspace": "backspace",
            "Return": "equal",
            "Enter": "equal"
        }
        for key, btn_key in shortcuts.items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(lambda k=btn_key: self._shortcut_pressed(k))


    def _shortcut_pressed(self, btn_key):
        if btn_key == "backspace":
            self._backspace()
        elif btn_key == "equal":
            self._calculate()
        else:
            self._add_to_input(btn_key)

    def _btn_clicked(self):
        sender = self.sender()
        for key, btn in self.buttons.items():
            if btn == sender:
                if key not in ("backspace", "equal"):
                    self._add_to_input(key)
                break

    def _add_to_input(self, char):
        text = self.input_field.text()

        # Запрет вводить "(" сразу после цифры
        if char == "(" and text and text[-1].isdigit():
            return

        # Запрет спецсимволов (кроме скобок) вводить более одного раза подряд
        if char in self.SPECIAL_CHARS:
            if text.endswith(char):
                return

        # При ошибке (ошибка в тексте) при вводе очищаем поле
        if "Ошибка" in text:
            self.input_field.clear()
            if char in self.SPECIAL_CHARS and char != "(":
                return

        self.input_field.setText(text + char)

    def _backspace(self):
        text = self.input_field.text()
        if text.endswith("Ошибка"):
            self.input_field.clear()
            return
        self.input_field.setText(text[:-1])

    def _calculate(self):
        expr = self.input_field.text().replace(",", ".")
        try:
            # Безопасный вычислитель, только базовые операции
            result = eval(expr, {"__builtins__": None}, {})
            if isinstance(result, float):
                result = round(result, 8)
            self.input_field.setText(str(result))
        except:
            self.input_field.setText("Ошибка")

    def _create_new_window(self):
        self.new_window = MintCalculator()
        self.new_window.show()

    def _change_theme(self, theme_name):
        self.current_theme = theme_name
        self.setStyleSheet(self.THEMES[theme_name])

    def _show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("О программе")
        dialog.setFixedSize(350, 150)

        layout = QVBoxLayout()
        label = QLabel(
            'MintCalculator 25.7.23 - калькулятор с дизайном linux mint, сделано I114rk,\n'
            '<a href="https://github.com/i114rk/mcalc" style="color:#4eaaff;">GitHub</a>'
        )
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)

        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec()

    def _show_author(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Об авторе")
        dialog.setFixedSize(350, 120)

        layout = QVBoxLayout()
        label = QLabel(
            'Автор - I114rk ©, Погребицкий Марк \n'
            '<a href="https://github.com/i114rk" style="color:#4eaaff;">GitHub</a>'
        )
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)

        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MintCalculator()
    window.show()
    sys.exit(app.exec_())
