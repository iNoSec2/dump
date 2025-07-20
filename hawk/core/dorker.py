import concurrent.futures

from core.goop import search
from core.values import var
from urllib.parse import quote_plus

def dorker(dork):
    num = 0
    results = {}
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=int(var['threads']))
    futures = (threadpool.submit(search, dork, var['cookie'], page=i, full=True) for i in range(var['pages']))
    for i in concurrent.futures.as_completed(futures):
        result = i.result()
        if result:
            for each_result in result:
                results[num] = result[each_result]
                num += 1
        else:
            var['stop_crawling'] = True
    return results
