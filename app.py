from middlewares.auth import tokenAuthMiddleware
from utils.dis.singles_instances import get_api_instance, get_ia_model_instance
from controllers.ocr_controller import router as ocr_router
from controllers.status_controller import router as status_router




# Inicializa a aplicação FastAPI
api = get_api_instance()

# Registra os middlewares
api.middleware("http")(tokenAuthMiddleware)

# Registra os controladores (routers)
api.include_router(status_router)
api.include_router(ocr_router)

# Inicializa o modelo de IA
get_ia_model_instance()
