#Number of connections to set up when scraping asynchronously
ASYNC_CONN_NUM = 10

#Hardly ever worn URLs to scrape - empty pages return back empty
HEWI_URLS=[
    "https://www.hardlyeverwornit.com/search_results.php?items=newin&orderby=2&order=0&p=" + str(x) for x in list(range(1,26))
]