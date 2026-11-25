from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    filter_element_type: Optional[str] = None

class SourceItem(BaseModel):
    arquivo: str
    tipo_elemento: str
    caminho_hierarquico: str
    paginas: List[int]
    conteudo: str

class QueryResponse(BaseModel):
    agente_ia: str
    pergunta: str
    resposta: str
    fontes_consultadas: List[SourceItem]

class UploadResponse(BaseModel):
    status: str
    mensagem: str
    total_chunks: int