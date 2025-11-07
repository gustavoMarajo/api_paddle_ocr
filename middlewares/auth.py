from fastapi import Request
from fastapi.responses import JSONResponse
from utils.configurations.config import API_TOKEN, PUBLIC_ROUTES



# ============================================================
# CONSTANTES
# ============================================================
COSNT_KEY_AUTH_HEADER = "Authorization"
COSNT_KEY_AUTH_HEADER_COMPLEMENT = "Bearer "



# ============================================================
# MIDDLEWARES
# ============================================================
async def tokenAuthMiddleware(request: Request, call_next):
    """
    Middleware simples que valida o token de autenticação em todas as rotas,
    exceto nas rotas públicas.
    """

    if request.url.path not in PUBLIC_ROUTES:
        auth_header = request.headers.get(COSNT_KEY_AUTH_HEADER)

        if not auth_header or not auth_header.startswith(COSNT_KEY_AUTH_HEADER_COMPLEMENT):
            return JSONResponse(status_code=401, content={"message": "Não autorizado."})

        token = auth_header.split(COSNT_KEY_AUTH_HEADER_COMPLEMENT)[1]
        if token != API_TOKEN:
            return JSONResponse(status_code=403, content={"message": "Não autenticado."})

    response = await call_next(request)
    return response

