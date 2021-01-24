from pdf2image import convert_from_path


if __name__ == "__main__":
    poppler_path = "./packages/poppler-21.01.0/Library/bin"
    file_path = "./sample/sample.pdf"
    images = convert_from_path(file_path, poppler_path = poppler_path)
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('./tmp/page'+ str(i) +'.jpg', 'JPEG')