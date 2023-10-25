#!/usr/bin/python
# -*- coding: UTF-8 -*-
import asyncio,os,subprocess
from common import config

temple = '''<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <appSettings>
    <add key="processFilter" value="firefox" />
    <add key="wsListenPort" value="{wsPort}" />
    <add key="listenAny" value="true" />
    <add key="proxyPort" value="{proxyPort}" />
    <add key="printBarrage" value="true" />
    <add key="printFilter" value="1,2,5" />
    <add key="usedProxy" value="false" />
    <add key="filterHostName" value="true" />
    <add key="hostNameFilter" value="" />
    <add key="roomIds" value="{playRoom}" />
  </appSettings>
  <runtime>
    <assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
      <dependentAssembly>
        <assemblyIdentity name="System.Memory" publicKeyToken="cc7b13ffcd2ddd51" culture="neutral" />
        <bindingRedirect oldVersion="0.0.0.0-4.0.1.2" newVersion="4.0.1.2" />
      </dependentAssembly>
    </assemblyBinding>
  </runtime>
</configuration>'''

def _grantTemple(wsPort,proxyPort,playRoom) -> bool:
    return temple.replace('{wsPort}',f"{wsPort}").replace('{proxyPort}',f"{proxyPort}").replace('{playRoom}',f"{playRoom}")

def replaceFile(wsPort,proxyPort,playRoom,roomid):
    tempText = _grantTemple(wsPort,proxyPort,playRoom)
    conf_path = config.getExeConfigName(roomid)
    # 新增一个默认配置
    with open(conf_path,'w') as f:
        f.write(tempText)

    os.replace(conf_path,config.getExeConfigName())
    
async def _replaceConfig(roomid,wsPort,proxyPort,playRoom) -> bool:
    if roomid == "":
        return False

    lock = asyncio.Lock()
    try:
        if not lock.locked():
            await lock.acquire()
            # 替换文件名称
            replaceFile(wsPort,proxyPort,playRoom,roomid)
            return True
    except Exception as e:
        print(e)
        lock.release()
    return False

async def openExe(roomid,wsPort,proxyPort,playRoom) -> bool:
    result = await _replaceConfig(roomid,wsPort,proxyPort,playRoom)
    if not result:
        return False
    
    # 先打开软件
    filePath = config.exe_work_path + os.sep + config.exe_name
    openResult = subprocess.Popen([filePath],stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     encoding='gb2312').stdout.readline()
    if openResult.find("Server started at") != -1:
        return True
    return False