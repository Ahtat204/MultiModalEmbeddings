import os
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

app = FastAPI()
UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed image content types
ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB Limit


@app.post("/image")
async def upload_image(file: UploadFile = File(...)):
    # 1. Validate File Type
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds the 5MB maximum limit."
        )
    file_path = UPLOAD_DIR / file.filename

    try:

        async with file.file as source_file:
            with open(file_path, "wb") as buffer:
                while content := await file.read(1024 * 1024):
                    buffer.write(content)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the file: {str(e)}"
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Image uploaded successfully",
            "filename": file.filename,
            "content_type": file.content_type,
            "saved_path": str(file_path)
        }
    )
