# INICIALIZAÇÃO
Instale as dependências respeitando a ordem para evitar problemas de build:
```python 
pip install paddlex
pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
pip -U "paddleocr[doc-parser]"
pip install python-multipart
pip install uvicorn
pip install fastapi
```

Para levantar a API, use:
```prompt
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1  
```

A Api esta executando um processamento rápido, mas não ao mesmo tempo. Para ter mum processamento em larga escala, configure mais "workers":
```prompt
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 5  
```
Mas se lembre que quanto mais workers, mais recurso será consumido.
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

A Api esta executando um processamento rápido, mas não ao mesmo tempo. Para ter um processamento em larga escala, configure mais "workers" no Dockerfile:
```dockerfile
CMD ["python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "(5)"]
```
Mas se lembre que quanto mais workers, mais recurso será consumido.
#
## Outros containers
Para referencia em execução sobre OS e pacotes para compilar o serviço, olhar o arquivo "Dockerfile" da aplicação.
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