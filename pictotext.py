import pytesseract
import urllib.request
from PIL import Image

urllib.request.urlretrieve('https://templates.invoicehome.com/receipt-template-us-band-blue-750px.png', 'temp.png')

# Open the image file
image = Image.open('temp.png')

# Perform OCR using PyTesseract
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)