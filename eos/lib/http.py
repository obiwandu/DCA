#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by lingjiao.lc

"""
Note, in my script, a tab equals four blanks.
You must have a check of your indentation.
"""
 
import os
import sys
import httplib
import json
import urllib
import time

headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}

class HTTP(object):
    def __init__(self, ip, port=8080):
        self.ip = ip
        self.port =port
    
    def post(self, uri,  body='', header='',timeout=60):
        try:
            conn = httplib.HTTPConnection(self.ip, self.port, timeout=timeout)
            if not header:
                header = headers
            conn.request('POST', uri, body, header)
        except Exception, e:
            raise Exception('Call host:%s port:%s error,  error msg:%s' % (self.ip, self.port, str(e)))

        return self.response(conn)

    
    def put(self, uri, body='', header='', timeout=60):
        try:
            conn = httplib.HTTPConnection(self.ip, self.port, timeout=timeout)
            uri = urllib.quote(uri)  
            if not header:
                header = headers
            conn.request('PUT', uri, body, header)
        except Exception, e:
            raise Exception('Call host:%s port:%s error,  error msg:%s' % (self.ip, self.port, str(e)))
        return self.response(conn)
    
    def get(self, uri, body='', timeout=60, quote=True):
        try:
            conn = httplib.HTTPConnection(self.ip, self.port, timeout=timeout)
            if quote:
                uri = urllib.quote(uri)  
            conn.request('GET', uri, body)
        except Exception, e:
            raise Exception('Call host:%s port:%s error,  error msg:%s' % (self.ip, self.port, str(e)))
        return self.response(conn)
    
    def delete(self, uri, timeout=60, body=None, header=''):
        try:
            conn = httplib.HTTPConnection(self.ip, self.port, timeout=timeout)
            uri = urllib.quote(uri)
            if not header:
                    header = headers
            if body :
                conn.request('DELETE', uri, body, header)
            else:
                conn.request('DELETE', uri, '', header)
        except Exception, e:
            raise Exception('Call host:%s port:%s error,  error msg:%s' % (self.ip, self.port, str(e)))
        return self.response(conn)
    
    def response(self, conn):
        try:
            response = conn.getresponse()
            print "response:"
            print response
            status = response.status
            reason = response.reason
            data = response.read()
            if status != 200:
                raise Exception('CALL CONTROLLER: %s:%s ERROR   status:%s reason:%s' % (self.ip, self.port, status, reason))
            conn.close()
            print "data:"
            print data
            return json.loads(data)
        except Exception, e:
            raise Exception('CALL CONTROLLER: %s:%s ERROR:%s' % (self.ip, self.port, str(e)))