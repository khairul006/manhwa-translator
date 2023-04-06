# BUILT ON 3/4/2023 AT 9.00PM BY KHAIRUL NAISU AND CHATGPT
# PROGRAM TAKE IMAGE AND SCAN FOR TEXT IN THAT IMAGE. USING GOOGLE TRANSLATOR TO TRANSLATE THE TEXT
# FOR THIS GOOGLE API KEY MUST CONNECTED TO USE ITS FEATURES ------ NEED YOUR API KEY CHECK THE CODE
# THE TRANSLATED TEXT WILL OVERWRITE ON THE ORIGINAL TEXT IMAGE 

import pytesseract
import requests
from PIL import Image, ImageDraw, ImageFont
import re
import tkinter as tk
from tkinter import filedialog
from googletrans import LANGUAGES, Translator

# Open a file dialog to select an image file
root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename(title="Select Image File", filetypes=(("JPEG Files", "*.jpg"), ("PNG Files", "*.png"), ("All Files", "*.*")))
root.destroy()

# Load the image
try:
    image = Image.open(filename)
except IOError:
    print("Cannot open image file. Please check the filename and try again.")
    exit()

# Convert the image to grayscale
image = image.convert('L')

# Set the OCR engine and its configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 6'

# Perform OCR using Tesseract OCR
text = pytesseract.image_to_string(image, lang='kor', config=custom_config)

# Define the regular expression pattern to match the Korean text in speech bubbles
pattern = r'\n\s*(.+?)\s*\n'

# Find all matches of the pattern in the text
matches = re.findall(pattern, text)

# Translate the matched text to English using Google Translate API
translator = Translator(service_urls=['translate.google.com'])
API_KEY = 'YOUR_API_KEY_HERE'
headers = {'Authorization': 'Bearer %s' % API_KEY}
for match in matches:
    try:
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            'q': match,
            'target': 'en',
            'source': 'ko'
        }
        response = requests.post(url, headers=headers, params=params)
        translated_text = response.json()['data']['translations'][0]['translatedText']
    except:
        translated_text = "Error: Unable to translate text."
    
    # Print the original and translated text to the console
    print(f"Korean: {match}")
    print(f"English: {translated_text}")
    
    # Draw the translated text on the image
    if translated_text:
        font = ImageFont.truetype("arial.ttf", 14)
        draw = ImageDraw.Draw(image)
        draw.text((50, 50), translated_text, font=font, fill='white')

# Save the modified image
new_filename = filedialog.asksaveasfilename(title="Save Modified Image As", defaultextension=".png", filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")))
if new_filename:
    image.save(new_filename)

# Display a message if no matches were found
if not matches:
    print("No Korean text detected in the image.")
