osssss
======

Welcome to osssss!

osssss a wrapper for the osu! api.

It's "agnositic" of the requesting backend, insofar as it provides a method "get" that takes a url and a params dict.

Using with aiohttp
```py
from osuapi import OsuApi
import aiohttp

async def get_peppy_user_id():
	api = OsuApi("mykey", connector=aiohttp)
	results = await api.get_user("peppy")
	return results[0].user_id
```

Or requests
```py
from osuapi import OsuApi
import requests

api = OsuApi("mykey", connector=requests)
results = api.get_user("peppy")
```
