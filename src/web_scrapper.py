#from search_engine_parser import GoogleSearch
from search_engine_parser.core.engines.bing import Search as BingSearch
from search_engine_parser.core.engines.yahoo import Search as YahooSearch
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

import urllib



def search_web_for_links(query):
    """
        Here yahoo search engine is used, support for other bing and google is also added.
        Bing and google are ignored for now , becaues no rendering frameworks like selenium or
        headless selenium is used. So the IP may get block after few searches
    """
    links = scrap_links_from_yahoo(query)
    #links += scrap_links_from_bing(query)
    #links = ['https://support.google.com/webmasters/answer/7451184', 'https://thebloggingguides.com/what-is-search-engine-optimization/', 'https://developers.google.com/search/docs/beginner/do-i-need-seo', 'https://www.coursera.org/specializations/seo', 'https://www.amazon.com/Best-Sellers-Books-Search-Engine-Optimization/zgbs/books/6133991011', 'https://www.seo.com/', 'https://www.coursehero.com/file/78412885/51-Search-Engine-Optimization-Services-Guidedocx/', 'https://moz.com/learn/seo/what-is-seo', 'https://en.wikipedia.org/wiki/Optimized_Searching', 'https://www.lyfemarketing.com/blog/what-is-seo-and-how-it-works/', 'https://contactscraper.com/new/2021/01/24/search-engine-optimization-an-introduction-2/', 'https://www.udemy.com/course/search-engine-optimization-complete-specialization-course/', 'https://www.freshercooker.com/courses/search-engine-optimization-complete-specialization-course-100-off-2/', 'https://thebloggingguides.com/what-is-search-engine-optimization/', 'https://support.google.com/webmasters/answer/7451184', 'https://moz.com/beginners-guide-to-seo', 'https://www.coursera.org/specializations/seo', 'https://developers.google.com/search/docs/beginner/do-i-need-seo', 'https://www.udemy.com/course/search-engine-optimization-complete-specialization-course/']
    return links

def scrap_web_page(url):
    """
        Each URL is scrapped and for simplicity of the code only paragraph-tag (p) is being extracted
    """
    print(url)
    try:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser') 
            p_tags = soup.findAll('p')
            texts = [ x.text for x in p_tags]
            text = clean_text_from_web_page(texts)
            return text
        else :
            return None
    except:
        return None
        # add error log here 


def clean_text_from_web_page(data):
    """
        some basic cleaning we can also use re lib, but her built in string operations do just fine
        html tag line is removed because its a word in the vocab and make unwanted learing
    """
    cleaned_data = []

    for sentence in data:
        if 'https://' not in sentence:
            sentence = sentence.replace('\n',' ')
            sentence = sentence.replace("\\","").replace('"', '')
            cleaned_data.append(sentence)
    return " ".join(cleaned_data)



def scrap_links_from_bing(query):
    """
    Used to scrap the seed links for a given query from bing
    """
    NUMBER_OF_PAGES_TO_COVER = 1

    available_links = []

    for i in range(1,NUMBER_OF_PAGES_TO_COVER+1):
        search_args = (query, i)
        results = BingSearch().search(search_args)
        [ available_links.append(link) for link in results['link'] if link not in available_links]

    return available_links
def scrap_links_from_yahoo(query):
    """
        Used to scrap the seed links for a given query from yahoo
    """
    NUMBER_OF_PAGES_TO_COVER = 3

    available_links = []

    for i in range(1,NUMBER_OF_PAGES_TO_COVER+1):
        try:
            search_args = (query, i)
            results = YahooSearch().search(search_args)
            [ available_links.append(link) for link in results['link'] if link not in available_links]
        except:
            pass

    return available_links

