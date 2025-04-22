#!/usr/bin/env python
import os
import shutil
from pathlib import Path

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Исходная директория с изображениями
src_dir = BASE_DIR / 'static' / 'img' / 'recipes'

# Целевая директория для изображений
target_dir = BASE_DIR / 'media' / 'recipes'

# Создаем целевую директорию, если она не существует
os.makedirs(target_dir, exist_ok=True)

# Копируем все файлы из исходной директории в целевую
for file_name in os.listdir(src_dir):
    if file_name.endswith('.jpg') or file_name.endswith('.png'):
        src_file = os.path.join(src_dir, file_name)
        dst_file = os.path.join(target_dir, file_name)
        shutil.copy2(src_file, dst_file)
        print(f"Скопирован файл: {file_name}")

print("Копирование завершено!") 