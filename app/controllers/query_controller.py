from fastapi import APIRouter, HTTPException

from app.models.schemas import QueryRequest, QueryResponse, SourceItem
from app.services.qdrant_services import get_vectorstore
from app.services.gemma_services import gerar_resposta_gemma

router = APIRouter(prefix="/query", tags=["Consulta RAG"])


@router.post("", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    vectorstore = get_vectorstore()
    if vectorstore is None:
        raise HTTPException(status_code=400, detail="Banco de dados vetorial vazio.")

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(request.question)
    resposta_texto = gerar_resposta_gemma(request.question, docs)

    fontes = [
        SourceItem(
            arquivo=doc.metadata.get("source", "Desconhecido"),
            tipo_elemento=doc.metadata.get("element_type", "paragraph"),
            caminho_hierarquico=doc.metadata.get("heading_path", "Geral"),
            paginas=doc.metadata.get("page_numbers", []),
            conteudo=doc.page_content,
        )
        for doc in docs
    ]

    return QueryResponse(
        agente_ia="Google Gemma 2 (via Ollama API)",
        pergunta=request.question,
        resposta=resposta_texto,
        fontes_consultadas=fontes,
    )