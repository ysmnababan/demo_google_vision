from google.cloud import vision

client = vision.ImageAnnotatorClient()

# Load the image
with open("./img/pekerjaan.png", "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)
response = client.document_text_detection(image=image)

# Parse result
lines = []

for page in response.full_text_annotation.pages:
    for block in page.blocks:
        for paragraph in block.paragraphs:
            line_text = ""
            min_y = min(v.y for word in paragraph.words for v in word.bounding_box.vertices)
            words = sorted(paragraph.words, key=lambda w: min(v.x for v in w.bounding_box.vertices))
            for word in words:
                word_text = "".join([symbol.text for symbol in word.symbols])
                line_text += word_text + " "
            lines.append((min_y, line_text.strip()))

# Group similar Y positions into rows
lines.sort(key=lambda x: x[0])
grouped_rows = []
current_y = None
current_row = []

for y, text in lines:
    if current_y is None or abs(y - current_y) < 10:
        current_row.append(text)
        current_y = y
    else:
        grouped_rows.append(current_row)
        current_row = [text]
        current_y = y
if current_row:
    grouped_rows.append(current_row)

# Print output
for row in grouped_rows:
    print(" | ".join(row))
