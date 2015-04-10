#!/usr/bin/python



import urllib
import httplib
import base64
import json
import urlparse
import sys

def apihit(host,conntype,authtoken,queryurl,reqbody):
    retdata = ''
    connection = httplib.HTTPSConnection(host)
    tokenheader = {"Authorization": 'Bearer ' + authtoken, "Content-type": "application/json", "Accept": "text/plain"}
    if conntype == "GET":
        connection.request(conntype, queryurl, '', tokenheader)
    else:
        connection.request(conntype, queryurl, json.dumps(reqbody), tokenheader)
    response = connection.getresponse()
    respbody = response.read().decode('ascii', 'ignore')
    respcode = response.status
    try:
        jsondata = respbody.decode()
        retdata = json.loads(jsondata)
    except:
        retdata = respbody.decode()
    connection.close()
    return retdata,respcode

def get_group_info(host,authtoken,grp_id):
    queryurl = '/v1/groups/'+str(grp_id)+'/'
    results,respcode = apihit(host, 'GET', authtoken, queryurl, '')
    return results, respcode

def get_server_info(host,authtoken,node_id):
    queryurl = '/v1/servers/'+str(node_id)+'/'
    results,respcode = apihit(host, 'GET', authtoken, queryurl, '')
    return results,respcode

def server_move(host,authtoken,node_id,d_groupid):
    reqbody= {"server":{"group_id":d_groupid}}
    queryurl = '/v1/servers/'+str(node_id)
    print "Attempting to move SERVER: "+str(node_id)+" to GROUP: "+d_groupid
    resp,respcode = apihit(host, 'PUT', authtoken, queryurl, reqbody)
    if resp != '':
        print "Taking a ride on the failboat... failed to move server to new group\nURL: "+str(queryurl)+"\nResponse code: "+str(respcode)
        sys.exit(2)
    return True,respcode

def get_authtoken(host,clientid,clientsecret):
    # Get the access token used for the API calls.
    connection = httplib.HTTPSConnection(host)
    authstring = "Basic " + base64.b64encode(clientid + ":" + clientsecret)
    header = {"Authorization": authstring}
    params = urllib.urlencode({'grant_type': 'client_credentials'})
    connection.request("POST", '/oauth/access_token', params, header)
    response = connection.getresponse()
    jsondata =  response.read().decode()
    data = json.loads(jsondata)
    try:
        if 'read+write' not in data['scope']:
            print "This script requires RW api access.  Exiting"
            sys.exit(2)
    except:
        print "We're having trouble getting a session token.  Please check your API key."
        print "Error output: "
        print data
        sys.exit()
    key = data['access_token']
    connection.close()
    return key

