import argparse
import json

from flask import Flask, render_template, request

from crawler_stackexchange import StackExchangeCrawler

app = Flask(__name__)

crawlers = [
    StackExchangeCrawler(),
]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/discover", methods=["POST"])
def discover():
    payload = json.loads(request.data)
    if 'question' not in payload:
        return {
            "code": 400,
            "message": "question must not blank"
        }
    question = payload['question']
    results = []
    for crawler in crawlers:
        rs = crawler.crawl(question)
        if rs is None:
            continue
        results.extend(rs)
    return results

def main():
    parser = argparse.ArgumentParser(
        description="DevSeeker",
        exit_on_error=True,
        prog="devseeker"
    )
    parser.add_argument("-d", "--debug", help="Run application in debug mode", action="store_true")
    parser.add_argument("-p", "--port", help="Port for running webserver", default=8080)
    args = parser.parse_args()
    if args.debug:
        app.run(debug=args.debug, port=args.port, host="0.0.0.0")
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
