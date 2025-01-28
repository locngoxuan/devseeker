from abc import abstractmethod


class Crawler():
    def __init__(self, question: str):
        self.question = question

    @abstractmethod
    def crawl(self):
        pass
