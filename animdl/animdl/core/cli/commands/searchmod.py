import logging

from ...__version__ import __core__
from ...codebase.providers import get_provider
from ...config import DEFAULT_PROVIDER
from .. import helpers
from ..http_client import client

searchre = {}

# @click.command(name="search-mod", help="Search for an anime in the provider. (modified file)")
# @click.argument("query", required=True)
# @click.option(
#     "-p",
#     "--provider",
#     help="Provider to search in.",
#     default=DEFAULT_PROVIDER,
#     type=click.Choice(helpers.provider_searcher_mapping.keys(), case_sensitive=False),
# )
# @helpers.decorators.automatic_selection_options()
# @helpers.decorators.logging_options()
# @click.option(
#     "-j",
#     "--json",
#     help="Output as json.",
#     is_flag=True,
#     flag_value=True,
# ) searchmod.animdl_search_mod(query="animixplay:5-toubun no Hanayome", json=True, provider="animixplay")
# @helpers.decorators.setup_loggers()
outercount = 0 #yes
def animdl_search_mod(query, json, provider):
    logger = logging.getLogger("searcher")

    match, module, _ = get_provider(query, raise_on_failure=False)

    if module is not None:
        genexp = (
            {
                "name": (
                    module.metadata_fetcher(client, query, match)["titles"] or [None]
                )[0]
                or "",
                "anime_url": query,
            },
        )
    else:
        genexp = helpers.provider_searcher_mapping.get(provider)(client, query)

    for count, search_data in enumerate(genexp, 1):
        if json:
            outercount = count
            searchre[count] = search_data
        else:
            logger.info("{0:02d}: {1[name]} {1[anime_url]}".format(count, search_data))
    return searchre, outercount