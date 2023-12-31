from langchain.document_loaders import Docx2txtLoader
from models.files import File

from .common import process_file


def process_docx(file: File, enable_summarization, brain_id):
    return process_file(
        file=file,
        loader_class=Docx2txtLoader,
        enable_summarization=enable_summarization,
        brain_id=brain_id,
    )
