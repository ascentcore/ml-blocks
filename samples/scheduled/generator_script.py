import random
import time
import requests
import threading


def printit():
    header = ['x', 'y', 'c']
    with open('tmp.csv', 'w') as file:
        file.write('time,x,y,c\n')
        for i in range(0, 300):
            file.write(
                f'{time.ctime(time.time())},{random.random()},{random.random()},{random.random()}\n')

    requests.post('http://localhost:9080/api/v1/data/upload_files',
                  files={'files': open('tmp.csv', 'rb')}, data={'append': True})


printit()
