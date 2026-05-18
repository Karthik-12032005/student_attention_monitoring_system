# Contributing

Thank you for your interest in contributing to Student Attention Monitoring System!

## How to contribute

1. Fork the repository.
2. Create a new branch for your change:
   ```powershell
git checkout -b feature/my-change
```
3. Install dependencies and verify the application runs locally.
4. Make your changes.
5. Commit with a clear message.
6. Push your branch and open a pull request.

## Development setup

Use the existing deployment helper to set up the environment:

```powershell
.\deploy.ps1
```

If you prefer manual setup:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Code guidelines

- Keep Python code readable and straightforward.
- Use descriptive variable names.
- Avoid committing large model files or generated binaries.
- Test changes locally before submitting.

## Issues and pull requests

- Use GitHub issues to report bugs or request features.
- Describe the problem clearly and include reproduction steps.
- Pull requests should reference relevant issues when possible.

## Notes

- This project is tested on Windows and uses `pyttsx3` with SAPI5.
- The YOLO model file `yolov8n.pt` is required for phone detection and is already included in the repository.
