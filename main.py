import json
import logging
import threading
import time
from typing import Callable

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

f = open('config.json')
config = json.load(f)


def main():
    if 'shellyDevices' not in config:
        raise Exception(f'shellyDevices missing in config')

    halloween()


def run(func: Callable, value: int = 0):
    threads: list[threading.Thread] = []
    for name, device in config['shellyDevices'].items():
        ip = device['ip']
        channel = device['channel']
        type = device['type']
        thread = threading.Thread(target=func, name=name, args=[name, ip, channel, type, value])
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def halloween():
    while True:
        run(dimm, 1)
        run(off)
        time.sleep(4)
        run(dimm, 100)
        run(on)
        time.sleep(4)
        run(off)
        for i in range(1, 20):
            run(dimm, 5)
            time.sleep(0.3)
            run(dimm, 10)
            time.sleep(0.3)
        run(dimm, 100)
        run(on)
        time.sleep(2)
        run(dimm, 1)
        run(off)
        for i in range(1, 10):
            run(dimm, 1)
            time.sleep(1)
            run(dimm, 80)
            time.sleep(1)
        run(dimm, 1)
        run(on)
        time.sleep(3)


def on(name: str, ip: str, channel: int, type: str, value: int = 0):
    if type != 'relay':
        return

    requests.get(url=f'http://{ip}/{type}/{channel}?turn=on')
    logger.warning(f'{name}\ton')


def off(name: str, ip: str, channel: int, type: str, value: int = 0):
    if type != 'relay':
        return

    requests.get(url=f'http://{ip}/{type}/{channel}?turn=off')
    logger.warning(f'{name}\toff')


def dimm(name: str, ip: str, channel: int, type: str, value: int = 0):
    if type != 'light':
        return

    value = int(value)

    requests.get(url=f'http://{ip}/{type}/{channel}?brightness={value}')
    logger.warning(f'{name}\t{value}%')


if __name__ == "__main__":
    main()
