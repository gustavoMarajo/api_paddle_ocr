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
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -U "paddleocr[doc-parser]"

RUN pip install paddlex
RUN pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
RUN pip install -U "paddleocr[doc-parser]"
RUN pip install python-multipart
RUN pip install uvicorn
RUN pip install fastapi

# Expõe a porta da API
EXPOSE 8000

# Comando para iniciar o servidor FastAPI com Uvicorn
CMD ["python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]