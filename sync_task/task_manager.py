#!/usr/bin/python
# -*- coding: UTF-8 -*-
from playwright.async_api import Playwright,async_playwright
from browser import init_browser
from model import barrage
from common import config
import asyncio,json
from queue import Queue
from model import page_info

async def run(playwright: Playwright,q: Queue) -> None:
    # 无限期挂起
    # 历史页面暂时不处理
    browser = await init_browser.getBrowser(playwright=playwright)
    # 测试打开新的页面
    mainPage = await init_browser.createNewPage(config.default_page_name,browser,"https://www.baidu.com")
    if mainPage is None:
        print("create mainPage error")
        return
    
    while True:
        item = q.get(block=True)
        djson = json.loads(item)
        dealQueue(playwright,djson)


async def mainTask(q:Queue):
    async with async_playwright() as playwright:
        await run(playwright,q)


dealFunc = {
    "start" : lambda : start,
    "close" : lambda : close,
}

async def dealQueue(playwright,djson:dict):
    type = djson["type"]
    ws_port = djson["ws_port"]
    proxy_port = djson["proxy_port"]
    roomid = djson["roomid"]
    deal = dealFunc[type](playwright,ws_port,proxy_port,roomid)
    return deal

async def close(roomid:str):
    context = page_info.get_context_instance().getContextByName(roomid)
    if context is not None:
        await context.close()
    return


async def start(ws_port: int,proxy_port:int,roomid:str) -> None:
    room_url = f"https://live.douyin.com/{roomid}"

    # 历史页面暂时不处理
    browser = await init_browser.getBrowser()
    # 测试打开新的页面
    mainPage = await init_browser.createNewPage(config.default_page_name,browser,room_url)
    if mainPage is None:
        print("create mainPage error")
        return
    playRoomId = await mainPage.evaluate('window.localStorage.playRoom')
    await mainPage.close()
    
    # 先打开软件
    res = await barrage.openExe(roomid,ws_port,proxy_port,playRoomId)
    if not res:
        return False

    # 测试打开新的页面
    newPage = await init_browser.createNewPage(roomid,browser,room_url,proxy_port)
    if newPage is None:
        print("create mainPage error")
        return

    loop = asyncio.get_event_loop()
    future = loop.create_future()
    ret = await future
    print('func end with %s' % ret)

    # ---------------------
    # browser.close()

# 生成端口
def grantPort():
    wssPort = 123456
    proxyPort = 321
    return wssPort,proxyPort