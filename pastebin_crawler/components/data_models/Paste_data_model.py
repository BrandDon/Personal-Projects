from pastebin_crawler.components.parser import PasteParser


class Paste:
    def __init__(self, title, content, author, date):
        _parser = PasteParser()
        self.date = _parser.parse_date(date)
        self.title = _parser.parse_title(title)
        self.author = _parser.parse_author(author)
        self.content = _parser.parse_content(content)

    def to_dict(self):
        return {"Title": self.title,
                "Author": self.author,
                "Content": self.content,
                "Date": str(self.date)}
