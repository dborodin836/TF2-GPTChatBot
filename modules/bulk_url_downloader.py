from queue import Queue
from threading import Thread, local
from typing import Any, List, Tuple

import requests
from requests.sessions import Session

from modules.typing import SteamHoursApiUrlID64


class BulkSteamGameDetailsUrlDownloader:
    q: Queue[SteamHoursApiUrlID64] = Queue(maxsize=0)
    results: List = []
    thread_local = local()
    urls: List[SteamHoursApiUrlID64] = []

    def __init__(self, urls: List[SteamHoursApiUrlID64]):
        self.urls = urls

    def _get_session(self) -> Session:
        if not hasattr(self.thread_local, "session"):
            self.thread_local.session = requests.Session()
        return self.thread_local.session

    def _download_link(self) -> None:
        """download link worker, get URL from queue until no url left in the queue"""
        session = self._get_session()
        while True:
            url: SteamHoursApiUrlID64 = self.q.get()
            with session.get(url.url) as response:
                self.results.append((response.json(), url.steamid64))
            self.q.task_done()

    def download_all(self) -> List[Tuple[Any, int]]:
        """Start 10 threads, each thread as a wrapper of downloader"""
        for url in self.urls:
            self.q.put(url)

        thread_num = 10
        for _ in range(thread_num):
            t_worker = Thread(target=self._download_link)
            t_worker.start()
        self.q.join()  # main thread wait until all url finished downloading
        return self.results
