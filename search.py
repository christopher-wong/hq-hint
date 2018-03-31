import re
from html import unescape

from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tag.perceptron import PerceptronTagger
from nltk.tokenize import RegexpTokenizer
from unidecode import unidecode

import networking

STOP = set(stopwords.words("english")) - {"most", "least"}
tokenizer = RegexpTokenizer(r"\w+")
tagger = PerceptronTagger()
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
           "Accept": "*/*",
           "Accept-Language": "en-US,en;q=0.5",
           "Accept-Encoding": "gzip, deflate"}
GOOGLE_URL = "https://www.google.com/search?q={}&ie=utf-8&oe=utf-8&client=firefox-b-1-ab"


def find_keywords(words):
    """
    Returns the list of words given without stopwords.
    :param words: List of words
    :return: Words without stopwords
    """
    return [w for w in tokenizer.tokenize(words.lower()) if w not in STOP]


def get_google_links(page, num_results):
    soup = BeautifulSoup(page, "html.parser")
    results = soup.findAll("h3", {"class": "r"})

    links = []
    for r in results:
        url = r.find("a")
        if url is not None:
            links.append(url["href"])
    links = list(dict.fromkeys(links))  # Remove duplicates while preserving order

    return links[:num_results]


async def search_google(question, num_results):
    """
    Returns num_results urls from a google search of question.
    :param question: Question to search
    :param num_results: Number of results to return
    :return: List of length num_results of urls retrieved from the search
    """
    # Could use Google's Custom Search API here, limit of 100 queries per day
    # result = service.cse().list(q=question, cx=CSE_ID, num=num_results).execute()
    # return result["items"]
    page = await networking.get_response(GOOGLE_URL.format(question), timeout=5, headers=HEADERS)
    return get_google_links(page, num_results)


async def multiple_search(questions, num_results):
    queries = list(map(GOOGLE_URL.format, questions))
    pages = await networking.get_responses(queries, timeout=5, headers=HEADERS)
    link_list = [get_google_links(page, num_results) for page in pages]
    return link_list


def clean_html(html):
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"\n", " ", cleaned)
    cleaned = re.sub(r"\s\s+", " ", cleaned)

    return unidecode(unescape(cleaned.strip()))


async def get_clean_texts(urls, timeout=1.5, headers=HEADERS):
    responses = await networking.get_responses(urls, timeout, headers)

    return [clean_html(r).lower() for r in responses]
