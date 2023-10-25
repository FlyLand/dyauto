from playwright.async_api import Playwright,Browser

async def getBrowser(playwright: Playwright) -> Browser:
    browser = await playwright.firefox.launch(headless=False)
    return browser