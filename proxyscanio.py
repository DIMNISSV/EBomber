from urllib.request import urlopen
from http.client import HTTPResponse
from threading import Thread


class GetProxiesError(Exception):
    pass


class ProxyScanIO:

    API_URL = "https://www.proxyscan.io/api/proxy?format=txt&"

    @staticmethod
    def _is_digit(obj=None) -> bool:
        return (isinstance(obj, int) or isinstance(obj, float))

    def Get_Proxies(self,
                    count: int = 20,
                    **kwargs) -> tuple:
        """
Parameter	Value	        Description

Level	    transparent,    
            anonymous,      
            elite           

Type	    http, https,
            socks4, socks5	Proxy Protocol

Last_Check	Any Number	    Seconds the proxy was last checked
Port	    Any Number	    Proxies with a specific port
Ping	    Any Number	    How fast you get a response after
                            you've sent out a request
Limit	    1 - 20	        How many proxies to list.
Uptime	    1 - 100	        How reliably a proxy has been running
Country	    2 Any Letters   Country of the proxy
Not_Country	2 Any Letters   Avoid proxy countries
"""

        if self._is_digit(count):
            self._limit = (count if isinstance(count, int)
                           else int(count))
        else:
            self._limit = 20
        self._end_link = self.API_URL

        for param in kwargs:
            value = kwargs[param]
            self._end_link += f"{param.lower()}={value}&"
        self._end_link = self._end_link[:-1]

        self._make_requests()

        return self._result

    def _add_result(self, limit: int=20) -> None:
        proxies = tuple()
        with_empty = self.error_with_empty
        while (len(proxies) < limit):
            try:
                url = f"{self._end_link}&limit={limit}"
                resp: HTTPResponse = urlopen(url)
                proxies += tuple(resp.read().decode("UTF-8")
                                 .splitlines())
                if len(proxies) == 0:
                    with_empty -= 1
                self._result += proxies
            except Exception as Error:
                if not self.suppressing_exceptions:
                    raise Error
            if not with_empty:
                raise GetProxiesError("Too many requests were unsuccessful.")

    def _make_requests(self) -> None:
        integer: tuple = (1,)*(self._limit//20)
        non_int = self._limit % 20 / 20,
        self._result = tuple()
        threads = tuple()
        for i in integer+non_int:
            t = Thread(target=self._add_result, args=(int(i*20),))
            t.start()
            threads += t,

        for t in threads:
            t.join()

    def __init__(self, API_URL: str = API_URL,
                 error_with_empty: int = 3,
                 suppressing_exceptions: bool = True) -> None:
        self.error_with_empty = error_with_empty
        self.suppressing_exceptions = suppressing_exceptions
        if API_URL != self.API_URL:
            self.API_URL = API_URL
