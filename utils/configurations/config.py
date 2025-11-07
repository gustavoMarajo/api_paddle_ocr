import os
from dotenv import load_dotenv



# --------------------------------------------------------
# CONSTANTES
# --------------------------------------------------------
CONST_KEY_ENV_SEPARATOR = ","
CONST_KEY_ENV_API_TOKEN = "API_TOKEN"
CONST_KEY_ENV_PUBLIC_ROUTES = "PUBLIC_ROUTES"
CONST_KEY_ENV_APP_NAME = "APP_NAME"
CONST_KEY_ENV_APP_VERSION = "APP_VERSION"

# Carrega o arquivo .env na inicialização
load_dotenv()

# --------------------------------------------------------
# VARIÁVEIS DE AMBIENTE
# --------------------------------------------------------
API_TOKEN = os.getenv(CONST_KEY_ENV_API_TOKEN)

public_routes_env = os.getenv(CONST_KEY_ENV_PUBLIC_ROUTES)
PUBLIC_ROUTES = [r.strip() for r in public_routes_env.split(CONST_KEY_ENV_SEPARATOR) if r.strip()]

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")




# ---------------------------------------------------------------------
# SUPRESSÃO DE LOGS E WARNINGS
# Para bloquear todos os logs de baixo nível e warnings desnecessários, descomente as linhas abaixo.
# ---------------------------------------------------------------------
# os.environ["FLAGS_minloglevel"] = "3"
# os.environ["GLOG_minloglevel"] = "3"
# warnings.filterwarnings("ignore", category=UserWarning, module="paddle")

# logging.getLogger("paddleocr").setLevel(logging.ERROR)
# logging.getLogger("paddle").setLevel(logging.ERROR)
# logging.getLogger("numba").setLevel(logging.ERROR)
# logging.getLogger("urllib3").setLevel(logging.ERROR)