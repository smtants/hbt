#!/usr/bin python 
# -*- coding: utf-8 -*-
#
#   log file function library
#   prefix with lg_
#   xianwen.zhang
#   2017-11-09

import os,time

# create log file path
# @para    path
#
def lg_create_path(path):
    if not (os.path.exists(path)):
        os.makedirs(path)

# hbt  log
# @para msg
#
def lg_write(msg):
    lg_create_path('./log')
    f = open('./log/app.log','a')
    content = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + msg + "\n"
    f.write(content)
    f.close()

# mariadb log
# @para   msg
#
def lg_write_mariadb(msg):
    lg_create_path('./log')
    f = open('./log/mariadb.error.log','a')
    content = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + msg + "\n"
    f.write(content)
    f.close()

# hbt  debug
# @para msg
#
def lg_debug(msg):
    lg_create_path('./log')
    f = open('./log/debug.log','a')
    content = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + msg + "\n"
    f.write(content)
    f.close()