import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.documents import Document

client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL", "https://ollama.com/v1"),
    api_key=os.getenv("OLLAMA_API_KEY", "ollama_key_padrao"),
)

def gerar_resposta_gemma(query: str, context_docs: List[Document]) -> str:
    
    context_text = "\n\n".join([
        f"[Fonte: {doc.metadata.get('source')} | Tipo: {doc.metadata.get('element\_type')} | Caminho: {doc.metadata.get('heading\_path')}]\\n{doc.page_content}"
        for doc in context_docs
        ])
    
    system_prompt = (
        "Você é um Agente de IA especialista em análise de documentos internos.\\n"
        "Responda à pergunta do usuário utilizando estritamente os trechos de contexto fornecidos abaixo.\\n\\n"
        f"Contexto Extraído dos Documentos:\n{context_text}"
    )

    completion = client.chat.completions.create(
        model=os.getenv("OLLAMA_MODEL", "gemma2"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=0.2
    )
    return completion.choices.message.content