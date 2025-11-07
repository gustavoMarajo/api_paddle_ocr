from utils.configurations.config import APP_NAME, APP_VERSION
from utils.controllers.routes import ROUTE_APP_STATUS
from fastapi import APIRouter



router = APIRouter()



@router.get(ROUTE_APP_STATUS)
def status_check():
    """"Verifica se a API está funcionando."""
    return {
        "status": "ok", 
        "message": APP_NAME + " funcionando corretamente.", 
        "version": APP_VERSION 
    }