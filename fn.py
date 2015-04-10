#!/usr/bin/python
import api
import sys

def amisane(apikey,apisecret):
    sanity = True
    if apikey == '':
        return False
    if apisecret == '':
        return False
    return sanity

