# coding=utf-8
import winreg
import requests


class ProxyServer:
    def __init__(self):
        self.__path = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
        self.__INTERNET_SETTINGS = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,
                                                    self.__path, 0, winreg.KEY_ALL_ACCESS)

    def get_server_form_Win(self):
        """获取代理配置的ip和端口号"""
        ip, port = "", ""
        if self.is_open_proxy_form_Win():
            try:
                ip, port = winreg.QueryValueEx(self.__INTERNET_SETTINGS, "ProxyServer")[0].split(":")
            except Exception as err:
                print("报错：" + str(err))
        else:
            return "0:0"
        return ip + ":" + port

    def is_open_proxy_form_Win(self):
        """判断是否开启了代理"""
        try:
            if winreg.QueryValueEx(self.__INTERNET_SETTINGS, "ProxyEnable")[0] == 1:
                return True
        except Exception as err:
            print("报错：" + str(err))
        return False


def if_open_vpn():
    ps = ProxyServer()
    ip_port = ps.get_server_form_Win()
    if ip_port == "0:0":
        return False
    else:
        try:
            proxies = {
                'http': ip_port,
                'https': ip_port
            }
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"}
            return requests.get("https://www.youtube.com/youtube", proxies=proxies, headers=headers).status_code == 200
        except requests.exceptions.SSLError:
            return False


print(if_open_vpn())