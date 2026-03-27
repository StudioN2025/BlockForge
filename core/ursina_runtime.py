from ursina import *
import subprocess
import sys
import os

def launch_ursina_window():
    """Запускает простой Ursina пример в отдельном процессе"""
    script = """
from ursina import *

app = Ursina()

player = Entity(model='cube', color=color.azure, scale=2)
ground = Entity(model='plane', scale=20, texture='grass', y=-2)

def update():
    player.x += (held_keys['d'] - held_keys['a']) * time.dt * 5
    player.z += (held_keys['w'] - held_keys['s']) * time.dt * 5

EditorCamera()
app.run()
"""
    # Сохраняем временный скрипт
    with open("temp_game.py", "w", encoding="utf-8") as f:
        f.write(script)

    # Запускаем в отдельном процессе
    process = subprocess.Popen([sys.executable, "temp_game.py"])
    return process
