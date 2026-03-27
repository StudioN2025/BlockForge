from PyQt6.QtCore import QObject, pyqtSlot

class BlocklyBridge(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    @pyqtSlot(str)
    def onCodeChanged(self, code):
        print("Блоки изменились, код:", code[:200] + "..." if len(code) > 200 else code)
