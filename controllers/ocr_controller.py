import asyncio
from fastapi import UploadFile, APIRouter
from fastapi.params import File
from services.ocr_service import run_ocr
from utils.controllers.routes import ROUTE_OCR



router = APIRouter()

# Lock global para impedir acesso simultâneo ao modelo (thread-safe) 
# Evita multiplos acessos aos arquivos escritos pelo modelo
ocr_lock = asyncio.Lock()



@router.post(ROUTE_OCR)
async def ocr_endpoint(file: UploadFile = File(...)):
    """
    Recebe uma imagem e devolve o texto OCR extraído.
    Aceita múltiplas requisições simultâneas, mas processa o modelo uma por vez.
    """
    try:
        image_bytes = await file.read()

        # Garante exclusividade do modelo PaddleOCR
        async with ocr_lock:
            text = await asyncio.to_thread(run_ocr, image_bytes)

        if not text or text.startswith("[ERRO"):
            return {
                "success": False,
                "filename": file.filename,
                "message": text if text.startswith("[ERRO") else "Nenhum texto detectado."
            }

        return {
            "success": True,
            "filename": file.filename,
            "text": text
        }

    except Exception as e:
        return {"success": False, "error": str(e)}