#!/usr/bin/python
# -*- coding:utf-8; mode:python-mode -*-

import urllib
import sys
import os, os.path
import re
import threading

import time

download_ext = ['jpeg', 'JPEG', 'jpg', 'JPG', 'png', 'PNG'] 

class DLThread(threading.Thread):

    Max_Try_Count = 5
    Max_Semaphore = 50

    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.try_count = 0
        self.pool_sema = threading.Semaphore()


    def run( self ):
        self.pool_sema.acquire( self.Max_Semaphore )
        self._dl()
        self.pool_sema.release()


    def _dl( self ):
        name = os.path.basename( self.url )

        try:
            print ('Saving...%s' % (name))

            if self.try_count < self.Max_Try_Count:
                self.try_count += 1
            else:
                print ('Give Up! %s is None.' % ( name ) )
                return

            urllib.urlretrieve(self.url, name)

        except:
            print "Waiting 5 seconds..."
            time.sleep(5)
            self._dl()


    def _dl2(self):

        c = ""

        for e in download_ext:
            c += "%s," % e
            cmd = re.sub(',$', '', c)

        os.system('wget --continue --tries=5 --quiet -N --accept=%s %s' % (cmd, self.url))


f = open(sys.argv[1])
b = f.read()
f.close()


result = []

for type in download_ext:
    result += re.findall('h?ttp://.*\.%s' % type, b)

if not os.access('dl-temp', os.F_OK):
    os.mkdir('dl-temp')

os.chdir('dl-temp')
result.sort()

thread_list = []

for i in range(len(result)):
    #  if front of URL is ttp
    if not result[i][0] == 'h':
        result[i] = 'h' + result[i]
    elif result[i]:
        continue

#    thread.start_new_thread(dl2, (result[i],))
    th = DLThread( result[i] )
    th.start()
    thread_list.append(th)
    print ( "%d/%d[%d]" % (i, len(result),  len(result) - i ) )
#    time.sleep(0.3)
#    dl(n)
    

for _thread in thread_list:
    _thread.join()
