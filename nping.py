'''
Author: Zeta 
Date: 2020-09-24 22:45:24
LastEditTime: 2020-09-25 23:54:49
LastEditors: Please set LastEditors
Description: 异步发包实现多地ping,测试域名ip
'''
import re
import asyncio
import aiohttp
import myguids
# import requests
# import time
# import datetime

url = 'http://ping.chinaz.com/iframe.ashx?t=ping'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://ping.chinaz.com',
    'Connection': 'close',
    'Referer': 'http://ping.chinaz.com/'
}


async def post(url, headers, params, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=params, headers=headers) as response:
                return await response.read()


def get_ips(responses):

    ips = []
    reg = r"{state:.*?,msg:'.*?',result:{ip:'(.*?)',ipaddress:'.*?',responsetime:'.*?',ttl:'.*?',bytes:'.*?'}}"
    pattern = re.compile(reg)

    for response in responses:
        response = response[1:-1]  # 去掉响应中的括号
        ip = pattern.findall(response)[0]
        ips.append(ip)

    return ips


def nping(host):

    headers['Referer'] = headers['Referer'] + host
    params = 'guid={guid}&host={host}&ishost=0&isipv6=0&encode=zxvXAfWZuer8pEY3YyErCfPjF~0gqfqG&checktype=0'.format(
        guid='{guid}', host=host)

    tasks = []
    semaphore = asyncio.Semaphore(20)  # 限制并发数20
    loop = asyncio.get_event_loop()
    # time1 = datetime.datetime.now()
    for guid in myguids.guids:
        task = asyncio.ensure_future(
            post(url, headers, params.format(guid=guid), semaphore))
        tasks.append(task)
        # print(params.format(guid=guid))
    responses = loop.run_until_complete(asyncio.gather(*tasks))
    # time2 = datetime.datetime.now()
    # print("delta time: %d" % ((time2 - time1).seconds))
    loop.close()

    ips = get_ips(responses)
    return ips


if __name__ == "__main__":
    host = 'baidu.com'
    ips = nping(host)
