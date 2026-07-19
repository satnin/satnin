from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import json
import os
import shutil
import tempfile
import zipfile

from process import process_file

app = FastAPI()


@app.post("/process")
async def process(
    config: str = Form(...),
    file: UploadFile = File(...)
):
    data = json.loads(config)

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, file.filename)

        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_dir = process_file(input_path, data)

        zip_path = os.path.join(temp_dir, "result.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(output_dir):
                for name in files:
                    file_path = os.path.join(root, name)
                    zip_file.write(file_path, arcname=os.path.relpath(file_path, output_dir))

        # Attention : le fichier temporaire doit rester disponible
        # pendant l'envoi de la réponse.
        final_zip = "/tmp/result.zip"
        shutil.copy(zip_path, final_zip)

        return FileResponse(
            final_zip,
            media_type="application/zip",
            filename="result.zip"
        )