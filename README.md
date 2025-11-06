# INICIALIZAÇÃO
Instale as dependencias respeitando a ordem para evitar problemas de build:
```python 
pip install paddlex
pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
pip -U "paddleocr[doc-parser]"
pip install python-multipart
pip install uvicorn
pip install fastapi
```
#
## Usando o Docker com Container Linux-GPU
O Dockerfile já esta configurado para OS Linux compativel com GPU conforme pacotes instalados para o modelo da IA, a fim de uma melhor performance.
Para gerar a imagem, abra o Powershell excute no repositório e execute:
```powershell
docker build -t nome-da-sua-imagem .
```

Depois de gerado a imagem do container, execute:
```powershell
docker run -d -p 8000:8000 --gpus all --name nome-da-sua-imagem_dev nome-da-sua-imagem
```
#
## Endpoint-OCR
Use o Postman se for somente para um teste rápido conforme descrito abaixo:<br>
URL: http://10.0.2.63:8000/ocr<br>
METHOD: POST<br>
BODY: form<br>
KEY=> file | VALUE: (imagem qualquer para OCR)

```curl
--location 'http://10.0.2.63:8000/ocr' \
--form 'file=@"postman-cloud:///1f0b8ee7-b4df-4840-b4bf-85d61e6d4177"'
```
#
FIM