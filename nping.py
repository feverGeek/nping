'''
Author: Zeta 
Date: 2020-09-24 22:45:24
LastEditTime: 2020-09-25 00:31:00
LastEditors: Please set LastEditors
Description: 异步发包实现多地ping,测试域名ip
'''
import asyncio
import aiohttp
import requests
import myguids
import time

url = 'http://ping.chinaz.com/iframe.ashx?t=ping'
callbacks = ['jQuery111305132493189017003_1600955943436']
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '126',
    'Origin': 'http://ping.chinaz.com',
    'Connection': 'close',
    'Referer': 'http://ping.chinaz.com/baidu.com'
}


async def post(url, headers, params, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params, headers=headers) as response:
                return await response.read()


def main():
    host = 'baidu.com'
    params = 'guid={guid}&host={host}&ishost=0&isipv6=0&encode=zxvXAfWZuer8pEY3YyErCfPjF~0gqfqG&checktype=0'.format(
        guid='{guid}', host=host)
    # semaphore = asyncio.Semaphore(20)  # 限制并发数10
    # loop = asyncio.get_event_loop()
    # tasks = []
    # for callback in callbacks:
    #     task = asyncio.ensure_future(
    #         post(url.format(callback), headers, params, semaphore))
    #     tasks.append(task)
    # results = loop.run_until_complete(asyncio.gather(*tasks))
    # print(results)
    # loop.close()
    for guid in myguids.guids:
        r = requests.post(url, headers=headers, data=params.format(guid=guid))
        print(r.text)


if __name__ == "__main__":
    main()
