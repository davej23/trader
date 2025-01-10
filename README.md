# Trader - Python Library for T212 API
This library provides a Pythonic interface to the T212 API. It ensures consistency with the current documentation (as of January 2025) and inputs/outputs are validated with Pydantic.

## WARNING
This library is a work in progress, has not been tested and comes with no warranty.

## Usage
API token is automatically pulled from the environment variable `T212_API_TOKEN`.

```python
from trader.client import T212Client
from trader.types import T212Server

client = T212Client(server=T212Server.DEMO)
client.pies.get_pies()
```
