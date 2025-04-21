from google.cloud import vision
import io

def detect_text(image_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # You can also use client.text_detection() for simpler cases
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text

    print("Detected text:\n", text)

    if response.error.message:
        raise Exception(response.error.message)

# Example usage
detect_text("./img/table_1_17.png")