from contextlib import redirect_stderr, redirect_stdout
import io, tempfile, os
from utils.dis.singles_instances import get_ia_model_instance




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
            result = get_ia_model_instance().predict(tmp_path)

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