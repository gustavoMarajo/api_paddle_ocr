import os
import io
import sys
import tempfile
import logging
import warnings
import asyncio
from contextlib import redirect_stdout, redirect_stderr
from fastapi import FastAPI, UploadFile, File
from ocr_service import PaddleOCR

# ---------------------------------------------------------------------
# SUPRESSÃO DE LOGS E WARNINGS
# ---------------------------------------------------------------------
# os.environ["FLAGS_minloglevel"] = "3"
# os.environ["GLOG_minloglevel"] = "3"
# warnings.filterwarnings("ignore", category=UserWarning, module="paddle")

# logging.getLogger("paddleocr").setLevel(logging.ERROR)
# logging.getLogger("paddle").setLevel(logging.ERROR)
# logging.getLogger("numba").setLevel(logging.ERROR)
# logging.getLogger("urllib3").setLevel(logging.ERROR)

# ---------------------------------------------------------------------
# INICIALIZA O MODELO APENAS UMA VEZ
# ---------------------------------------------------------------------
print(" Inicializando modelo PaddleOCR (isso pode levar alguns segundos)...")
ocr = PaddleOCR(
    lang="pt",                    # Idioma português
    use_textline_orientation=False,          # Desativa rotação automática
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
)
print(" Modelo carregado com sucesso!")

# ---------------------------------------------------------------------
# CONFIGURAÇÃO DO SERVIÇO FASTAPI
# ---------------------------------------------------------------------
app = FastAPI(
    title="PaddleOCR API",
    version="1.1",
    description="API de OCR usando PaddleOCR com controle de concorrência seguro."
)

# Lock global para impedir acesso simultâneo ao modelo (thread-safe)
ocr_lock = asyncio.Lock()

# ---------------------------------------------------------------------
# FUNÇÃO OCR PRINCIPAL
# ---------------------------------------------------------------------
def run_ocr(image_bytes: bytes) -> str:
    """Executa OCR de forma silenciosa e segura."""
    # Cria arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    # Redireciona saídas para buffer (evita logs de baixo nível)
    buf = io.StringIO()
    try:
        with redirect_stdout(buf), redirect_stderr(buf):
            result = ocr.predict(tmp_path)

        # Extrai somente os textos reconhecidos
        all_texts = []
        for res in result:
            data = res.get("res", res)
            texts = data.get("rec_texts", [])
            all_texts.extend(texts)

        return "\n".join(all_texts).strip()
    except Exception as e:
        return f"[ERRO OCR] {e}"
    finally:
        # Remove arquivo temporário
        try:
            os.remove(tmp_path)
        except Exception:
            pass

# ---------------------------------------------------------------------
# ENDPOINT /ocr
# ---------------------------------------------------------------------
@app.post("/ocr")
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

# ---------------------------------------------------------------------
# SAÚDE DO SERVIÇO
# ---------------------------------------------------------------------
@app.get("/")
def health_check():
    return {"status": "ok", "message": "PaddleOCR API funcionando corretamente."}

# ---------------------------------------------------------------------
# MAIN LOCAL (para debug)
# ---------------------------------------------------------------------
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False, workers=1)
