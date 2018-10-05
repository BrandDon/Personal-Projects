from multiprocessing.pool import ThreadPool

import arrow
from apscheduler.schedulers.blocking import BlockingScheduler

from pastebin_crawler.components.crawler import PasteBinCrawler
from pastebin_crawler.components.db_handler import TinyDBHandler
from pastebin_crawler.config import conf


def get_new_urls(paste_urls, db_handler):
    new_urls = []
    last_url = db_handler.get_latest_url()
    if not last_url:
        return paste_urls
    for url in paste_urls:
        if url == last_url:
            break
        new_urls.append(url)
    return new_urls


def main():
    print("Starting to crawl at: {}".format(arrow.utcnow()))
    db = TinyDBHandler()
    crawler = PasteBinCrawler()
    paste_urls = crawler.crawl_main_page()
    new_urls = get_new_urls(paste_urls, db)
    thread_pool = ThreadPool(conf.THREADS_AMOUNT)
    paste_details = thread_pool.map(crawler.crawl_paste, new_urls)
    paste_dicts = [paste.to_dict() for paste in paste_details]
    db.save_multiple_pastes(paste_dicts)
    if len(new_urls) > 0:
        db.save_latest_url(new_urls[0])


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(main, 'interval', minutes=conf.MINUTES_INTERVAL,
                      next_run_time=arrow.utcnow().shift(seconds=5).datetime)  # To prevent skipping the first run
    scheduler.start()
    # TODO: Add README.md
