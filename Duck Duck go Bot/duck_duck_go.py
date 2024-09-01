# from duckpy import Client

# client = Client()

# results = client.search("snakes")
# print(results)

# # # Prints first result title
# # print(results[0].title)

# # # Prints first result URL
# # print(results[0].url)

# # # Prints first result description
# # print(results[0].description)

import asyncio
from duckpy import AsyncClient

client = AsyncClient()

async def get_results():
  results = await client.search("Python")
  print(results)
#   # Prints first result title
#   print(results[0].title)

#   # Prints first result URL
#   print(results[0].url)

#   # Prints first result description
#   print(results[0].description)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_results())