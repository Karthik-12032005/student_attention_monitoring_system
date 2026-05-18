# Student Attention Monitoring System

A Windows-based student attention monitoring application using webcam data to detect drowsiness, phone usage, speaking, and face absence.

## Features

- Real-time face and eye landmark detection with MediaPipe
- Drowsiness detection using Eye Aspect Ratio (EAR)
- Phone detection using YOLOv8 and a pretrained model file
- Speaking and mouth-open detection via lip landmarks
- Absence detection when no face is visible
- Voice notifications using `pyttsx3`

## Requirements

- Python 3.8+
- Webcam access
- Windows OS (for `pyttsx3` SAPI5 support)
- `yolov8n.pt` model file included in repository

## Setup

From PowerShell in the project directory:

```powershell
.\deploy.ps1
```

Or manually:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe main.py
```

## Demo & Deployment

This project works best as a desktop AI application because it uses real-time webcam access, YOLO + MediaPipe, and voice alerts.

A full demo guide is available in `DEMO.md` with:

- local desktop app deployment
- EXE packaging with PyInstaller
- Streamlit web interface notes
- cloud deployment caveats

## GitHub Actions CI

This repository includes a Windows-based GitHub Actions workflow that:

- installs Python dependencies
- validates Python source files with `py_compile`

## Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for guidelines on how to submit issues and pull requests.

## Notes

- The application uses the local YOLO model file `yolov8n.pt`.
- If you do not have a webcam attached, the application may not start correctly.
- The `deploy.ps1` script sets up a virtual environment and starts the app.
