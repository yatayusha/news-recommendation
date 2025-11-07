import unittest
from unittest import mock
from unittest.mock import call

from boddle import boddle
from db import News
from habrnews import add_label, classify_news, update_news


class TestHabrnews(unittest.TestCase):
    @mock.patch("habrnews.session")
    def test_add_label(self, session):
        with boddle(query={"id": 1, "label": "never"}):
            news = News(
                title="Ask HN: Do you use an optimization solver? Which one? Do you like it?",
                author="ryan-nextmv",
                url="https://news.ycombinator.com/item?id=31099186",
                complexity="Средний",
                label=None,
            )
            session.return_value.query.return_value.get.return_value = news
            add_label()
            self.assertTrue(news.label == "never")
            self.assertTrue(session.mock_calls[-1] == call().commit())

    @mock.patch("habrnews.get_news")
    @mock.patch("habrnews.session")
    def test_update_news(self, session, get_news):
        news = [
            {
                "author": "ngaut",
                "complexity": "Средний",
                "title": "Go will use pdqsort in next release",
                "url": "https://github.com/golang/go/commit/72e77a7f41bbf45d466119444307fd3ae996e257",
            },
            {
                "author": "electric_muse",
                "complexity": "Средний",
                "title": "Show HN: Two-way Jira sync in a collaborative spreadsheet and Gantt",
                "url": "https://www.visor.us/landing/visor-for-jira-launch",
            },
            {
                "author": "ryan-nextmv",
                "complexity": "Средний",
                "title": "Ask HN: Do you use an optimization solver? Which one? Do you like it?",
                "url": "https://news.ycombinator.com/item?id=31099186",
            },
        ]
        get_news.return_value = news
        session.return_value.query.return_value.filter.return_value.first.side_effect = [
            True,
            False,
            False,
        ]
        update_news()
        n_commit = 0
        for one_call in session.mock_calls:
            if one_call == call().commit() and one_call != call():
                n_commit += 1
        self.assertEqual(2, n_commit)

    @mock.patch("habrnews.session")
    def test_classify_news(self, session):
        news_cl = [
            News(
                title="Just a random example",
                author="ngaut",
                url="https://github.com/golang/go/commit/72e77a7f41bbf45d466119444307fd3ae996e257",
                complexity="Средний",
                label="good",
            ),
            News(
                title="Another name appeared on the wall",
                author="electric_muse",
                url="https://www.visor.us/landing/visor-for-jira-launch",
                complexity="Средний",
                label="maybe",
            ),
            News(
                title="Getting started with Python is easy",
                author="ryan-nextmv",
                url="https://news.ycombinator.com/item?id=31099186",
                complexity="Средний",
                label="never",
            ),
            News(
                title="Getting started with Java is easy",
                author="ryan-nextmv",
                url="https://news.ycombinator.com/item?id=31099186",
                complexity="Средний",
                label="never",
            ),
            News(
                title="One more random example",
                author="ryan-nextmv",
                url="https://news.ycombinator.com/item?id=31099186",
                complexity="Средний",
                label="good",
            ),
        ]
        news_not_cl = [
            News(
                title="A name suddenly appeared on the wall",
                author="ngaut",
                url="https://github.com/golang/go/commit/72e77a7f41bbf45d466119444307fd3ae996e257",
                complexity="Простой",
            ),
            News(
                title="Getting started with C++ is relatively hard",
                author="electric_muse",
                url="https://www.visor.us/landing/visor-for-jira-launch",
                complexity="Простой",
            ),
            News(
                title="Just another random example",
                author="ryan-nextmv",
                url="https://news.ycombinator.com/item?id=31099186",
                complexity="Простой",
            ),
        ]
        session.return_value.query.return_value.filter.return_value.all.side_effect = [
            news_cl,
            news_not_cl,
        ]
        expected = [news_not_cl[2], news_not_cl[0], news_not_cl[1]]
        actual = classify_news()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
