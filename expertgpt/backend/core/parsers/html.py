from langchain.document_loaders import UnstructuredHTMLLoader
from models.files import File

from .common import process_file


def process_html(file: File, enable_summarization, brain_id):
    return process_file(
        file=file,
        loader_class=UnstructuredHTMLLoader,
        enable_summarization=enable_summarization,
        brain_id=brain_id,
    )
