from playwright.async_api import Playwright, async_playwright,Page,Browser
from model import page_info
from common import config
import asyncio


async def getBrowser(playwright: Playwright) -> Browser:
    browser = await playwright.firefox.launch(headless=False)
    return browser

async def createNewPage(contextName:str,browser:Browser,url:str,proxyPort:int=None) -> Page:
    lock = asyncio.Lock() 
    context = page_info.get_context_instance().getContextByName(contextName)
    if context is not None:
        newPage = context.pages[0]
    else:
        if not lock.locked():
            context = await page_info.get_context_instance().createContext(contextName,browser,proxyPort)
            if context == None:
                return
            newPage = await context.new_page()

    await newPage.goto(url)
    return newPage