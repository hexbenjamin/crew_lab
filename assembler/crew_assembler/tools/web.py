from langchain.tools import tool
from unstructured.partition.html import partition_html


@tool("Get a URL's content as text")
def unstructured_html(url: str) -> str:
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


#! for use with duckduckgo search
def make_scoped_query(query, sites):
    site_query = " OR ".join(f"site:{site}" for site in sites)
    return f"{query} {site_query}"
