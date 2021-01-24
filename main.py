import os
from pdf2image import convert_from_path
import pytesseract
import PySimpleGUI as sg
from PyPDF2 import PdfFileReader
from googletrans import Translator

pytesseract.tesseract_cmd = './packages/tesseract-ocr/tesseract.exe'


def make_dir(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)


def launch_ui():
    home_dir = os.path.expanduser("~")
    file_list_row = [
        [
            sg.Text("PDF Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),)),
        ]
    ]

    export_row = [
        [
            sg.Text("Export To: "),
            sg.In(size=(25, 1), enable_events=True, key="-EXPORT-", default_text=f"{home_dir}\Documents"),
            sg.FolderBrowse(),
        ]
    ]

    layout = [
        [
            sg.Column(file_list_row),
            
        ],
        [sg.Column(export_row)],
        [sg.Button('Translate')]
    ]

    window = sg.Window("Image Viewer", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-FILE-":
            file = values["-FILE-"]
        if event == "-EXPORT-":
            export_path = values["-EXPORT-"]
            

def split_pdf(pdf):
    from PyPDF2 import PdfFileWriter
    tmp_path = "tmp/pdf_split"
    make_dir(tmp_path)
    for i in range(pdf.numPages):
        output = PdfFileWriter()
        output.addPage(pdf.getPage(i))
        with open(f"{tmp_path}/tmp_pdf{i}.pdf", "wb") as outputStream:
            output.write(outputStream)
    return tmp_path

def convert_pdf_to_txt(path, threshold=1):
    check = PdfFileReader(open(path, 'rb'))
    translator = Translator()
    if check.numPages >= threshold:
        split_path = split_pdf(check)
        pdf_paths = os.listdir(split_path)
        f = open("./tmp/tmp.txt", "a")
        for pdf_path in pdf_paths:
            images = convert_from_path(f"{split_path}/{pdf_path}", poppler_path = poppler_path, grayscale=True)
            for i in range(len(images)):
                text = pytesseract.image_to_string(images[i])
                translations = translator.translate("hi", dest="zh-cn")
                # f.write(text)

            

if __name__ == "__main__":
    poppler_path = "./packages/poppler-21.01.0/Library/bin"
    file_path = "./sample/sample.pdf"
    make_dir("tmp")
    convert_pdf_to_txt(file_path)
    # images = convert_from_path(file_path, poppler_path = poppler_path, grayscale=True)
    # print("Done Converting")
    # make_dir("tmp")
    # f = open("./tmp/tmp.txt", "a")

    # for i in range(len(images)):
    #     # Save pages as images in the pdf
    #     text = pytesseract.image_to_string(images[i])
    #     f.write(text)

    # launch_ui()
