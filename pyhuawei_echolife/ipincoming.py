from pyhuawei_echolife import API
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint as pp

from collections import namedtuple

FilterIn = namedtuple("FilterIn", "inFilterInId ip description")

class IPIncomming:
    def __init__(self, api) -> None:
        self._api = api

        self._table = []

        page = self._api.get('/html/bbsp/ipincoming/ipincoming.asp')

        for line in page.split('\n'):
            if "new stFilterIn" in line:
                block_regex_res = re.compile(r"new stFilterIn\((.*?)\),").findall(line)
                for block in block_regex_res:
                    ip_filter_id,_,_, _,_,_, ip, _, _, _, _, _, _, name = block.split(",")
                    self._table.append(FilterIn(ip_filter_id[1:][:-1], ip[1:][:-1], name[1:][:-1]))


        soup = BeautifulSoup(page, 'html.parser')

        for _input in soup.find_all('input', {'name':'onttoken'}):
            self._api.X_HW_Token = _input.get('value')
    

    @property
    def table(self):
        return self._table

    def in_table(self, ip):
        for filter in self._table:
            if filter.ip == ip:
                return True
        return False

    def block(self, ip, description) -> None:

        data = {
            'x.Protocol': 'ALL',
            'x.Direction': 'Bidirectional',
            'x.Name': description,
            'x.SourceIPStart': '',
            'x.SourceIPEnd': '',
            'x.DestIPStart': ip,
            'x.DestIPEnd': '',
            'x.LanSideTcpPort': '',
            'x.LanSideUdpPort': '',
            'x.WanSideTcpPort': '',
            'x.WanSideUdpPort': '',
            'x.X_HW_Token': self._api.X_HW_Token
        }

        return self._api.post('/html/bbsp/ipincoming/add.cgi?x=InternetGatewayDevice.X_HW_Security.IpFilterIn&RequestFile=html/bbsp/ipincoming/ipincoming.asp', data)

    def unblock(self, ip):

        for entry in self._table:
            if ip == entry.ip:
                data = {
                    entry.inFilterInId: '',
                    'x.X_HW_Token': self._api.X_HW_Token
                }

                return self._api.post(f'/html/bbsp/ipincoming/del.cgi?x={entry.inFilterInId}&RequestFile=html/bbsp/ipincoming/ipincoming.asp', data)


