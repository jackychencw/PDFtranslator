import os
from pdf2image import convert_from_path
import pytesseract
import PySimpleGUI as sg
from PyPDF2 import PdfFileReader, PdfFileWriter
from googletrans import Translator
# from baidu_trans import Translator
from fpdf import FPDF
workdir = os.getcwd()
poppler_path = "./packages/poppler-21.01.0/Library/bin"


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
    export_path = f"{home_dir}\Documents"
    file_list_row = [
        [
            sg.Text("PDF Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),)),
        ]
    ]

    # export_row = [
    #     [
    #         sg.Text("Export To: "),
    #         sg.In(size=(25, 1), enable_events=True, key="-EXPORT-", default_text=export_path),
    #         sg.FolderBrowse(),
    #     ]
    # ]

    layout = [
        [
            sg.Column(file_list_row),
            
        ],
        # [sg.Column(export_row)],
        [sg.Button('Translate', key="-TRANSLATE-")],
        [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
    ]

    window = sg.Window("Image Viewer", layout)


    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-FILE-":
            file = values["-FILE-"]
        if event == "-TRANSLATE-":
            if file:
                filename = file.split("/")[-1]
                filepath = file[:-len(filename)]
                clean_folder("tmp")
                make_dir("tmp")
                output_path=f'{filepath}/中文版{filename}'
                convert_pdf_to_txt(file, window=window, output=output_path)
                clean_folder("tmp")
            

def split_pdf(pdf, window = None):   
    tmp_path = "./tmp/pdf_split"
    make_dir(tmp_path)
    for i in range(pdf.numPages):
        progress = int(i/pdf.numPages * 500)
        if window:
            window['progbar'].update_bar(progress)
        output = PdfFileWriter()
        output.addPage(pdf.getPage(i))
        with open(f"{tmp_path}/tmp_pdf{i}.pdf", "wb") as outputStream:
            output.write(outputStream)
    return tmp_path

def clean_folder(path):
    if os.path.isfile(path):
        os.remove(path)
    else:
        if os.path.isdir(path):
            sub_paths = os.listdir(path)
            if len(sub_paths) == 0:
                os.rmdir(path)
            else:
                for sub_path in sub_paths:
                    clean_folder(f"{path}\{sub_path}")
                os.rmdir(path)


def translate(text, text_limit=10000):
    translator = Translator()
    
    translated_text = ""
    if len(text) >= text_limit:
        splited_texts = [text[i:i+text_limit] for i in range(0, len(text), text_limit)]
        for splited_text in splited_texts:
            translated_text += translator.translate(splited_text, dest="zh-cn").text
                        
    else:
        translated_text += translator.translate(text, dest="zh-cn").text
    return translated_text

    
def convert_pdf_to_txt(path, window = None,output="output.pdf", threshold=1, text_limit=10000):
    if os.path.exists(output):
        os.remove(output)
    pdf = FPDF() 
    pdf.add_page()
    pdf.add_font('fireflysung', '', 'fonts/fireflysung-1.3.0/fireflysung.ttf', uni=True)
    pdf.set_font('fireflysung', '', 8)
    
    check = PdfFileReader(open(path, 'rb'))
    translator = Translator()

    if check.numPages >= threshold:
        split_path = split_pdf(check, window=window)
        pdf_paths = os.listdir(split_path)
        p = 1
        for pdf_path in pdf_paths:
            progress = 500 + int(p/len(pdf_paths) * 500)
            if window:
                window['progbar'].update_bar(progress)
            p += 1
            images = convert_from_path(f"{split_path}/{pdf_path}", poppler_path = poppler_path, grayscale=True)
            for i in range(len(images)):
                text = pytesseract.image_to_string(images[i])
                translated_text = translate(text)
                
                pdf.write(4, txt = translated_text,) 
                pdf.ln(5)

            clean_folder(f"{split_path}/{pdf_path}")

        pdf.output(output)
    else:
        images = convert_from_path(path, poppler_path = poppler_path, grayscale=True)
        for i in range(len(images)):
            progress = 500 + int((i+1)/len(images) * 500)
            if window:
                window['progbar'].update_bar(progress)
            text = pytesseract.image_to_string(images[i])
            translated_text = translate(text)
                
            pdf.write(4, txt = translated_text,) 
            pdf.ln(5)

        pdf.output(output)
               

if __name__ == "__main__":
    # 
    # file_path = "./sample/sample.pdf"
    # 
    # 
    # convert_pdf_to_txt(file_path)
    # 

    launch_ui()
