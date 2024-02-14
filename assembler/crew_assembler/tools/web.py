from bs4 import BeautifulSoup as Soup
from langchain.tools import tool
from langchain_community.document_loaders import DocusaurusLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from unstructured.partition.html import partition_html


class WebTools:
    @tool("Get a URL's content as text")
    def get_html(url: str) -> str:
        """
        Given a URL, return the HTML content of the page it points to as text.

        Parameters:
            - url: The URL to fetch.

        Returns:
            - str: The HTML content of the page as text.
        """
        try:
            return partition_html(url=url)
        except Exception as e:
            return f"Oh no! We hit an error: '{str(e)}'"

    @tool("Fetch a website URL recursively")
    def fetch_recursive(url: str) -> list:
        """
        Given a URL, return the HTML content of the page and all of its linked pages.

        Parameters:
            - url: The URL to fetch.

        Returns:
            - str: A list of the HTML content of the page and all of its linked pages.

        """
        loader = RecursiveUrlLoader(
            url=url, max_depth=3, extractor=lambda x: Soup(x, "html.parser").text
        )

        return str(loader.load())

    @tool("Fetch a Docusaurus documentation website")
    def get_docusaurus_docs(base_url: str) -> str:
        """
        Given a URL, return the HTML content of the page and all of its linked pages.

        Parameters:
            - base_url: The Docusaurus-powered URL to fetch.

        Returns:
            - str: A list of the HTML content of the page and all of its linked pages.

        """
        loader = DocusaurusLoader(base_url)

        return str(loader.load())


#! for use with duckduckgo search
def make_scoped_query(query, sites):
    site_query = " OR ".join(f"site:{site}" for site in sites)
    return f"{query} {site_query}"


if __name__ == "__main__":
    # print(WebTools.get_html("https://www.google.com"))
    print(WebTools.fetch_recursive("https://flet.dev/docs/")[0])
