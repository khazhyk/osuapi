osuapi
======
[![pip](https://img.shields.io/pypi/v/osuapi.svg)](https://pypi.python.org/pypi/osuapi/)
[![Documentation Status](http://readthedocs.org/projects/osuapi/badge/?version=latest)](http://osuapi.readthedocs.io/en/latest/?badge=latest)

Welcome to osssss!

osuapi a python wrapper for the osu! api.

It's "agnostic" of the requesting backend. Uses "connectors" to handle making requests and retrieving json.
Comes with `aiohttp` and `requests` implementations.

Using with aiohttp
```py
from osuapi import OsuApi, AHConnector
import aiohttp
import asyncio

async def get_peppy_user_id():
	api = OsuApi("mykey", connector=AHConnector())
	results = await api.get_user("peppy")
	return results[0].user_id

results = asyncio.get_event_loop().run_until_complete(get_peppy_user_id())
```

Or requests
```py
from osuapi import OsuApi, ReqConnector
import requests

api = OsuApi("mykey", connector=ReqConnector())
results = api.get_user("peppy")
```
