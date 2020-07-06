from bs4 import BeautifulSoup as soup
import re

from src.util import async_get

#Hardly ever worn URLs to scrape - empty pages return back empty
HEWI_URLS=[
    "https://www.hardlyeverwornit.com/search_results.php?items=newin&orderby=2&order=0&p=" + str(x) for x in list(range(1,26))
]

def hewi_fetch(limit):
    if not(limit is None):
        urls = HEWI_URLS[:limit]
    else:
        urls = HEWI_URLS
    response_content_list = async_get(urls)
    all_res = [
        hewi_parse_item(item) for resp_content in response_content_list \
        for item in hewi_parse_page(resp_content)
    ]

    return all_res

#Item scraper for Hardly Ever Worn It website
def hewi_parse_page(resp_content):
    sp = soup(resp_content,'lxml')
    
    return sp.findAll('div',{'class':'item_wrap 1'})

#Item scraper for Hardly Ever Worn It website
def hewi_parse_item(item):
    links=item.findAll('a')
    brand=links[2]['title']
    img_src=links[0].img['src']
    title=links[0].img['alt']
    url=links[0]['href']
    err=''
    if re.search('Yikes! Sold',str(item)) is not None:
        err='Sold;'
        curr=''
        cost='0'
    else:
        curr=item.find('span',{'class':'cost'}).findAll('span')[0].text
        cost=item.find('span',{'class':'cost'}).findAll('span')[1].text

    price=curr+cost
    orig_price=item.find('div',{'class':'new-shared-original-price'}).text
    if orig_price=='\xa0':
        err=err+'Original Price;'
        orig_price=0
    return {
        'brand':brand,'img_src':img_src,'url':url,'title':title,'curr':curr,
        'cost':cost,'price':price,'orig_price':orig_price,'err':err
    }