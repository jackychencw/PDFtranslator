from pdf2image import convert_from_path
 

def convert_pdf_to_img(path):
    images = convert_from_path(path)
    return images

if __name__ == "__main__":
    path = "./sample/sample.pdf"
    images = convert_from_path(path)
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('page'+ str(i) +'.jpg', 'JPEG')