import requests  # type: ignore[import-untyped]
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []

    articles = parser.find_all("article", class_="tm-articles-list__item")

    for article in articles:
        title_tag = article.find("a", class_="tm-title__link")
        title = title_tag.text.strip() if title_tag else ""

        author_tag = article.find("a", class_="tm-user-info__username")
        author = author_tag.text.strip() if author_tag else None

        url = "https://habr.com" + title_tag["href"] if title_tag else None
        habr_id = url.split("/")[-2] if url else None

        complexity_tag = article.find("span", class_="tm-article-complexity__label")
        complexity = complexity_tag.text.strip() if complexity_tag else "-"

        news_list.append({"title": title, "author": author, "url": url, "habr_id": habr_id, "complexity": complexity})

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    next_page = parser.find("a", class_="tm-pagination__navigation-link", rel="next")
    return next_page["href"] if next_page and next_page.has_attr("href") else None


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []

    # session = requests.Session()
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://habr.com" + next_page
        news.extend(news_list)
        n_pages -= 1

    return news


if __name__ == "__main__":
    from db import save_articles

    articles = get_news("https://habr.com/ru/articles/", n_pages=15)
    save_articles(articles)

    print(f"\nРезультат: собрано {len(articles)} статей")
    if articles:
        print("\nПервые 3 статьи:")
        for idx, article in enumerate(articles[:3], 1):
            print(f"{idx}. {article['title']}")
            print(f"   Автор: {article['author']}")
            print(f"   id: {article['habr_id']}")
            print(f"   сложность: {article['complexity']}")
            print(f"   Ссылка: {article['url']}\n")
