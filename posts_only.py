import requests
from bs4 import BeautifulSoup
from toolz import thread_first, thread_last
from typing import List
import pandas as pd

#pip install lxml

STRING_FUNCS = ["capitalize", "join", "count", "isalnum", "isalpha", "isascii", "isdecimal", "isdigit", "isidentifier", "islower", "isnumeric", "isspace", "istitle", "isupper", "lower", "lstrip", "replace", "rstrip", "split", "strip", "upper"]

for s_func in STRING_FUNCS: #PYTHON MAGIC
    exec("%s=getattr(str, s_func)" %s_func)
    
def pipe(*funcs:List[callable], thread="first"):
  thread = thread_first if thread == "first" else thread_last
  return lambda data: thread(data, *funcs)

clean_sentence = pipe(strip,
                     (replace, "\n", " ")
                     )

def bs_to_paragraphs(soup, tag, tag_filter, strip=True):
  """ Extracts all the text from the given tags and returns them as a list. """
  return [paragraph.get_text(strip=strip) for paragraph in soup.findAll(tag, tag_filter)]

def url_to_html(url: str):
  """ Takes a url and returns a request.Response object """
  return requests.get(url, headers = {'User-Agent': 'test'})


def url_to_base_url(url):
  """ Gets the base url from url (useful for pagination). """
  return "/".join(url.split("/")[:3])

def html_to_bs(html, parser="lxml"):
  """ Takes a request.Response object and returns a Beautiful Soup object"""
  return BeautifulSoup(html.content, parser)

def bs_replace(soup, source, target):
  """ Replaces source tag with target tag in Beautiful Soup object """
  for tag in soup.findAll(source):
    tag.replace_with(target)
  return soup

def bs_to_text(soup, strip=True):
  """ Extracts all the text from a Beautiful soup object. """
  return soup.get_text(strip=strip)


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TypeError:
            print(f"{func.__name__} only takes numbers as the argument")
    return inner_function    


url_to_text = pipe(url_to_html,
                      html_to_bs,
                      (bs_replace, "br", "\n"),
                      bs_to_text
                     )

url_to_bs = pipe(url_to_html, 
                 html_to_bs)

def get_post_text(url):
    return " ".join(bs_to_paragraphs(url_to_bs(url), "p", {}))


def get_p_text_safe(url):
    try:
        text = get_post_text(url)
        if is_post(text):
            print("probably article: ", url)
        return text
    except:
        return ""
    return ""


#TODO make this an argument
def is_post(text):
    """an incredibly complex classifier. State of the Art"""
    return len(text.split(" ")) > 300


cleaned = pd.read_csv("out/cleaned.csv")

cleaned = cleaned[:100]
# print(is_post("https://dacapo.io/questions"), "is post?")


cleaned["text"] = cleaned["url"].map(get_p_text_safe)
is_post_mask = [is_post(text) for text in cleaned.text]
post_df = cleaned[is_post_mask]

print(len(post_df), " entries considered articles")
post_df.to_csv("out/posts.csv", index = False, header=True)