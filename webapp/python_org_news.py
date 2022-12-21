from datetime import datetime
from dateutil.parser import parse
import requests
from bs4 import BeautifulSoup
from webapp.model import db, News


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (ValueError, requests.RequestException):
        return False


def get_python_news():
    html = get_html("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(
            html, "html.parser"
        )  # получаем дерево, с которым будем работать
        # получаем текст списка с нужным названием и разбиваем его на составляющие
        all_news = soup.find("ul", class_="list-recent-posts").findAll("li")
        for news in all_news:
            title = news.find("a").text
            url = news.find("a")["href"]

            published = news.find("time").text
            
            try: 
                published = parse(published).date()
            except ValueError:
                published = datetime.now()

            save_news(title= title, url= url, published= published)
    else:
        return False

def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:

        new_news = News(title = title, url = url, published = published)
        db.session.add(new_news)
        db.session.commit()
