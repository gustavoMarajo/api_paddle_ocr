FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Evita prompts na instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza pacotes e instala dependências
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        libgl1 \
        libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Cria diretório da aplicação
WORKDIR /app

# Copia os arquivos
COPY . .

# Instala dependências Python
RUN pip install paddlex
RUN pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
RUN pip install -U "paddleocr[doc-parser]"
RUN pip install python-multipart
RUN pip install uvicorn
RUN pip install fastapi
RUN pip install python-dotenv

# Gera as ENVs da API
RUN echo "API_TOKEN=token_aquir" > .env && \
    echo "PUBLIC_ROUTES=/" >> .env && \
    echo "APP_NAME=PaddleOCR API" >> .env 

ARG BUILD_COUNTER_FILE=.build_counter
RUN if [ -f "$BUILD_COUNTER_FILE" ]; then \
        build_number=$(cat $BUILD_COUNTER_FILE); \
        build_number=$((build_number + 1)); \
    else \
        build_number=1; \
    fi && \
    echo $build_number > $BUILD_COUNTER_FILE && \
    build_version="$(date +'%Y.%m.%d').${build_number}" && \
    echo "Gerando APP_VERSION=${build_version}" && \
    (grep -q '^APP_VERSION=' .env 2>/dev/null && sed -i "s/^APP_VERSION=.*/APP_VERSION=${build_version}/" .env || echo "APP_VERSION=${build_version}" >> .env)

# Expõe a porta da API
EXPOSE 8000

# Comando para iniciar o servidor FastAPI com Uvicorn
CMD ["python3", "-m", "uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]