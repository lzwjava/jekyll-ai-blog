import requests
from bs4 import BeautifulSoup

proxy = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


def search_bing(query):
    url = f"https://www.bing.com/search?q={query}"

    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, proxies=proxy)

    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    for item in soup.select("li.b_algo h2 a"):
        results.append({"title": item.text, "url": item["href"]})

    return results[:5]


print(search_bing("US inflation rate 2026"))
