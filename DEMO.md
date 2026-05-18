# Project Demo & Deployment

This project is best demonstrated as a desktop AI application rather than a normal hosted website.

## Why desktop deployment is best

The Student Attention Monitoring System relies on:

- webcam access
- real-time computer vision
- audio / voice alerts
- YOLO + MediaPipe processing

Because of these requirements, the best deployment option is:

✅ **Desktop AI Application**

This is ideal for:

- project demo
- viva presentation
- portfolio showcase
- accessibility demonstrations

## Best Deployment Options

| Option | Recommended | Difficulty |
|---|---|---|
| Local Desktop App | ✅ BEST | Easy |
| Streamlit Web App | ✅ Good | Medium |
| Flask Local Server | ✅ Good | Medium |
| Cloud Deployment | ❌ Not ideal for webcam AI | Hard |

## OPTION 1 — Run Locally (Recommended)

This is the best way to demo the app.

Run the project:

```powershell
python main.py
```

## OPTION 2 — Convert Into EXE Application

You can create a distributable EXE so anyone can run it without Python.

1. Install PyInstaller:

```powershell
pip install pyinstaller
```

2. Generate the EXE:

```powershell
pyinstaller --onefile --windowed main.py
```

✅ After completion, the output will be in:

```text
dist/main.exe
```

Then you can share the executable with teachers, classmates, or include it in your portfolio.

## OPTION 3 — Streamlit Web Interface (Modern UI)

If you want a browser-based interface, you can build a Streamlit app.

1. Install Streamlit:

```powershell
pip install streamlit
```

2. Run the app:

```powershell
streamlit run app.py
```

3. Deploy to services like Streamlit Community Cloud or Render.

⚠️ Important limitation:

Browser deployments may have issues with webcam permissions, real-time voice alerts, and heavy YOLO processing.

## Recommended final project structure

```text
Student-Attention-Monitoring-System/
│
├── main.py
├── requirements.txt
├── README.md
├── DEMO.md
├── screenshots/
├── demo-video.mp4
└── dist/
    └── main.exe
```

## Notes

- Local desktop deployment is the most professional and easiest demo method.
- Use GitHub for source code, screenshots, README, and demo videos.
- For this project, the best approach is:

✅ **EXE Desktop Application + GitHub**

That is the easiest presentation-ready solution for interviews and college demos.
