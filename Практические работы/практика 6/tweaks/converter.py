import docx2pdf
from pdf2docx import Converter

from .directory import is_linux
from aspose.words import Document


def convert_docx_to_pdf(docx: str, pdf: str):
    """
    Конвертация существующего документа docx в новый файл pdf
    :param docx: Путь до существующего файла docx
    :param pdf: Путь для нового файла
    """

    # docx2pdf не поддерживает linux, в отличие от aspose-words
    if not is_linux:
        docx2pdf.convert(input_path=docx, output_path=pdf)
    else:
        Document(docx).save(pdf)


def convert_pdf_to_docx(pdf: str, docx: str):
    """
    Конвертация существующего pdf файла в новый файл docx
    :param pdf: Путь до существующего pdf файла
    :param docx: Путь для нового файла docx
    """
    converter = Converter(pdf_file=pdf)
    converter.convert(docx_filename=docx)
