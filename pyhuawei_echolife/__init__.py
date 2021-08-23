from pprint import pp
import requests
import base64
import logging

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)



class API:
    LOGIN_COOKIE = {"Cookie": "body:Language:portuguese:id=-1"}

    def __init__(self, host, username, password) -> None:
        self._host = host
        self._username = username
        self._password = password
        self._get_cookie()

    def _get_cookie(self):
        """Get the auth cookie from the router."""
        cnt = requests.post(f"http://{self._host}/asp/GetRandCount.asp")
        self.X_HW_Token = str(cnt.content, cnt.apparent_encoding, errors="replace")
        _LOGGER.debug("Retrieved X_HW_Token: %s", self.X_HW_Token)


        _LOGGER.debug("Logging in")
        cookie = requests.post(
            f"http://{self._host}/login.cgi",
            data=[
                ("UserName", self._username),
                ("PassWord", base64.b64encode(bytes(self._password, "utf-8"))),
                ("x.X_HW_Token", self.X_HW_Token),
            ],
            cookies=self.LOGIN_COOKIE,
        )

        self.cookie_jar = cookie.cookies
    
    def get(self, path):
        url = f"http://{self._host}{path}"
        _LOGGER.debug("GET %s", url)

        if not self.cookie_jar:
            self._get_cookie()

        data = requests.get(
            url,
            cookies=self.cookie_jar,
        )

        return (
            data.content.decode(data.apparent_encoding)
            .encode()
            .decode("unicode_escape")
        )

    def post(self, path, data):
        url = f"http://{self._host}{path}"
        _LOGGER.debug("POST %s", url)

        if not self.cookie_jar:
            self._get_cookie()

        data = requests.post(
            url,
            cookies=self.cookie_jar,
            data=data,
        )

        return (
            data.content.decode(data.apparent_encoding)
            .encode()
            .decode("unicode_escape")
        )



