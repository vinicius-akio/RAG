from typing import List
from langchain_core.documents import Document


def processar_documento_docling(file_path: str, filename: str) -> List[Document]:
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.chunking import HybridChunker

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True

    converter = DocumentConverter(
        format_options={"pdf": PdfFormatOption(pipeline_options=pipeline_options)}
    )

    conversion_result = converter.convert(file_path)
    dl_doc = conversion_result.document

    chunker = HybridChunker(repeat_table_header=True, merge_peers=True)
    langchain_docs: List[Document] = []

    for chunk in chunker.chunk(dl_doc):
        contextualized_text = chunker.contextualize(chunk)
        headings = getattr(chunk.meta, "headings", [])
        doc_items = getattr(chunk.meta, "doc_items", [])

        element_type = "paragraph"
        if doc_items and hasattr(doc_items, "label"):
            element_type = str(doc_items.label)

        metadata = {
            "source": filename,
            "element_type": element_type,
            "heading_path": " > ".join(headings) if headings else "Geral",
            "page_numbers": [prov.page_no for item in doc_items for prov in getattr(item, "prov", []) if hasattr(prov, "page_no")]
        }

        langchain_docs.append(Document(page_content=contextualized_text, metadata=metadata))
    
    return langchain_docs