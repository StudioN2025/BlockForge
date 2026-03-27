from PyQt6.QtWidgets import (
    QMainWindow, QSplitter, QWidget, QVBoxLayout, 
    QPushButton, QHBoxLayout, QLabel, QTextEdit
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from editor.blockly_bridge import BlocklyBridge
from core.ursina_runtime import launch_ursina_window
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Block3D Engine - Python 3D с блоками")
        self.resize(1400, 900)

        # Главный сплиттер
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # === Левая панель: Blockly ===
        self.blockly_view = QWebEngineView()
        self.channel = QWebChannel()
        self.bridge = BlocklyBridge(self)
        self.channel.registerObject("pythonBridge", self.bridge)
        self.blockly_view.page().setWebChannel(self.channel)

        # Загружаем локальный HTML
        current_dir = os.path.dirname(os.path.abspath(__file__))
        web_path = os.path.join(current_dir, "..", "web", "index.html")
        self.blockly_view.setUrl(QUrl.fromLocalFile(web_path))

        # === Правая панель: Инспектор + сгенерированный код ===
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.code_text = QTextEdit()
        self.code_text.setReadOnly(True)
        right_layout.addWidget(QLabel("Сгенерированный Python код:"))
        right_layout.addWidget(self.code_text)

        btn_layout = QHBoxLayout()
        self.btn_generate = QPushButton("Сгенерировать код")
        self.btn_run = QPushButton("Запустить игру")
        self.btn_stop = QPushButton("Остановить")

        self.btn_generate.clicked.connect(self.generate_code)
        self.btn_run.clicked.connect(self.run_game)
        self.btn_stop.clicked.connect(self.stop_game)

        btn_layout.addWidget(self.btn_generate)
        btn_layout.addWidget(self.btn_run)
        btn_layout.addWidget(self.btn_stop)
        right_layout.addLayout(btn_layout)

        self.splitter.addWidget(self.blockly_view)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([900, 500])

        self.setCentralWidget(self.splitter)

        self.ursina_process = None

    def generate_code(self):
        # Вызываем JS функцию для получения кода
        self.blockly_view.page().runJavaScript("getGeneratedPythonCode()", self.on_code_received)

    def on_code_received(self, code):
        if code:
            self.code_text.setPlainText(code)
            print("=== Сгенерированный код ===\n", code)
            # Можно сохранить в файл projects/current_game.py
        else:
            print("Код не получен")

    def run_game(self):
        self.generate_code()  # сначала обновляем код
        # Запускаем Ursina в отдельном окне
        self.ursina_process = launch_ursina_window()
        print("Ursina запущена в отдельном окне")

    def stop_game(self):
        if self.ursina_process:
            # Здесь будет нормальное завершение процесса позже
            print("Остановка игры (пока просто сообщение)")
