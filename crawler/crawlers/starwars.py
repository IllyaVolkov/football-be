import math

from crawler.crawlers.base import BaseCrawler
from crawler.models import Player


class StarWarsCrawler(BaseCrawler):
    @property
    def name(self):
        return "StarWars"

    def crawl(self, **kwargs):
        results, count, next = self.fetch_data(**kwargs)
        bulk_create_list = []

        for player in results:
            name = player.pop("name")
            try:
                weight = float(player.pop("mass"))
                height = float(player.pop("height"))
            except ValueError:
                continue
            unique_id = name
            bulk_create_list.append(
                Player(
                    name=name,
                    weight=weight,
                    height=height,
                    unique_id=unique_id,
                    source=self.source,
                    additional_data=player,
                )
            )
        Player.objects.bulk_create(bulk_create_list, ignore_conflicts=True)

        page = kwargs.get("page", 1)
        has_more_results = bool(next)
        results_left = (count - (page * len(results))) if has_more_results else 0
        num_pages_left = math.ceil(results_left / len(results)) if results_left else 0
        return num_pages_left
