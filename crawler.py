from abc import abstractmethod


class Crawler():
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def crawl(self, question: str):
        pass
