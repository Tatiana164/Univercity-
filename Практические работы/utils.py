import random

def load_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = file.readlines()
            words = [word.strip() for word in words]
            return words
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

def save_record(file_path, record):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(record))
    except Exception as e:
        print(f"Ошибка при записи рекорда: {e}")

def load_record(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            record = int(file.read().strip())
            return record
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return 0
    except Exception as e:
        print(f"Ошибка при чтении рекорда: {e}")
        return 0