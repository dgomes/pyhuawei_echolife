
import argparse
from datetime import datetime, timedelta

from pyhuawei_echolife import API
from pyhuawei_echolife.ipincoming import IPIncomming

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Manage Huawei Echolife IPv4 Filter.')
    parser.add_argument('router_address', help='router address')
    parser.add_argument('username', help='router admin username')
    parser.add_argument('password', help='router admin password')
    parser.add_argument('--ips', metavar='IPs', nargs='+', help='ips block/unblock')
    parser.add_argument('--action', choices=['purge', 'list', 'block', 'unblock'], default="block", help="Action to perform with ips")
    

    args = parser.parse_args()

    api = API(args.router_address, args.username, args.password)
    fw = IPIncomming(api)

    if args.action == 'list':
        for filter in fw.table:
            print(f"{filter.ip} - {datetime.fromtimestamp(int(float(filter.description)))}")
    elif args.action == 'purge':
        for filter in fw.table:
            if datetime.now() - datetime.fromtimestamp(int(float(filter.description))) > timedelta(hours=1):
                fw.unblock(filter.ip)
                print(f"unblocking {filter.ip} after {datetime.now() - datetime.fromtimestamp(int(float(filter.description)))}")
    else:
        for ip in args.ips:
            if args.action == 'block' and not fw.in_table(ip):
                fw.block(ip, datetime.now().timestamp())
                print(f"blocking {ip}")
            elif args.action == 'unblock' and fw.in_table(ip):
                fw.unblock(ip)
                print(f"unblocking {ip}")

            

