# Image Enhancement App

A small FastAPI + React app for enhancing images with Pillow. The backend accepts an image upload, applies contrast, brightness, or sharpness enhancement, and returns the processed image to the React frontend.

## Project Structure

```text
.
├── image_enhancement.py      # Pillow image helpers
├── main.py                   # FastAPI backend
├── images/                   # Local images and generated outputs
└── frontend/                 # React/Vite frontend
```

## Backend Setup

Create and activate a virtual environment if you have not already:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install backend dependencies:

```powershell
pip install fastapi uvicorn pillow python-multipart
```

Run the backend:

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Install frontend dependencies:

```powershell
cd frontend
npm install
```

Run the React app:

```powershell
npm run dev -- --port 5173
```

Frontend URL:

```text
http://127.0.0.1:5173
```

## Usage

1. Start the backend on port `8000`.
2. Start the frontend on port `5173`.
3. Open `http://127.0.0.1:5173`.
4. Choose an image.
5. Select an enhancement method.
6. Adjust the factor slider.
7. Click `Enhance`.

The enhanced image is returned by the backend and shown in the browser with a download link.

## API Endpoints

`GET /`

Health check for the backend.

`POST /enhance/upload`

Enhances an uploaded image. Form fields:

- `file`: image file
- `factor`: enhancement strength, for example `1.5`
- `method`: one of `sharpness`, `contrast`, or `brightness`

`POST /enhance/path`

Enhances an image that already exists on disk. JSON body example:

```json
{
  "image_path": "images/Interstellar wallpaper 4k.jpg",
  "factor": 1.5,
  "method": "sharpness"
}
```

Generated path-based outputs are saved under:

```text
images/enhanced/
```

## Build Frontend

```powershell
cd frontend
npm run build
```
