import json
from functools import partial

import lxml.html as htmlparser
import regex

from ....config import NINEANIME
from ...helper import construct_site_based_regex
from .decipher import decrypt_url, encrypt_url

REGEX = construct_site_based_regex(
    NINEANIME, extra_regex=r"/watch/[^&?/]+\.(?P<slug>[^&?/]+)"
)
TITLES_REGEX = regex.compile(r'<h1 itemprop="name" class="title" .+?>(.+?)</h1>')

SOURCES = {
    "41": "vidstream",
    "28": "mycloud",
    "35": "mp4upload",
    "40": "streamtape",
    "43": "videovard",
}


def fetch_episode(session, data_sources):
    for server_id, data_hash in data_sources.items():
        response = session.get(
            NINEANIME + "ajax/anime/episode", params={"id": data_hash}
        )
        if response.status_code >= 400:
            continue

        yield {
            "stream_url": decrypt_url(response.json().get("url")),
            "further_extraction": (
                SOURCES.get(server_id),
                {"headers": {"referer": NINEANIME}},
            ),
        }


def fetcher(session, url, check, match):
    slug = match.group("slug")

    for episode in htmlparser.fromstring(
        session.get(
            NINEANIME + "ajax/anime/servers",
            params={"id": slug, "vrf": encrypt_url(slug)},
        )
        .json()
        .get("html")
    ).cssselect("a[title][data-sources][data-base]"):
        number = int(episode.get("data-base", 0))
        if check(number):
            yield partial(
                lambda data_sources: fetch_episode(session, data_sources),
                data_sources=json.loads(episode.get("data-sources")),
            ), number


def metadata_fetcher(session, url, match):

    response = session.get(url).text

    return {"titles": TITLES_REGEX.findall(response)}
