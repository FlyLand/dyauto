#!/usr/bin/python
# -*- coding: UTF-8 -*-
import asyncio
from playwright.async_api import Playwright,async_playwright
from browser import init_browser
from common import config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import page

# filePath = "F:/code/python/dyauto/f.txt"
filePath = "./"
class FileHandle(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"File {event.src_path} was modified")
        # 读取文件内容
        # todo 可以读取多行作为队列使用，为了方便读一行
        line = ""
        with open("./aa.txt",'r') as f:
            line = f.readline()
        if line == "":
            return
        
        # 解析文件内容
        es = line.split("    ")
        name = es[0]
        wsPort = es[1]
        proxyPort = es[2]
        asyncio.run(page.run(None))
        # 开协程处理
        

async def run(playwright: Playwright) -> None:
    # 无限期挂起
    # 历史页面暂时不处理
    browser = await init_browser.getBrowser(playwright=playwright)
    # 测试打开新的页面
    mainPage = await init_browser.createNewPage(config.default_page_name,browser,"https://www.baidu.com")
    if mainPage is None:
        print("create mainPage error")
        return
    eventHandle = FileHandle()
    obs = Observer()
    obs.schedule(eventHandle,filePath,recursive=True)
    obs.start()
    while True:
        await asyncio.sleep(1)

async def mainTask():
    async with async_playwright() as playwright:
        await run(playwright)

