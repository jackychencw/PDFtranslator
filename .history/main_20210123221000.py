import os
from pdf2image import convert_from_path
from google.cloud import vision
import io

def make_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def detect_text(path):
    """Detects text in the file."""
    
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

if __name__ == "__main__":
    poppler_path = "./packages/poppler-21.01.0/Library/bin"
    file_path = "./sample/sample.pdf"
    images = convert_from_path(file_path, poppler_path = poppler_path)
    make_dir("tmp")
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('./tmp/page'+ str(i) +'.jpg', 'JPEG')