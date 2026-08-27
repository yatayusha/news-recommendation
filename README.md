# Personalized News Recommendation System

An end-to-end personalized news recommendation system that collects articles from Habr, stores user interaction data, learns user preferences from labeled content, and generates a ranked news feed.

## Overview

The project addresses the problem of **information overload**: users are exposed to a large volume of content but only a small portion of it is relevant to their interests.

The system collects news articles from Habr, allows users to label articles according to their preferences, and uses these interactions to classify and rank new content.

The final output is a **personalized ranked list of news articles**.

## Business Problem

News platforms continuously publish new content, making it difficult for users to efficiently find articles that match their interests.

The system answers the following question:

> Which available articles are most relevant to a particular user?

User feedback is used to learn preferences and assign one of three classes to incoming articles:

* **Interesting**
* **Maybe Later**
* **Not Interesting**

The resulting predictions are used to rank the available news feed.

## Project Architecture

```text
Habr
  │
  ▼
Data Collection
Requests + BeautifulSoup
  │
  ▼
Data Storage
SQLite + SQLAlchemy
  │
  ▼
User Feedback
Article Labeling
  │
  ▼
Text Preprocessing
  │
  ▼
Naive Bayes Classifier
  │
  ▼
Article Classification
  │
  ▼
Ranked News Feed
```

## Implementation

### 1. Data Collection

The system collects news articles from Habr using HTTP requests and HTML parsing.

For each article, the following information is extracted:

* title
* author
* article URL
* complexity level
* Habr article ID

The scraper supports collecting news from multiple pages.

### 2. Data Storage

Collected articles and user labels are stored in a SQLite database using SQLAlchemy.

The database stores structured article information together with the corresponding user feedback.

### 3. User Feedback and Data Labeling

A lightweight web interface allows users to label previously unseen articles.

Three labels are available:

* **Interesting** — the user is interested in the article
* **Maybe Later** — the user may read the article later
* **Not Interesting** — the article is not relevant to the user

These labels are used as training data for the classification model.

## Machine Learning

The recommendation pipeline uses a **Naive Bayes classifier** to predict the relevance class of a news article.

The classification process can be represented as:

```text
Article Text
     │
     ▼
Text Features
     │
     ▼
Naive Bayes Classifier
     │
     ▼
Predicted User Preference
     │
     ▼
Ranked Recommendations
```

The implementation includes:

* text preprocessing
* class probability estimation
* Lidstone/Laplacian smoothing
* logarithmic probability calculations
* prediction of article classes

The classifier was validated on the SMS Spam Collection dataset and achieved an accuracy of approximately **98.2%** on the test set.

The implementation was also compared with `MultinomialNB` from scikit-learn.

## Recommendation Output

After classification, previously unseen news articles are organized according to their predicted relevance.

The resulting feed prioritizes:

1. Interesting articles
2. Articles that may be relevant
3. Not Interesting articles

This produces a personalized ranked news feed based on the user's historical feedback.

## Tech Stack

**Programming**

* Python

**Data Collection**

* Requests
* BeautifulSoup

**Data Storage**

* SQLite
* SQLAlchemy

**Web Interface**

* Bottle
* Semantic UI

**Machine Learning**

* scikit-learn
* Naive Bayes

**Data Processing**

* CSV
* `collections.Counter`
* `defaultdict`
