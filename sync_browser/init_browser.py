from playwright.async_api import Playwright,Page,Browser
from model import page_info
from common import config
import asyncio

async def getBrowser(playwright: Playwright) -> Browser:
    _browser = await playwright.chromium.launch(headless=False)

    return _browser