import logging
import os

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


@cache.cached(timeout=50)
def fetch_repo_stats():
    data = []
    repos = [
        "my-secret-santa",
        "prithajnath.github.io",
        "mmc",
        "anc",
        "fnalgo",
        "homebash",
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
        total_loc = sum([v for k, v in languages.items()])
        stats = {language: loc / total_loc for language, loc in languages.items()}
        data.append(stats)
    s = set()
    for repo in data:
        s = s.union(repo.keys())
    axis = list(s)
    for repo in data:
        for key in axis:
            repo[key] = repo.get(key, 0.0)
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
