import math
from celery import group

from crawler.crawlers import (
    PokemonsCrawler,
    StarWarsCrawler,
)
from football.celery_app import app


@app.task
def crawl_pokemons_page(limit, offset=0):
    return PokemonsCrawler().crawl(limit=limit, offset=offset)


@app.task
def crawl_starwars_page(page=1):
    return StarWarsCrawler().crawl(page=page)


@app.task
def crawl_pokemons():
    limit = 60
    results_left = crawl_pokemons_page(limit)
    if results_left:
        num_pages_left = math.ceil(results_left / limit)
        pages_to_retrieve = range(1, num_pages_left + 1)
        tasks = [
            crawl_pokemons_page.s(limit, page * limit) for page in pages_to_retrieve
        ]
        job = group(*tasks)
        job.apply_async()


@app.task
def crawl_starwars():
    num_pages_left = crawl_starwars_page()
    if num_pages_left:
        pages_to_retrieve = range(1, num_pages_left + 1)
        tasks = [crawl_starwars_page.s(page + 1) for page in pages_to_retrieve]
        job = group(*tasks)
        job.apply_async()


@app.task
def crawl_sources():
    job = group(crawl_pokemons.s(), crawl_starwars.s())
    job.apply_async()
