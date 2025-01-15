from PIL import Image


def compress(image_path: str, output_path: str, quality=90):
    """
    Сжатие изображения и сохранения в виде нового файла
    :param image_path: Путь до оригинальной картинки
    :param output_path: Путь для нового файла со сжатым изображением
    :param quality: Разрешение сжатия
    """
    Image.open(image_path).convert("RGB").save(output_path, quality=quality, optimize=True)
