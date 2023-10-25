from playwright.async_api import BrowserContext,Browser

# 最好是不要进行tab的关闭操作,否则比较难管理
class TabInfo():
    def __init__(self,name:str,index:int) -> None:
        self.name = name
        self.index = index #在pageList中的index，一旦已经创建好，需要修改还是比较麻烦

class PageInfo():
    def __init__(self,name:str) -> None:
        self._tabList = {}
        self._name = name
    
    def getPageName(self) -> str:
        return self._name

    def addTabList(self,t:TabInfo):
        self._tabList[t.name] = t

    def getPageList(self) -> {}:
        return self._tabList
    
    def getTabByName(self,tabName:str) -> TabInfo:
        if tabName in self._tabList:
            return self._tabList[tabName]
        return None
                
class PageListInfo():
    def __init__(self) -> None:
        self._pageList = {}

    def addPageInfo(self,t:PageInfo):
        self._pageList[t.getPageName()] = t
    
    def getPageInfoByName(self,tabName:str) -> PageInfo:
        if tabName in self._pageList:
            return self._pageList[tabName]
        return None
    

class ContextInfo():
    _context_list = dict()

    def __init__(self) -> None:
        pass

    def getContextByName(self,name) -> BrowserContext:
        if name in self._context_list.keys():
            return self._context_list[name]
        return None
    
    def addContextByName(self,name:str,context:BrowserContext) -> None: 
        self._context_list[name] = context
    
    async def createContext(self,name:str,browser:Browser,proxyPort:int = None) -> BrowserContext:
        proxy = None
        if proxyPort is not None:
            proxy = {"server" : f"http://localhost:{proxyPort}"}
            
        context = await browser.new_context(proxy=proxy)
        self.addContextByName(name,context)
        return context

global _context_instance
_context_instance = None

def get_context_instance() -> ContextInfo: 
    global _context_instance
    if _context_instance == None:
        _context_instance = ContextInfo()
    return _context_instance