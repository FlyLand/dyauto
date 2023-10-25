from multiprocessing import Process,SimpleQueue,Manager
from playwright.async_api import async_playwright
from browser import init_browser
import time,asyncio,api
from task import task_manager
import json

def startChrome(roomid,ws_port,proxy_port):
    asyncio.get_event_loop().run_until_complete(run(ws_port,proxy_port,roomid))

async def run(ws_port,proxy_port,roomid):
    async with async_playwright() as playwright:
        await task_manager.start(playwright,ws_port,proxy_port,roomid)

taskManager = dict()
runningTask = dict()

# 获取子线程
def getTaskByName(name) -> Process | None:
    if name in taskManager.keys():
        return taskManager[name]
    else:
        return None

def startApi(q,pmanager):
    api.run(q,pmanager)

def createApiTask(q,pmanager):
    p = Process(target=startApi,name="api",args=(q,pmanager))
    p.daemon = True
    p.start()

# 創建綫程
def createTask(portConfig,roomid):
    ws_port,proxy_port = portConfig.grantPort()
    p = Process(target=startChrome,name=roomid,args=(roomid,ws_port,proxy_port))
    p.daemon = True
    taskManager[roomid] = {"process":p,"roomid":roomid,"ws_port":ws_port,"proxy_port":proxy_port,"start_time":0}


def createProcess(portConfig,roomid):
    # 判断是否已经存在
    if roomid in taskManager.keys() or roomid in runningTask.keys():
        return True
    createTask(portConfig,roomid)
    return True
    
def closeProcess(roomid,pmanager):
    if roomid not in runningTask:
        return
    
    rtiem = runningTask.get(roomid)

    if rtiem['process'].is_alive():
        rtiem['process'].kill()
    if roomid in pmanager.keys():
        pmanager.pop(roomid)
    runningTask.pop(roomid)
    print(f"{rid} is closed")

def restartProcess(portConfig,roomid,pmanager):
    if roomid in runningTask:
        closeProcess(roomid,pmanager)
    return createProcess(portConfig,roomid)

if __name__ == '__main__':
    q = SimpleQueue()
    pmanager = Manager().dict()

    portConfig = task_manager.PortConfig()
    portConfig.initPortList()
    createApiTask(q,pmanager)
    while True:
        if not q.empty():
            context = q.get()
            qcontext = json.loads(context)
            if "create" == qcontext["type"]:
                createProcess(portConfig,qcontext["roomid"])
            if "close" == qcontext["type"]:
                closeProcess(qcontext["roomid"],pmanager)
            if "restart" == qcontext["type"]:
                restartProcess(portConfig,qcontext["roomid"],pmanager)
        
        if len(taskManager) > 0:
            rid,item = taskManager.popitem()
            p = item['process']
            if not p.is_alive():
                p.start()
                item["pid"] = p.pid
                item["start_time"] = int(time.time())
                runningTask[rid] = item
                pitem = item.copy()
                pitem['process'] = ""
                pmanager[rid] = pitem
            else:
                taskManager[rid] = item

        if len(runningTask) > 0:
            for rid in list(runningTask.keys()):
                item = runningTask[rid]
                p = item['process']
                if not p.is_alive():
                    if int(time.time()) - item["start_time"] > 5:
                        p.kill()
                        runningTask.pop(rid)
                        pmanager.pop(rid)
                else:
                    print(item["roomid"])
                    pass
        
        time.sleep(3)
            



    
    
    