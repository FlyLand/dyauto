# 开启个最简单的http协议处理
from aiohttp import web
from playwright.async_api import Playwright, async_playwright,Page
import json,time
from common import config

app = web.Application()
workspan = dict()
async def start_handle(request):
    roomid = request.match_info.get('roomid')
    if roomid == "":
        return web.Response(text="error")
    que = app["queue"]
    que.put(json.dumps({"type":"create","roomid":roomid}))
    return web.Response(text="success")

async def close_handle(request):
    roomid = request.match_info.get('roomid')
    if roomid == "":
        return web.Response(text="error")
    
    que = app["queue"]
    que.put(json.dumps({"type":"close","roomid":roomid}))
    time.sleep(3)
    pmanager = app["pmanager"]
    res = "success"
    if roomid in pmanager.keys():
         res = "failed"
    return web.Response(text=res)

async def check_handle(request):
    roomid = request.match_info.get('roomid')
    text = "failed"
    if roomid == "":
        return web.Response(text=text)
    
    pmanager = app["pmanager"]
    if roomid in pmanager.keys():
         port = pmanager[roomid]["ws_port"]
         text = json.dumps({"ws_url":f"ws://{config.server_host}:{port}"})
    
    return web.Response(text=text) 

async def restart(request):
    roomid = request.match_info.get('roomid')
    if roomid == "":
        return web.Response(text=text)
    text = "success"
    que = app["queue"]
    que.put(json.dumps({"type":"restart","roomid":roomid}))
    return web.Response(text=text) 

# 开启新程序
app.router.add_get('/start/{roomid}', start_handle)
# 关闭程序
app.router.add_get('/close/{roomid}', close_handle)
# 检查程序
app.router.add_get('/check/{roomid}', check_handle)
# 重启
app.router.add_get('/restart/{roomid}', restart)

def run(q,pmanager):
    app["queue"] = q
    app["pmanager"] = pmanager
    web.run_app(app=app)
         



