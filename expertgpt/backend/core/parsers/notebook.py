from langchain.document_loaders import NotebookLoader
from models.files import File

from .common import process_file


def process_ipnyb(file: File, enable_summarization, brain_id):
    return process_file(
        file=file,
        loader_class=NotebookLoader,
        enable_summarization=enable_summarization,
        brain_id=brain_id
    )
