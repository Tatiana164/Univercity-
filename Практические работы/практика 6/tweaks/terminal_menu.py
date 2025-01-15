from sys import exit
from typing import Callable

from .compressor import compress
from .converter import convert_docx_to_pdf, convert_pdf_to_docx
from .directory import show_current_directory, change_directory, get_files, change_format_file, get_file_path, \
    append_postfix_file, get_format_file, remove_format
from os import remove


def item_menu_change_current_directory():
    """
    Пункт главного меню для смены директории
    """
    inp_user = input_with_exit("Укажите корректный путь к рабочему каталогу")
    if inp_user is None:
        return
    change_directory(inp_user)


def item_menu_convert(inp: str, out: str, converter):
    """
    Пункт главного меню для конвертаций
    :param inp: из чего конвертировать
    :param out: в что конвертировать
    :param converter: функция конвертирования
    """
    files = get_files(format_file=[inp])

    def fun(index_file: int):
        file_path = get_file_path(files[index_file])
        output_file = change_format_file(file_path, out)
        print("Ожидайте...")
        converter(file_path, output_file)
        print(f"Готово. Создан {output_file}")

    choose_file(fun, files, [inp])


def item_menu_compress_image():
    """
    Пункт главного меню для сжатия изображения
    """
    formats = ["png", "jpg", "jpeg", "gif"]
    files = get_files(formats)

    def fun(index_file: int):
        file_path = get_file_path(files[index_file])
        output_file_path = append_postfix_file(file_path, "_compress")
        while True:
            try:
                inp = input_with_exit("Введите параметр сжатия (от 0 до 100%)")
                if inp is None:
                    return
                quality = int(inp)
                if not (0 <= quality <= 100):
                    print("Введите число от 0 до 100")
                    continue
                break
            except ValueError:
                print("Введите только число от 0 до 100")

        compress(file_path, output_file_path, quality)
        print(f"Сжатия выполнено - {output_file_path}")

    choose_file(fun, files, formats)


def item_menu_delete_group_files():
    """
    Пункт главного меню для группового удаления файлов
    """
    files = get_files([])
    if len(files) == 0:
        print("Файлы в текущей директории отсутствуют!")
        return

    def delete_file_substring(validation_fun: Callable):
        """
        Пункт подменю группового удаления для удаления по подстроке
        :param validation_fun: функция валидации, принимающая имя файла и подстроку
        """
        substring = input("Введите подстроку: ").lower()
        target_files = [file for file in files if validation_fun(remove_format(file.lower()), substring)]
        if len(target_files) == 0:
            print("Файлов на удаление не найдено!")
            return
        delete_files(target_files)

    def delete_file_format():
        """
        Пункт подменю группового удаления для удаления по расширению
        """
        format_file = input("Введите формат файлов: ")
        target_files = [file for file in files if get_format_file(file) == format_file]
        delete_files(target_files)

    def delete_files(target_files: list[str]):
        """
        Удаление списка файлов
        :param target_files: список файлов
        """
        for file in target_files:
            path_file = get_file_path(file)
            remove(path_file)
        print(f"{'Файл удален:' if len(target_files) == 1 else 'Файлы удалены:'} {target_files}")

    menu_delete = {
        "Удалить все файлы начинающиеся на определенную подстроку":
            lambda: delete_file_substring(lambda file, substring: file.startswith(substring)),
        "Удалить все файлы заканчивающиеся на определенную подстроку":
            lambda: delete_file_substring(lambda file, substring: file.endswith(substring)),
        "Удалить все файлы содержащиеся определенную подстроку":
            lambda: delete_file_substring(lambda file, substring: substring in file),
        "Удалить все файлы по расширению": delete_file_format,
    }

    show_menu(menu_delete)
    func_item_menu, _ = safe_choose_item_menu(menu_delete)
    func_item_menu()


def choose_file(fun, files: list[str], formats: list[str]):
    files_menu = {file: fun for file in files}
    if len(files_menu) == 0:
        print(f"Файлов с расширением {formats} в рабочем каталоге не найдено")
        return

    show_menu(files_menu)
    func, index = safe_choose_item_menu(files_menu)
    func(index)


menu = {
    "Сменить рабочий каталог": item_menu_change_current_directory,
    "Преобразовать PDF в Docx": lambda: item_menu_convert("pdf", "docx", convert_pdf_to_docx),
    "Преобразовать Docx в PDF": lambda: item_menu_convert("docx", "pdf", convert_docx_to_pdf),
    "Произвести сжатие изображения": item_menu_compress_image,
    "Удалить группу файлов": item_menu_delete_group_files,
    "Выход": exit,
}


def show_main_menu():
    """
    Показать главное меню
    """
    show_menu(menu)


def show_menu(local_menu: dict):
    """
    Показать переданное меню
    :param local_menu: меню в виде словаря 
    """
    print("-" * 15 + "МЕНЮ" + "-" * 15)
    show_current_directory()
    print("\n".join(f"{i}. {e}" for i, e in enumerate(local_menu)))


def choose_main_menu():
    """
    Предоставить выбор пункта из главного меню
    """
    func_item_menu, _ = safe_choose_item_menu(menu)
    func_item_menu()


def safe_choose_item_menu(local_menu: dict[str, Callable[[], None]]) -> (Callable[[], None], int):
    """
    Безопасное получение пункта выбранного пользователем
    :param local_menu: меню для выбора
    :return: функция меню пункта, которого выбрал пользователь
    """
    while True:
        try:
            usr_input = input("Введите индекс пункта меню: ")
            if usr_input is None:
                return lambda: None, -1
            index_item_menu = int(usr_input)
            return local_menu[list(local_menu.keys())[index_item_menu]], index_item_menu
        except ValueError:
            print("Ошибка! Введите число")
        except KeyError:
            print(f"Ошибка! Введите индекс меню от 0 до {len(local_menu)} включительно")


def input_with_exit(text: str) -> str | None:
    """
    Пользовательский ввод с возможностью отмены (exit)
    :param text: текст для input
    :return: текст пользователя или None в случаях выхода
    """
    usr_input = input(f"{text} (exit - для выхода): ")
    if usr_input == "exit":
        return None
    return usr_input
