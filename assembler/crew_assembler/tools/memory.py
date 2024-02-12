import os
from textwrap import dedent

from langchain.text_splitter import CharacterTextSplitter
from langchain.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from rich.pretty import pprint

from crew_assembler.utils import make_subdir

TEXT_SPLITTER = CharacterTextSplitter(chunk_size=200, chunk_overlap=0.2)
EMBEDDINGS = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


@tool("Store a text file into memory")
def embed_text(text_path: str, collection_name: str = None) -> bool:
    """
    This tool allows you to store the contents of a text file into your permanent memory.

    Parameters:
    - text_path: The path to the text file you want to store.

    Returns:
    - bool: True if the operation was successful, False otherwise.
    """

    vec_db = Chroma(
        collection_name=collection_name or "langchain",
        embedding_function=EMBEDDINGS,
        persist_directory=str(make_subdir("chroma")),
    )

    try:
        docs = TextLoader(text_path).load()
        docs = TEXT_SPLITTER.split_documents(docs)

        vec_db.add_documents(docs)

        return True
    except Exception as e:
        print(f"We hit an error while using the tool: {e}.")
        return False


@tool("Query the permanent memory for a text string")
def similarity_search(query: str, collection_name: str = None) -> list:
    """
    This tool allows you to query the permanent memory for a text string.

    Parameters:
    - text: The text string you want to query for.

    Returns:
    - str: The results of the query.
    """

    vec_db = Chroma(
        collection_name=collection_name or "langchain",
        embedding_function=EMBEDDINGS,
        persist_directory=str(make_subdir("chroma")),
    )

    docs = vec_db.similarity_search(query, k=2)
    # return docs

    template = dedent(
        """
        DOCUMENT {i}: {txt}
         
        ---
        SOURCE: {src}
         
        -------"""
    )

    results = "\n".join(
        [
            template.format(i=i, txt=d.page_content, src=d.metadata["source"])
            for i, d in enumerate(docs)
        ]
    )

    return dedent(
        f"""Here are the results of the query:
        + + +
        
        {results}"""
    )


# if __name__ == "__main__":
# embed_text("/home/hex/python/crew_lab/assembler/testdocs/test-gain.txt")
# print(similarity_search("Who is the person speaking?"))
