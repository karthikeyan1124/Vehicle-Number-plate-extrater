
# 🚗 Vehicle Number Plate Detection System

This project detects vehicle number plates in real time using **YOLOv8** and **EasyOCR**, and logs detected plates into **Google Sheets** for tracking.

<img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python Badge"> <img src="https://img.shields.io/badge/OpenCV-4.x-green" alt="OpenCV Badge"> <img src="https://img.shields.io/badge/EasyOCR-%3E%3D1.6.2-brightgreen" alt="EasyOCR Badge"> <img src="https://img.shields.io/badge/YOLOv8-ultralytics-red" alt="YOLOv8 Badge">

## 🎥 Features
- Real-time number plate detection (via webcam or video)
- Accurate OCR using EasyOCR
- Stores detected plates & timestamp to Google Sheets
- Supports YOLOv8 detection (optimized for CPU)

## 🛠️ Tech Stack
- Python 3.9+
- OpenCV
- EasyOCR
- Ultralytics YOLOv8
- Google Sheets API (gspread + service account)

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
Sample `requirements.txt`:
```
opencv-python
easyocr
ultralytics
gspread
oauth2client
```

### 3️⃣ Prepare Google Sheets API
- Create a **Service Account** from Google Cloud Console
- Download the `google_sheets_key.json` file
- Share your Google Sheet with the service account email
- The sheet name should be: `Vehicle Tracking Data`

### 4️⃣ Run the Application
```bash
python app1.py
```

## 📄 Files
- `app1.py` — main application
- `yolov8n.pt` — YOLOv8n model weights
- `Vehicle_Number_Plates.xlsx` — sample data file
- `google_sheets_key.json` — your API credentials (NOT included in repo)

## 🎬 Demo
![Screenshot 2025-03-16 082949](https://github.com/user-attachments/assets/2ce8e2fe-fae0-4096-932d-55feff92c27f)


## ✏️ How It Works
1. Captures frames from webcam
2. YOLOv8 detects number plates
3. EasyOCR extracts text
4. Detected number & timestamp saved to Google Sheet
5. Live feed displayed with bounding boxes

## 🛡️ License
MIT License — feel free to use and improve!
