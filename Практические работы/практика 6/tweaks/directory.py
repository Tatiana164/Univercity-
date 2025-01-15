from os.path import isdir, isfile, exists
from os import listdir
from sys import platform

is_linux = platform == "linux"
split_slash_platform = "\\" if "win" in platform.lower() else "/"
slash_platform = "/"
current_directory = slash_platform.join(__file__.split(split_slash_platform)[:-2])


def show_current_directory():
    """
    Показать текущий рабочий каталог
    """
    print(f"Текущий каталог: {current_directory}")


def is_dir(dir_path: str) -> bool:
    """
    Проверка, что путь указывает на директорию
    :param dir_path: Путь для проверки
    :return: указывает ли путь на директорию
    """
    return isdir(dir_path)


def is_file(file_path: str) -> bool:
    """
    Проверка, что путь указывает на файл
    :param file_path: Путь для проверки
    :return: указывает ли путь на файл
    """
    return isfile(file_path)


def is_exist(path: str) -> bool:
    """
    Проверка, что путь существует
    :param path: Путь для проверки существования
    :return: существует ли путь
    """
    return exists(path)


def is_exist_format_file(file: str) -> bool:
    """
    Проверка, что у файла существует расширение
    :param file: Путь до файла
    :return: существует ли расширение у файла
    """
    return file.rfind(".") != -1


def get_format_file(file: str) -> str:
    """
    Возвращает расширение переданного файла
    :param file: Путь до файла
    :return: расширение файла
    """
    return file[file.rfind(".") + 1:]


def remove_format(file: str) -> str:
    """
    Удалить расширение (с точкой) из названия/пути файла
    :param file: Название/путь файла
    :return: название/путь без расширения
    """
    return file[:file.rfind(".")]


def change_format_file(file: str, new_format: str) -> str:
    """
    Изменяет расширение у названия/пути файла
    :param file: Название/путь файла
    :param new_format: Новое расширение файла
    :return: название/путь с новым расширением файла
    """
    return file[:file.rfind(".") + 1] + new_format


def append_postfix_file(file: str, postfix: str) -> str:
    """
    Добавляет перед точкой в название/пути файла постфикс
    :param file: Название/путь файла
    :param postfix: Постфикс для добавления
    :return: название/путь с постфиксом
    """
    parts = file.split(slash_platform)
    filename = parts[-1]
    filename = filename[:filename.rfind(".")] + postfix + filename[filename.rfind("."):]
    return slash_platform.join(parts[:-1] + [filename])


def get_file_path(filename: str):
    """
    Получение пути файла из текущей рабочей директории
    :param filename: Название файла
    :return: путь до файла
    """
    return f"{current_directory}{slash_platform}{filename}"


def get_files(format_file: list, do_raise=False) -> list[str]:
    """
    Получение списка файлов определенного расширения из текущей рабочий директории
    :param do_raise: выводить ли ошибки
    :param format_file: Список расширений
    :return: список файлов
    """
    files = listdir(current_directory)
    return [
        file for file in files
        if is_valid_file(f"{current_directory}{slash_platform}{file}", format_file, do_raise)
    ]


def is_valid_directory(directory_path: str) -> bool:
    """
    Проверка на то, существует ли путь и этот путь указывает на директорию
    :param directory_path: Путь для проверки
    :return: существует ли путь и указывает ли он на папку
    """
    if not is_exist(directory_path):
        raise Exception(f"Ошибка! Директория {directory_path} не найдена")
    if not is_dir(directory_path):
        raise Exception(f"Ошибка! Путь {directory_path} указывает не на директорию")
    return True


def is_valid_file(file_path: str, file_format: list, do_raise: bool = False) -> bool:
    """
    Проверка на то, существует ли путь, указывает ли он на файл определенного формата
    :param do_raise: выдавать ли ошибки
    :param file_path: путь для проверки
    :param file_format: список расширений
    :return: существует ли путь, указывает ли он на файл определенного формата
    """

    if not is_exist(file_path):
        if do_raise:
            raise Exception(f"Ошибка! Файл {file_path} не найден")
        return False
    if not is_file(file_path):
        if do_raise:
            raise Exception(f"Ошибка! Путь {file_path} указывает не на файл")
        return False
    if len(file_format) != 0:
        if not is_exist_format_file(file_path):
            if do_raise:
                raise Exception(f"Файл {file_path} не имеет формата")
            return False
        if get_format_file(file_path) not in file_format:
            if do_raise:
                raise Exception(f"Файл {file_path} не имеет нужный формат {file_format}")
            return False
    return True


def change_directory(new_directory: str) -> bool:
    """
    Смена текущей рабочей директории
    :param new_directory: Путь до новой директории
    :return: произошла ли смена директории
    """
    global current_directory
    if not is_valid_directory(new_directory):
        return False

    current_directory = new_directory
    return True
