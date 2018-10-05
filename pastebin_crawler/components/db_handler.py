from tinydb import TinyDB

from pastebin_crawler.config import conf


class TinyDBHandler:
    def __init__(self):
        db = TinyDB(conf.DB_PATH)
        self.pastes_table = db.table('Pastes')
        self.url_table = db.table('URL')

    def save_paste(self, paste_dict):
        self.pastes_table.insert(paste_dict)

    def save_multiple_pastes(self, paste_dicts):
        self.pastes_table.insert_multiple(paste_dicts)

    def save_latest_url(self, url):
        self.url_table.insert({"URL": url})

    def get_latest_url(self):
        last_row = self.url_table.get(doc_id=len(self.url_table))
        if last_row is None:
            return None
        return last_row["URL"]
