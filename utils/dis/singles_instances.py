from fastapi import FastAPI
from ocr_service._pipelines.ocr import PaddleOCR
from utils.configurations.config import APP_NAME, APP_VERSION




# ---------------------------------------------------------------------
# CONFIGURAÇÃO DO SERVIÇO FASTAPI
# ---------------------------------------------------------------------
api: FastAPI = None
def get_api_instance() -> FastAPI:

    global api
    if api is None:
        api = FastAPI(
            title=APP_NAME,
            version=APP_VERSION,
        )
        
    return api



# ---------------------------------------------------------------------
# INICIALIZA O MODELO APENAS UMA VEZ
# ---------------------------------------------------------------------

model: PaddleOCR = None
def get_ia_model_instance() -> PaddleOCR:

    global model
    if model is None:
        print("=> Inicializando modelo PaddleOCR (pode levar alguns segundos)...")
        model = PaddleOCR(
            lang="pt",
            use_textline_orientation=False,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
        )
        print("=> Modelo carregado com sucesso!")
    
    return model



