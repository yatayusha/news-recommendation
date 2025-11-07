from typing import Any
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base: Any = declarative_base()
engine = create_engine("sqlite:///news.db")
Session = sessionmaker(bind=engine)


class News(Base):  # type: ignore[misc]
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    complexity = Column(String)
    habr_id = Column(String)
    label = Column(String)

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}')>"


Base.metadata.create_all(bind=engine)  # type: ignore[attr-defined]


def save_articles(articles):
    """Сохраняет статьи в базу данных"""
    session = Session()
    try:
        for article in articles:
            # Проверка на дубликаты
            if not session.query(News).filter_by(habr_id=article["habr_id"]).first():
                news_entry = News(
                    title=article["title"],
                    author=article["author"],
                    url=article["url"],
                    complexity=article["complexity"],
                    habr_id=article["habr_id"],
                    label=None,
                )
                session.add(news_entry)
        session.commit()
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        session.rollback()
    finally:
        session.close()
