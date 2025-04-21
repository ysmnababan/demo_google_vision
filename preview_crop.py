from google.cloud import vision
import io
import cv2
import numpy as np

def preview_and_crop_blocks(image_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    # Load image with OpenCV
    img = cv2.imread(image_path)

    count = 0
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            box = block.bounding_box.vertices
            x_coords = [v.x for v in box]
            y_coords = [v.y for v in box]

            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            # Draw rectangle on image for preview
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            count += 1

    # Show the image with rectangles
    print(f"Detected and marked {count} blocks. Press any key to close preview.")
    cv2.imshow("Detected Text Blocks", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

preview_and_crop_blocks("./img/warped.png")
