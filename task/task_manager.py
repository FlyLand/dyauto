#!/usr/bin/python
# -*- coding: UTF-8 -*-
from playwright.async_api import Playwright,async_playwright
from browser import init_browser
from model import barrage
from model import page_info

async def close(roomid:str):
    context = page_info.get_context_instance().getContextByName(roomid)
    if context is not None:
        await context.close()
    return


async def start(playwright:Playwright,ws_port: int,proxy_port:int,roomid:str) -> None:
    room_url = f"https://live.douyin.com/{roomid}"

    # 历史页面暂时不处理
    browser = await init_browser.getBrowser(playwright)
    context = await browser.new_context()
    mainPage = await context.new_page()
    await mainPage.goto(room_url)
    try:
        # 判断是否已经结束 todo 可能网络问题30S才返回
        await mainPage.wait_for_selector("#giftPanelEntrance",state="visible")
    except:
        return False
    playRoomId = await mainPage.evaluate('window.localStorage.playRoom')
    if playRoomId == None:
        return False
    await context.close()
    await mainPage.close()

    # 先打开软件
    res = await barrage.openExe(roomid,ws_port,proxy_port,playRoomId)
    if not res:
        return False

    context = await browser.new_context(proxy={"server" : f"http://localhost:{proxy_port}"})
    # 测试打开新的页面
    newPage = await context.new_page()
    await newPage.goto(room_url)

    await newPage.pause()
    # await asyncio.sleep(100)

    # loop = asyncio.get_event_loop()
    # future = loop.create_future()
    # ret = await future
    # print('func end with %s' % ret)


class PortConfig():
    wsSet = set()
    proxyProtSet = set()

    def initPortList(self):
        wsPortList = range(10000,10100)
        for w in wsPortList:
            self.wsSet.add(w)

        proxyPortList = range(10200,10300)
        for p in proxyPortList:
            self.proxyProtSet.add(p)


    def grantPort(self):
        return self.wsSet.pop(),self.proxyProtSet.pop()
    
    def addPort(self,wsPort,proxyPort):
        self.wsSet.add(wsPort)
        self.proxyProtSet.add(proxyPort)
        