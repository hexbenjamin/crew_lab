def make_scoped_query(query, sites):
    site_query = " OR ".join(f"site:{site}" for site in sites)
    return f"{query} {site_query}"
