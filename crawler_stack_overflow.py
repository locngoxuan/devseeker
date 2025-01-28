from crawler import Crawler


class StackOverflowCrawler(Crawler):
    def __init__(self, question: str):
        super().__init__(question)
