import cv2
import pytesseract
import pandas as pd
import time
import re
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 Set up Tesseract OCR (Ensure correct path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 🔹 Load Haar cascade for number plate detection
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# 🔹 Google Sheets API Setup
json_key_path = r"C:\Users\karthikeyan\vino file\google_sheets_key.json"  # ✅ Ensure correct filename and path!

# Check if the file exists before proceeding
if not os.path.exists(json_key_path):
    raise FileNotFoundError(f"Error: {json_key_path} not found! Check the file path.")

# Authenticate Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
client = gspread.authorize(creds)

# 🔹 Open the Google Sheet (Replace with your actual sheet name)
try:
    sheet_name = "Vehicle Tracking Data"  # Ensure this is the correct sheet name
    try:
        sheet = client.open(sheet_name).sheet1
    except gspread.SpreadsheetNotFound:
        raise Exception(f"Error: Google Sheet '{sheet_name}' not found! Check the sheet name.")
except gspread.SpreadsheetNotFound:
    raise Exception("Error: Google Sheet not found! Check the sheet name.")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Error: Could not open video device. Please check if the camera is connected and accessible.")

# Create an empty DataFrame to store extracted number plates
data = pd.DataFrame(columns=["Timestamp", "Number Plate"])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect number plates
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in plates:
        roi = frame[y:y+h, x:x+w]
        gray_plate = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # OCR to extract text
        number_plate_text = pytesseract.image_to_string(gray_plate, config='--psm 7')

        # Clean the OCR output (remove unwanted characters)
        number_plate_text = re.sub(r'[^A-Z0-9-]', '', number_plate_text.strip())

        if number_plate_text:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Detected: {number_plate_text} at {timestamp}")

            # Save to DataFrame (local storage)
            data = pd.concat([data, pd.DataFrame([[timestamp, number_plate_text]], 
                                                  columns=["Timestamp", "Number Plate"])], ignore_index=True)

            # Save data to Google Sheets
            try:
                sheet.append_row([timestamp, number_plate_text])
            except Exception as e:
                print(f"Error: Could not append data to Google Sheets. {e}")

        # Draw rectangle around detected number plate
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Vehicle Number Plate Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save extracted data to an Excel sheet (local backup)
data.to_excel("Vehicle_Number_Plates.xlsx", index=False)
print("✅ Data successfully saved to Google Sheets and Excel!")