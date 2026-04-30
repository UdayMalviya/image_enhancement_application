from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from image_enhancement import enhance_image, read_image, save_image


app = FastAPI(title="Image Enhancement")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "images" / "enhanced"
ALLOWED_METHODS = {"contrast", "brightness", "sharpness"}


class EnhancePathRequest(BaseModel):
    image_path: str = Field(..., examples=["images/input.jpg"])
    factor: float = Field(1.5, gt=0)
    method: str = Field("sharpness", examples=["contrast", "brightness", "sharpness"])
    output_name: str | None = Field(None, examples=["enhanced.png"])


def validate_method(method: str) -> str:
    normalized_method = method.lower()
    if normalized_method not in ALLOWED_METHODS:
        raise HTTPException(
            status_code=400,
            detail=f"method must be one of: {', '.join(sorted(ALLOWED_METHODS))}",
        )
    return normalized_method


def resolve_image_path(image_path: str) -> Path:
    path = Path(image_path)
    if not path.is_absolute():
        path = BASE_DIR / path

    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail=f"Image not found: {image_path}")

    return path


def build_output_path(output_name: str | None, source_name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if output_name:
        output_path = OUTPUT_DIR / Path(output_name).name
    else:
        source_suffix = Path(source_name).suffix or ".png"
        output_path = OUTPUT_DIR / f"{Path(source_name).stem}-{uuid4().hex}{source_suffix}"

    return output_path


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Image Enhancement API is running"}


@app.post("/enhance/path")
def enhance_from_path(request: EnhancePathRequest):
    method = validate_method(request.method)
    image_path = resolve_image_path(request.image_path)
    output_path = build_output_path(request.output_name, image_path.name)

    try:
        image = read_image(image_path)
        enhanced_image = enhance_image(image, request.factor, method)
        save_image(enhanced_image, output_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "message": "Image enhanced successfully",
        "output_path": str(output_path.relative_to(BASE_DIR)),
    }


@app.post("/enhance/upload")
async def enhance_from_upload(
    file: UploadFile = File(...),
    factor: float = Form(1.5, gt=0),
    method: str = Form("sharpness"),
):
    method = validate_method(method)
    output_path = build_output_path(None, file.filename or "uploaded.png")
    temp_path = OUTPUT_DIR / f"upload-{uuid4().hex}-{Path(file.filename or 'image').name}"

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        temp_path.write_bytes(await file.read())

        image = read_image(temp_path)
        enhanced_image = enhance_image(image, factor, method)
        save_image(enhanced_image, output_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        if temp_path.exists():
            temp_path.unlink()

    return FileResponse(
        output_path,
        media_type=file.content_type or "application/octet-stream",
        filename=output_path.name,
    )
