"""
Парсинг данных статей habr в формате .text
вид данных: название статьи и ссылка;
настраиваемое кол-во страниц в 15 строке.
"""

import requests
from bs4 import BeautifulSoup as BS

page = 1
url_articles = requests.get("https://habr.com/ru/articles/")

try:
    if url_articles.status_code == 200:
        while page < 49:
            url = requests.get("https://habr.com/ru/articles/page" + str(page))
            response = BS(url.content, "html.parser")

            a_tags = response.find_all("a", {"class": "tm-title__link"})
            title = response.find_all("h2", {"class": "tm-title tm-title_h2"})

            for a_tag in a_tags:
                a_title = a_tag.find("span").text
                link = "https://habr.com" + a_tag["href"]
                print(a_title, link, end="\n")
                with open("habr.text", encoding="utf-8", mode="a") as file:
                    file.write(a_title + " " + link + "\n")
            page += 1

except requests.ConnectionError as error_connect:
    print("Ошибка подключения:", error_connect)
except requests.Timeout as error_timeout:
    print("Ошибка тайм-аута:", error_timeout)
except requests.RequestException as error_request:
    print("Ошибка запроса:", error_request)
