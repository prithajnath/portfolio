import logging
import os
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

RADIAL_CHART_AXES = ["Python", "JavaScript", "HTML"]


@cache.cached(timeout=50)
def fetch_repo_stats():
    data = []
    repos = [
        "my-secret-santa",
        "prithajnath.github.io",
        "mmc",
        "fnalgo",
        "nytscraper",
        # "homebash",
    ]
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
                stats[language] = scaled_loc / total_loc

        data.append(stats)

    return data


@app.route("/")
def index():
    return render_template("about.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


# JSON endpoints
@app.route("/github")
def github():
    data = fetch_repo_stats()
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
