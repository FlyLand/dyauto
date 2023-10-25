import os
main_page_name = "mainPage"
exe_work_path = ".\dyauto\wssBarrageService"
exe_name = "WssBarrageService.exe"
conf_name = "WssBarrageService.exe.config"
default_page_name = "default"
server_host = "139.155.155.73"

def getExeConfigName(roomid:str=""):
    return exe_work_path + os.sep + conf_name + roomid

pages_map = {
    # name : url
    default_page_name: "https://www.baidu.com",
}

def getUrlByPagesMap(key:str) -> str:
    if key not in pages_map:
        return ""
    return pages_map[key]