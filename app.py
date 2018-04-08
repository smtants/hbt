#! /usr/bin python
# -*- coding:utf-8 -*-
#
#   xianwen.zhang
#   2017-12-21

import os, io
import sys
import json, demjson
import time  
from multiprocessing import Process
import tornado.ioloop
import tornado.web
from include import log
from include import mariadbfunc
from include import statuscode

isDebug  = False

#   cache endpoints and items
endpointsMap = {}

class RouterConfig(tornado.web.Application):
    def route(self, url):
        def register(handler):
            self.add_handlers(".*$", [(url, handler)])
            return handler
        return register

app = RouterConfig()

@app.route(r'/v1/hbt/isok')
class V1_HbtHandler(tornado.web.RequestHandler):
    def get(self):
        retJson  = {}
        try:
            retJson['res'] = statuscode.SUCCESS
            retJson['msg'] = "hbt is ok!"
        except Exception as e:
            retJson['res'] = statuscode.API_ABNORMA
            log.lg_write(' ==hbt.v1.hbt.get== ' + str(e))
        
        self.write(retJson)

@app.route(r'/v1/hbt')
class V1_HbtHandler(tornado.web.RequestHandler):
    def post(self):
        endpoint = ''
        ip       = ''
        version  = ''
        retJson  = {}
        try:
            if self.get_argument('endpoint'):
                endpoint = self.get_argument('endpoint')

            if self.get_argument('ip'):
                ip = self.get_argument('ip')

            if self.get_argument('version'):
                version = self.get_argument('version')

            #   parameter cannot be empty
            if endpoint == '' or ip == '' or version == '':
                retJson['res'] = statuscode.REQ_PARAM_ERROR
                return retJson
            
            #   debug
            if isDebug:
                log.lg_debug(str(endpoint) + ' is ok !')
            
            endpointId = 0
            #   endpoint is exists
            if endpointsMap.get(endpoint):
                endpointId = endpointsMap.get(endpoint)[0]
                #   check version
                if not version == endpointsMap.get(endpoint)[1]:
                    #   update version
                    mariadbfunc.update_endpoint_version(endpointsMap.get(endpoint)[0], version)
                else:
                    #   update cache
                    endpointsMap.get(endpoint)[2] = int(time.time())
            else:
                #   add endpoint
                isOk = mariadbfunc.add_endpoint(endpoint, ip, version)
                if isOk:
                    #   add cache
                    endpointId = mariadbfunc.get_endpoint_id(endpoint)
                    if endpointId > 0:
                        endpointArr = []
                        endpointArr.append(endpointId)
                        endpointArr.append(version)
                        endpointArr.append(int(time.time()))
                        endpointsMap[endpoint] = endpointArr

            if endpointId > 0:
                retJson['res'] = statuscode.SUCCESS
            else:
                retJson['res'] = statuscode.DAT_INSERT_FAIL

        except Exception as e:
            retJson['res'] = statuscode.API_ABNORMA
            log.lg_write(' ==hbt.v1.hbt== ' + str(e))
        
        self.write(retJson)

def init():
    try:
        #   traverse the endpoint to get the list of endpoints
        endpointList = mariadbfunc.get_endpoint_list()
        if not endpointList == '':
            for endpoint in endpointList:
                endpointArr = []
                endpointArr.append(endpoint[0])
                endpointArr.append(endpoint[2])
                endpointArr.append(int(time.time()))
                endpointsMap[endpoint[1]] = endpointArr        
    except Exception as e:
        log.lg_write(' ==hbt.init== ' + str(e))
        exit()

#   listen port
#
def hbt(port):
    try:
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()
    except Exception as e:
        log.lg_write(' ==hbt.hbt== ' + str(e))
        exit()

def check_hbt(interval):
    try:
        while True:
            #   draverse endpointsMap check if the endpoint is online
            for key in dict(endpointsMap).keys():
                if int(time.time()) - endpointsMap.get(key)[2] > interval * 2:
                    #   endpoint is not online
                    mariadbfunc.update_endpoint_status(endpointsMap.get(key)[0])
                    #   set msg
                    #   ......
            time.sleep(interval)
    except Exception as e:
        log.lg_write(' ==hbt.check_hbt== ' + str(e))

def main():
    try:
        if not os.path.exists('cfg.json'):
            log.lg_write(' ==hbt.main== cfg.json file is not exists !')
            exit()

        f = io.open('cfg.json', 'r', encoding='utf-8') 
        data = json.load(f)

        if not data['socket']['post']:
            log.lg_write(' ==hbt.main== please enter the correct port !')
            exit()

        interval = data['interval']

        if data['debug']:
            isDebug = True
        
        port = data['socket']['post']

        ph = Process(target = hbt, args = (port,))
        ph.start()

        pc = Process(target = check_hbt, args = (interval,))
        pc.start()
    except Exception as e:
        log.lg_write(' ==hbt.main== ' + str(e))
        exit()

if __name__ == "__main__":
    init()
    main()