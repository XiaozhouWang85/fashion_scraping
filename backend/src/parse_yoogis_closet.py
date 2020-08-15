from bs4 import BeautifulSoup as soup
import json
import re
import requests

from src.util import async_get, get_gcp_logger

#Hardly ever worn URLs to scrape - empty pages return back empty
YC_HOME = 'https://www.yoogiscloset.com/latest-arrivals'
YC_PAGE = "https://www.yoogiscloset.com/latest-arrivals?ajax=1&dir=desc&gan_data=true&order=received&p="

def yc_fetch(limit):

    logger = get_gcp_logger()

    log_message = {}
    log_message.update({
        "Website":"Yoogi's closet",
        "Process Start":"Scraper process starting for ⚙️"
    })
    
    try:
        pages=yc_get_number_of_pages()
        
        urls=[YC_PAGE + str(x) for x in list(range(1,pages+1))]

        if not(limit is None):
            urls = urls[:limit]
        else:
            pass

        response_content_list = async_get(urls)

        all_res = [
            yc_parse_item(item) for resp_content in response_content_list \
            for item in yc_parse_page(resp_content)
        ]
        log_message.update({
            "Process End":"Successfully parsed results 📝"
        })

        logger.log_struct(log_message, 'INFO')
        return all_res
    
    except Exception as e:
        log_message.update({
            "Process End": str(e)
        })
        logger.log_struct(log_message, 'ERROR')

#Item scraper for Hardly Ever Worn It website
def yc_parse_page(resp_content):
    sp = soup(json.loads(resp_content)['product_list'],'lxml')
    #Extract each item container
    boxes=sp.findAll('div',{'class':'item'})
    #Remove empty boxes
    items=[]
    for box in boxes:
        if len(box)>0:
            items.append(box)
    
    return items

def yc_get_number_of_pages():
    resp=requests.get(YC_HOME)
    sp = soup(resp.content,'lxml')
    nav=sp.find('div',{'class':'amount'})
    item_count=re.findall('[0-9]+',nav.text)[2]
    pages=int(int(item_count)/64)
    return pages
    
def yc_parse_item(item):
    err=''
    brand=item.find('span',{'class':'designer-name'}).text
    img_src=item.find('img',{'class':'primary_image rollover'})['src']
    title=re.sub('\n|\t','',item.find('span',{'class':'product-name'}).text.strip())
    url=item.find('a',{'class':'product-image'})['href']
    curr=item.find('meta',{'itemprop':'priceCurrency'})['content']
    cost=''
    price_box=item.find('div',{'class':'price-box'})
    
    if item.find('link',{'href':"http://schema.org/SoldOut"}) is None:
        price=price_box.find('span',{'itemprop':'price'}).text
    else:
        err='Sold;'
        price=''
    old_box=price_box.find('li',{'class':'old-price'})
    if old_box is not None:
        orig_price=old_box.find('span',{'class':'price'}).text
    else:
        orig_price=''
    return {
        'site':'yoogiscloset',
        'brand':brand,'img_src':img_src,'url':url,'title':title,'curr':curr,
        'cost':cost,'price':price,'orig_price':orig_price,'err':err
    }