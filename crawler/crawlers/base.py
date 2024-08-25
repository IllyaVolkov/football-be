import requests
from abc import ABC, abstractmethod

from crawler.models import Source, Pagination


class BaseCrawler(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    def __init__(self):
        self.source = Source.objects.get(name=self.name)

    def fetch_data(self, **kwargs):
        url = f"{self.source.base_url}{self.source.players_path}"

        if self.source.pagination == Pagination.NONE:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json(), None
            else:
                raise Exception(
                    f"Failed to fetch data from {url}. Status code: {response.status_code}"
                )
        elif self.source.pagination == Pagination.LIMIT_OFFSET:
            limit = kwargs.get("limit")
            offset = kwargs.get("offset")
            params = {}
            if limit is not None:
                params["limit"] = limit
            if offset is not None:
                params["offset"] = offset

            response = requests.get(url, params=params)

            if response.status_code == 200:
                res_data = response.json()
                return res_data.get("results"), res_data.get("count")
            else:
                raise Exception(
                    f"Failed to fetch data from {url}. Status code: {response.status_code}"
                )
        elif self.source.pagination == Pagination.PAGE_NUMBER:
            page = kwargs.get("page")
            params = {}
            if page is not None:
                params["page"] = page

            response = requests.get(url, params=params)

            if response.status_code == 200:
                res_data = response.json()
                return (
                    res_data.get("results"),
                    res_data.get("count"),
                    res_data.get("next"),
                )
            else:
                raise Exception(
                    f"Failed to fetch data from {url}. Status code: {response.status_code}"
                )

    @abstractmethod
    def crawl(self, **kwargs):
        pass
