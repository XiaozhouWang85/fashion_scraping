from bs4 import BeautifulSoup as soup
import json
import re
import requests

from src.util import async_get
from src.bigquery import log_to_bigquery

#Hardly ever worn URLs to scrape - empty pages return back empty
FP_HOME = 'https://www.fashionphile.com/shop/new-arrivals?sort=date-desc&pageSize=180'
FP_PAGE = "https://www.fashionphile.com/shop/new-arrivals?pageSize=180&sort=date-desc&page="

def fp_fetch(limit):
    pages=fp_get_number_of_pages()
    
    urls=[FP_PAGE + str(x) for x in list(range(1,pages+1))]

    if not(limit is None):
        urls = urls[:limit]
    else:
        pass
    response_content_list = async_get(urls)
    all_res = [
        fp_parse_item(item) for resp_content in response_content_list \
        for item in fp_parse_page(resp_content)
    ]

    return all_res

def fp_parse_page(resp_content):
    sp = soup(resp_content,'lxml')
    boxes=sp.findAll('script')
    for box in boxes:
        if re.search('bootstrappedShopResults',str(box)) is not None:
            script=box
    script_json=json.loads(re.sub("^\n    var bootstrappedShopResults = |;\n$",'',script.text))
    page_sp = soup(script_json['products'],'lxml')
    items=page_sp.findAll('div',{'class':'product_container'})
    
    log_to_bigquery(items)
    return items

def fp_get_number_of_pages():
    resp=requests.get(FP_HOME)
    sp = soup(resp.content,'lxml')
    nav=sp.find('div',{'data-container':'pagination'})
    pages=0
    for link in nav.findAll('a'):
        try:
            pages=max(pages,int(link.text))
        except:
            pass
    return pages
    
#Item scraper for Fashionphile website
def fp_parse_item(item):
    links=item.findAll('a')
    brand=item.find('meta',itemprop='brand').get('content')
    img_src=links[0].img['data-src']
    title=links[1].text
    url=links[1]['href']
    err=''
    curr=''
    cost=item.find('div',{'class':'price'}).span.text

    price=curr+cost
    orig_price=''
    return {
        'site':'fashionphile',
        'brand':brand,'img_src':img_src,'url':url,'title':title,'curr':curr,
        'cost':cost,'price':price,'orig_price':orig_price,'err':err
    }