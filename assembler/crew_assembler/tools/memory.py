# import os
from textwrap import dedent

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from crew_assembler.utils import make_subdir

EMBEDDINGS: SentenceTransformerEmbeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


def create_chroma_instance(collection_name: str = None):
    return Chroma(
        collection_name=collection_name or "crew_memory",
        embedding_function=EMBEDDINGS,
        persist_directory=str(make_subdir("chroma")),
    )


class MemoryTools:
    @tool("Store a text file into memory")
    def embed_text(text_path: str) -> bool:
        """
        Store a text file into memory.

        Args:
            text_path (str): The path to the text file.
            collection_name (str, optional): The name of the collection. Defaults to None.

        Returns:
            str: True if the text file is successfully stored in memory, False otherwise.
        """

        # collection_name = os.path.basename(text_path).split(".")[0]
        vec_db = create_chroma_instance()

        try:
            docs = TextLoader(file_path=text_path, encoding="utf-8").load()
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=100, chunk_overlap=0.15
            )
            docs = splitter.split_documents(docs)
            vec_db.add_documents(docs)
            return str(True)
        except Exception as e:
            print(f"We hit an error while using the tool: {e}.")
            return str(False)

    @tool("Query the permanent memory for a text string")
    def similarity_search(query: str) -> list:
        """
        Query the permanent memory for a text string.

        Args:
            query (str): The text string to search for.
            collection_name (str, optional): The name of the collection. Defaults to None.

        Returns:
            list: A list of documents matching the query, along with their source and content.
        """

        vec_db = create_chroma_instance()

        docs = vec_db.similarity_search(query, k=2)

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
            
            {results}"""
        )


# if __name__ == "__main__":
# embed_text("/home/hex/python/crew_lab/assembler/testdocs/test-gain.txt")
# print(similarity_search("Who is the person speaking?"))
