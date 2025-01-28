import argparse

from flask import Flask, render_template, request

from crawler_stackexchange import StackExchangeCrawler

app = Flask(__name__)

crawlers = [
    StackExchangeCrawler(),
]


@app.route("/", methods=["GET", "POST"])
def index():
    question = None
    results = []
    if request.method == "POST":
        question = request.form.get("question")
        results = [f"Result {i} for question {question}" for i in range(1, 6)]
        for crawler in crawlers:
            crawler.crawl(question)
    return render_template("index.html", question=question, results=results)


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
