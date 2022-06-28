import random
import time
import requests
import threading


def printit():
    header = ['x', 'y', 'c']
    with open('tmp.csv', 'w') as file:
        file.write('time,x,y,c\n')
        for i in range(0, 300):
            x = -1 + random.random() * 2
            y = -1 + random.random() * 2
            c  = 0
            if x > 0 and y < 0:
                c = 1
            elif x < 0 and y > 0:
                c = 2
            elif x > 0 and y > 0:
                c = 3
            file.write(
                f'{time.ctime(time.time())},{x},{y},{round(c)}\n')

    requests.post('http://localhost:9080/api/v1/data/upload_files',
                  files={'files': open('tmp.csv', 'rb')}, data={'append': False})


printit()
