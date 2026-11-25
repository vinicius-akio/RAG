from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, HTTPException, UploadFile, File

from app.models.schemas import UploadResponse
from app.services.docling_services import processar_documento_docling
from app.services.qdrant_services import salvar_no_qdrant

router = APIRouter(prefix="/upload", tags=["Upload RAG"])

SUPPORTED_EXTENSIONS = {"pdf", "docx", "xlsx", "pptx", "html", "htm"}


@router.post("", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nenhum arquivo foi enviado.")

    extension = Path(file.filename).suffix.lower().lstrip(".")
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Extensão '.{extension}' não suportada.")

    temp_path = None
    try:
        with NamedTemporaryFile(delete=False, suffix=f".{extension}") as temp_file:
            temp_path = temp_file.name
            temp_file.write(await file.read())

        documents = processar_documento_docling(temp_path, file.filename)

        salvar_no_qdrant(documents)
        return UploadResponse(
            status="sucesso",
            mensagem=f"Documento '{file.filename}' processado com sucesso.",
            total_chunks=len(documents),
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Falha ao processar documento: {exc}")
    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)