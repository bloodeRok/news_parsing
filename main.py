from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup as bs
import csv
import time
import os

from requests import Response

from constants import HEADERS, URL
from exceptions import StatusCodeException


def get_response_from_bybit(url: str) -> Response:
    """
    Sends a GET request to the specified URL with custom headers.

    Args:
        url (str): The URL to send the request to.

    Returns:
        Response: The response object.

    Raises:
        StatusCodeException: When the response status code is not 200.
    """

    response = requests.get(url=url, headers=HEADERS)
    if response.status_code != 200:
        raise StatusCodeException(response)
    return response


def get_all_news() -> list[dict[str, str]]:
    """
    Retrieves a list of news articles from Bybit announcements page.

    Returns:
        list[dict[str, str]]: A list of dictionaries
         containing news information.
    """

    not_empty = True
    news_list = []
    current_page = 0
    while not_empty:
        current_page += 1
        response = get_response_from_bybit(url=URL.format(page=current_page))

        soup = bs(response.content, "html.parser")
        if soup.find("div", class_="article-list-empty"):
            break
        raw_news = soup \
            .find("div", class_="article-list") \
            .find_all("a", class_="no-style")

        for news in raw_news:
            title = news.find("span").text
            link = "https://announcements.bybit.com" + news.attrs["href"]
            news_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
            news_list.append(
                {
                    "page": current_page,
                    "news_id": raw_news.index(news),
                    "title": title,
                    "link": link,
                    "time": news_time
                }
            )

    return news_list


def get_updated_news(last_news: dict[str, str]) -> list[dict[str, str]]:
    """
    Retrieves updated news articles since the last checked news.

    Args:
        last_news (dict[str, str]): The last checked news article.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing updated news information.
    """

    current_page = 0
    news_list = []
    while True:
        current_page += 1
        response = get_response_from_bybit(url=URL.format(page=current_page))

        soup = bs(response.content, "html.parser")
        raw_news = soup \
            .find("div", class_="article-list") \
            .find_all("a", class_="no-style")

        for news in raw_news:
            title = news.find("span").text
            if last_news["title"] == title:
                return news_list
            link = "https://announcements.bybit.com" + news.attrs["href"]
            news_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S%Z")
            news_list.append(
                {
                    "page": current_page,
                    "news_id": raw_news.index(news),
                    "title": title,
                    "link": link,
                    "time": news_time
                }
            )


def save_to_csv(
        news_list: list[dict[str, str]],
        file_name: Optional[str] = None
) -> str:
    """
    Saves a list of news articles to a CSV file.

    Args:
        news_list (list[dict[str, str]]): A list of dictionaries containing news information.
        file_name (Optional[str]): The name of the CSV file. If not provided, it will be generated.

    Returns:
        str: The name of the saved CSV file.
    """

    if not file_name:
        file_name = \
            f"bybit_news-{datetime.now().strftime('%Y-%m-%dT%H-%M')}.csv"

    with open(
            file_name,
            mode="a",
            encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            delimiter=";",
            fieldnames=["page", "news_id", "title", "link", "time"],
            lineterminator="\n"
        )
        if os.stat(file_name).st_size == 0:
            writer.writeheader()
        for news in news_list:
            writer.writerow(news)
        return file_name


def check_news_update(last_local_news: dict[str, str]) -> bool:
    """
    Checks if there are any new news articles on the server.

    Args:
        last_local_news (dict[str, str]): The last checked local news article.

    Returns:
        bool: True if there are new articles, False otherwise.
    """

    response = get_response_from_bybit(url=URL.format(page=1))
    soup = bs(response.content, "html.parser")
    last_server_news_title = soup \
        .find("div", class_="article-list") \
        .find_all("a", class_="no-style")[0] \
        .find("span").text

    if last_server_news_title == last_local_news["title"]:
        return False
    return True


def main() -> None:
    """
    Main function to run the news scraping and updating process.
    """

    news_list = get_all_news()
    file_name = save_to_csv(news_list=news_list)
    while True:
        is_news_update = check_news_update(last_local_news=news_list[0])

        if is_news_update:
            unregistered_news = get_updated_news(last_news=news_list[0])
            for news in unregistered_news[::-1]:
                news_list.insert(0, news)
            save_to_csv(news_list=unregistered_news, file_name=file_name)
        time.sleep(1)


if __name__ == "__main__":
    main()
