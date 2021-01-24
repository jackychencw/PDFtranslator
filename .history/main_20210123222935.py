import os
from pdf2image import convert_from_path
from packages import pytesseract

def make_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)


if __name__ == "__main__":
    # poppler_path = "./packages/poppler-21.01.0/Library/bin"
    # file_path = "./sample/sample.pdf"
    # images = convert_from_path(file_path, poppler_path = poppler_path)
    # make_dir("tmp")
    # for i in range(len(images)):
    #     # Save pages as images in the pdf
    #     images[i].save('./tmp/page'+ str(i) +'.jpg', 'JPEG')
    print(pytesseract.image_to_string('./tmp/page0.jpg'))