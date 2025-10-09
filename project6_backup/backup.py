import os
import zipfile
from datetime import datetime
import logging
import sys

# Настройка логирования
logging.basicConfig(
    filename="backup.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def create_backup(src_folder: str, dest_folder: str):
    """Создание ZIP-архива с резервной копией"""

    if not os.path.exists(src_folder):
        logging.error(f"Исходная папка не найдена: {src_folder}")
        raise FileNotFoundError(f"Исходная папка не найдена: {src_folder}")

    if not os.path.exists(dest_folder):
        try:
            os.makedirs(dest_folder, exist_ok=True)
            logging.info(f"Создана папка назначения: {dest_folder}")
        except Exception as e:
            logging.error(f"Ошибка при создании папки назначения: {e}")
            raise

    # Имя архива с датой и временем
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"backup_{timestamp}.zip"
    archive_path = os.path.join(dest_folder, archive_name)

    try:
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(src_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, src_folder)
                    try:
                        zipf.write(file_path, rel_path)
                        logging.info(f"Добавлен файл: {file_path} → {rel_path}")
                    except Exception as e:
                        logging.error(f"Ошибка при добавлении файла {file_path}: {e}")
        logging.info(f"Архив успешно создан: {archive_path}")
        print(f"✅ Резервная копия создана: {archive_path}")
    except Exception as e:
        logging.error(f"Ошибка при создании архива: {e}")
        print("❌ Ошибка при создании архива:", e)


def main():
    print("=== Утилита резервного копирования ===")
    src = input("Введите путь к исходной папке: ").strip()
    dest = input("Введите путь для сохранения архива: ").strip()
    try:
        create_backup(src, dest)
    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()