#!/usr/bin/env python3

import time
import random
from threading import Thread
from multiprocessing import Pipe
from select import select

result_r, result_w = Pipe()
timeout_r, timeout_w = Pipe()

"""
The scope where the Pipe is declared is relevant.
search() loop will block if the following statement is placed inside first().
"""
replica_r, replica_w = Pipe()

def main():
    results = search('teste')
    for r in results:
        print(r)

def first(query: str, *replicas):
    threads = [
        Thread(target=replica, args=(query, replica_w))
        for replica in replicas
    ]

    for thread in threads:
        thread.daemon = True
        thread.start()

    while True:
        result = replica_r.recv()
        result_w.send(result)
        break

def search(query: str):
    threads = [
        Thread(target=first(query, web, web2, web3)),
        Thread(target=first(query, image, image2, image3)),
        Thread(target=first(query, video, video2, video3)),
        Thread(target=timeout, args=(4,))
    ]

    for thread in threads:
        thread.daemon = True
        thread.start()

    results = []

    while True:
        ready, *_ = select([result_r, timeout_r], [], [])
        which = random.choice(ready)
        if which == result_r:
            results.append(result_r.recv())
            if len(results) == 3:
                break

        if which == timeout_r:
            print('Timed out!')
            break

    return results

def timeout(seconds: int):
    time.sleep(seconds)
    timeout_w.send(True)

def web(query: str, chan=result_w):
    latency = random.randint(1, 5)
    time.sleep(latency)
    try:
        chan.send('web result for "%s" (took %d seconds)' % (query, latency))
    except:
        pass

def image(query: str, chan=result_w):
    latency = random.randint(1, 5)
    time.sleep(latency)
    try:
        chan.send('image result for "%s" (took %d seconds)' % (query, latency))
    except:
        pass

def video(query: str, chan=result_w):
    latency = random.randint(1, 5)
    time.sleep(latency)
    try:
        chan.send('video result for "%s" (took %d seconds)' % (query, latency))
    except:
        pass

web2 = web3 = web
image2 = image3 = image
video2 = video3 = video

if __name__ == '__main__':
    main()
