osssss
======

Welcome to osssss!

osssss a wrapper for the osu! api.

It's "agnositic" of the requesting backend. Comes with aiohttp and requests options.

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
