import arrow


class PasteParser:
    def parse_title(self, title):
        unknown_titles = ["Untitled"]
        return self._handle_if_unknown(title, unknown_titles)

    def parse_author(self, author):
        unknown_authors = ["Guest", "Unknown", "Anonymous", "a guest"]
        return self._handle_if_unknown(author, unknown_authors)

    @staticmethod
    def parse_date(date):
        date = date.strip()
        if date.endswith("CDT"):
            date = date.replace("CDT", "US/Central")
            # I've only seen time return as CDT, and since I can't parse timezones abbreviations (such as 'CDT') to
            # full tz names ('US/Central') automatically (Some timezones abbreviations have multiple timezones) I assume
            # this is the only possible time
            # Ask hagay
        utc_datetime = arrow.get(date, "Do of MMMM YYYY hh:mm:ss A ZZZ").to('UTC').datetime
        return utc_datetime

    @staticmethod
    def parse_content(content):
        return content.strip()

    @staticmethod
    def _handle_if_unknown(data, possible_unknowns):
        data = data.strip()
        if data.lower() in [unknown.lower() for unknown in possible_unknowns]:
            return ""
        else:
            return data
