from pdf2image import convert_from_path
 

def convert_pdf_to_img(path):
    images = convert_from_path(path)
    return images



 


if __name__ == "__main__":
    print("hello world")