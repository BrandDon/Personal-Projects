from bs4 import BeautifulSoup
import requests
from pastebin_crawler.components.data_models.Paste_data_model import Paste


class PasteBinCrawler:
    def __init__(self):
        self._session = requests.Session()
        self._base_url = "https://pastebin.com"

    def crawl_main_page(self):
        bs = self._get_bs_page(self._base_url + "/archive")
        paste_links = []

        for tr in bs.find_all('tr')[1:]:
            paste_link = tr.td.a.get('href')
            paste_links.append(self._base_url + paste_link)
        return paste_links

    def crawl_paste(self, url):
        bs = self._get_bs_page(url)
        title = self._get_title(bs)
        author = self._get_author(bs)
        date = self._get_date(bs)
        content = self._get_content(bs)
        paste_details = Paste(title, content, author, date)
        return paste_details

    def _get_bs_page(self, url):
        res = self._session.get(url)
        bs = BeautifulSoup(res.text, "html.parser")
        return bs

    @staticmethod
    def _get_author(bs):
        details_bar = bs.find(attrs={'class': 'paste_box_line2'})
        if details_bar.a is None:  # User is logged out
            return details_bar.contents[2]
        else:
            return details_bar.a.text

    @staticmethod
    def _get_title(bs):
        return bs.find(attrs={'class': 'paste_box_line1'}).h1.text

    @staticmethod
    def _get_date(bs):
        return bs.find(attrs={'class': 'paste_box_line2'}).span['title']

    @staticmethod
    def _get_content(bs):
        return bs.find('textarea').text
