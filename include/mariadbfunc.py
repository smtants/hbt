#!/usr/bin python 
# -*- coding: utf-8 -*-
#
#   mariadb function库
#   xianwen.zhang
#   2017-12-28

import os
import json
from smtants.hbt.include import log 
from smtants.hbt.include import mariadbclient
from smtants.hbt.include import enumhelpr

mariadbclient = mariadbclient.init()

# get endpoint list
# @return  array
# 
def get_endpoint_list():
    data = ''
    try:
        sql  = 'select id, endpoint, version from ops_endpoints'
        data = mariadbclient.query(sql)
    except Exception as e:
        log.lg_write(" ==mariadbfunc.get_endpoint_list== " + str(e))
    return data

# update version
# @return  bool
# 
def update_endpoint_version(endpointId, version):
    isOk = False
    try:
        sql = 'update from ops_endpoints set version="' + str(version) + '" where id=' + str(endpointId)
        isOk = mariadbclient.execute(sql)
    except Exception as e:
        log.lg_write(" ==mariadbfunc.update_endpoint_version== " + str(e))
    return isOk

# add endpoint 
# @return  bool
# 
def add_endpoint(endpoint, ip, version):
    isOk = False
    try:
        sql = 'insert into ops_endpoints (endpoint, ip, version, createdate) values("'
        sql += str(endpoint) + '","' 
        sql += str(ip) + '","' 
        sql += str(version) + '",' 
        sql += 'unix_timestamp(now()))'
        isOk = mariadbclient.execute(sql)
    except Exception as e:
        log.lg_write(" ==mariadbfunc.add_endpoint== " + str(e))
    return isOk

# get endpoint 
# @return  endpoint
# 
def get_endpoint_id(endpoint):
        endpointId = 0
        try:
            sql = 'select id from ops_endpoints where endpoint="' + endpoint + '"'
            if  mariadbclient.query(sql)[0][0] > 0:
                endpointId = mariadbclient.query(sql)[0][0]
        except Exception as e:
            log.lg_write(" ==mariadbfunc.get_endpoint_id== " + str(e))
        return endpointId

# update endpoint status
# @return  bool
# 
def update_endpoint_status(endpointId):
    isOk = False
    try:
        sql = 'update ops_endpoints set status=' + str(enumhelpr.ENUM_STOP_STATUS) + ', updatedate=unix_timestamp(now()) where id=' + str(endpointId)
        isOk = mariadbclient.execute(sql)
    except Exception as e:
        log.lg_write(" ==mariadbfunc.update_endpoint_status== " + str(e))
    return isOk