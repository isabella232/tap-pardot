#!/usr/bin/env python3
import singer
import json
from singer import utils
from .client import Client
from .discover import discover
from .sync import sync

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = ["start_date", "email", "password", "user_key"]

@utils.handle_top_exception(LOGGER)
def main():

    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    client = Client(args.config)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover(client)
        print(json.dumps(catalog, indent=2))
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog =  discover(client)

        sync(client, args.config, args.state, catalog)

if __name__ == "__main__":
    main()
