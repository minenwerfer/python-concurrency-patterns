#!/usr/bin/env python3

import time
import random
from threading import Thread
from multiprocessing import Pipe
from select import select

result_r, result_w = Pipe()
timeout_r, timeout_w = Pipe()

def main():
    results = search('teste')
    for r in results:
        print(r)

def search(query: str):
    threads = [
        Thread(target=web, args=(query,)),
        Thread(target=image, args=(query,)),
        Thread(target=video, args=(query,)),
        Thread(target=timeout, args=(4,))
    ]

    for thread in threads:
        thread.daemon = True
        thread.start()

    results = []

    while True:
        ready, *_ = select([result_r, timeout_r], [], [])

        """
        Chooses pseudo-randomly when multiple channels are available.
        """
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

def web(query: str):
    latency = random.randint(1, 5)
    time.sleep(latency)
    result_w.send('web result for "%s" (took %d seconds)' % (query, latency))

def image(query: str):
    latency = random.randint(1, 5)
    time.sleep(latency)
    result_w.send('image result for "%s" (took %d seconds)' % (query, latency))

def video(query: str):
    latency = random.randint(1, 5)
    time.sleep(latency)
    result_w.send('video result for "%s" (took %d seconds)' % (query, latency))

if __name__ == '__main__':
    main()
