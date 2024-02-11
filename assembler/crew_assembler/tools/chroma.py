from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from crew_assembler.file_ops import make_subdir


TEXT_SPLITTER = RecursiveCharacterTextSplitter()
EMBEDDINGS = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
VEC_DB = Chroma(
    embedding_function=EMBEDDINGS,
    persist_directory=make_subdir("chroma"),
)


@tool("Store a text file into memory")
def embed_text(text_path: str) -> bool:
    """
    This tool allows you to store the contents of a text file into your permanent memory.

    Parameters:
    - text_path: The path to the text file you want to store.

    Returns:
    - bool: True if the operation was successful, False otherwise.
    """
    try:
        docs = TextLoader(text_path).load()
        docs = TEXT_SPLITTER.split_documents(docs)

        VEC_DB.add_documents(docs)
        VEC_DB.persist()

        return True
    except Exception as e:
        print(f"We hit an error while using the tool: {e}.")
        return False


if __name__ == "__main__":
    embed_text("")
