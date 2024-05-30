import logging
import os
from dataclasses import dataclass
from random import gauss
from statistics import mean, stdev

import requests
from flask import Flask, jsonify, render_template
from flask_caching import Cache

config = {
    "DEBUG": (
        False if os.getenv("ENVIRONMENT") == "production" else True
    ),  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "CACHE_DEFAULT_TIMEOUT": 300,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
logger = logging.getLogger()

RADIAL_CHART_AXES = ["Python", "JavaScript", "Ruby", "HTML"]


@dataclass
class MetaTag:
    image: str
    url: str
    title: str
    description: str


description = """Hi, my name is Prithaj and I'm a software engineer who likes dabbling in everything data. I have spent most of my career building complex ETL pipelines for machine learning models using Python, SQL, Ruby and Apache Airflow. I'm also proficient in Linux system administration, terraforming resources on AWS, writing CI/CD pipelines using GitHub Actions/Gitlab CI, containerizing projects using Docker and Kubernetes, web-scraping using scrapy, Puppeteer and BeautifulSoup."""

tag = MetaTag(
    image="https://res.cloudinary.com/dzmp7xptn/image/upload/v1716908380/radial_s0kfqq.png",
    url="https://prithaj.dev",
    title="Prithaj Nath - Python/SQL/Docker",
    description=description,
)


@cache.cached(timeout=200)
def fetch_repo_stats():
    data = []
    repos = ["nytscraper", "FeedMeWhatever", "my-secret-santa", "HackerRank"]
    urls = [
        f"https://api.github.com/repos/prithajnath/{repo}/languages" for repo in repos
    ]
    print(f"Fetching stats for {urls}")
    access_token = os.getenv("GH_ACCESS_TOKEN")
    for url in urls:
        resp = requests.get(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        languages = resp.json()
        max_loc = max(languages.values())
        total_loc = sum([v for k, v in languages.items()])
        stats = {}

        for language in RADIAL_CHART_AXES:
            if loc := languages.get(language):
                value = loc / total_loc
                stats[language] = value
            else:
                if len(languages) > 1:
                    avg_loc = mean(languages.values())
                    stdev_loc = stdev(languages.values())

                    scaled_loc = gauss(mu=avg_loc, sigma=stdev_loc)
                else:
                    scaled_loc = gauss(mu=500, sigma=120)
                stats[language] = abs(scaled_loc) / total_loc

        data.append(stats)

    return data


@app.route("/")
def index():

    return render_template("about.html", meta=tag, description=description)


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", meta=tag)


# JSON endpoints
@app.route("/github")
def github():
    data = fetch_repo_stats()
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
