#!/usr/bin/env python3

import time
import random
from threading import Thread
from queue import Queue

q_result = Queue(maxsize=0)

def main():
    results = search('teste')
    for r in results:
        print(r)

def search(query: str):
    threads = [
        Thread(target=web, args=(query,)),
        Thread(target=image, args=(query,)),
        Thread(target=video, args=(query,))
    ]

    for thread in threads:
        thread.start()

    results = []

    while True:
        results.append(q_result.get())
        if len(results) == len(threads):
            break

    return results


def web(query: str):
    latency = random.randint(1, 5)
    time.sleep(latency)
    q_result.put('web result for "%s" (took %d seconds)' % (query, latency))

def image(query: str):
    latency = random.randint(1, 5)
    time.sleep(latency)
    q_result.put('image result for "%s" (took %d seconds)' % (query, latency))

def video(query: str):
    latency = random.randint(1, 5)
    time.sleep(latency)
    q_result.put('video result for "%s" (took %d seconds)' % (query, latency))

if __name__ == '__main__':
    main()
