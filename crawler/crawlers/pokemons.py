import requests

from crawler.crawlers.base import BaseCrawler
from crawler.models import Player


class PokemonsCrawler(BaseCrawler):
    @property
    def name(self):
        return "Pokemons"

    def crawl(self, **kwargs):
        results, count = self.fetch_data(**kwargs)
        bulk_create_list = []

        for result in results:
            player_url = result.get("url")
            response = requests.get(player_url)
            if response.status_code == 200:
                player = response.json()
            else:
                raise Exception(
                    f"Failed to fetch data from {player_url}. Status code: {response.status_code}"
                )
            name = player.pop("name")
            weight = player.pop("weight") / 10  # Convert hg to kg
            height = player.pop("height") * 10  # Convert dm to cm
            unique_id = str(player.pop("id", name))
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

        offset = kwargs.get("offset", 0)
        results_left = count - (offset + len(results))
        return results_left
