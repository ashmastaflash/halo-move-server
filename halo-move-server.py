#!/usr/bin/python

#import time
import sys
import getopt
import api
import json
import fn

def main(argv):
    config={}
    #First, we get the vars from the config file
    execfile("config.conf",config)
    config["usagetext"] = str("halo-move-server.py -s SERVERID -g GROUPID\n"+
                 "This script moves SERVERID to GROUPID.")
    serverolist = []
    # Next, we attempt to parse args from CLI, overriding vars from config file.
    try:
        opts, args = getopt.getopt(argv, "hs:g:",["serverid=","groupid="])
    except getopt.GetoptError:
        print config["usagetext"]
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print config["usagetext"]
            sys.exit()
        elif opt in ("-s","--serverid"):
            config["serverid"] = arg
        elif opt in ("-g", "--groupid"):
            config["groupid"] = arg

    try:
        #iterations = config["iterations"]
        s_id = config["serverid"]
        g_id = config["groupid"]
        clientid = config["clientid"]
        clientsecret = config["clientsecret"]
        host = config["host"]
    except:
        print 'Error setting variables.  Check your config and options.\n'+str(config["usagetext"])
        sys.exit(2)

    # Sanity check, let's make sure that we aren't speaking crazytalk
    sanity = fn.amisane(clientid,clientsecret)
    if sanity == False:
        print "Insane in the membrane.  Crazy insane, got no keys."
        sys.exit(2)
    try:
        # Call the routine to set the autentication token
        authtoken = api.get_authtoken(host,clientid,clientsecret)
    except:
        print "Failed to get auth token!!!"

    # Get server info
    try:
        server_info,s_respcode = api.get_server_info(host, authtoken, s_id)
        group_info,g_respcode = api.get_group_info(host, authtoken, g_id)
    except:
        print "Attempt to get server or group info failed!!!"
        print "Server:\n",json.dumps (server_info, sort_keys=True, indent=4)
        print "Group:\n",json.dumps (group_info, sort_keys=True, indent=4)
        sys.exit(1)
    try:
        movestatus,respcode = api.server_move(host,authtoken,s_id,g_id)
    except:
        # Print server info
        print 'Server failed to move!!  Info (collected before attempt to move) follows:'
        print 'Server response code:'+str(s_respcode)+'\ninfo:\n',json.dumps(server_info, sort_keys=True, indent=4)
        print 'Group response code:'+str(g_respcode)+'\ninfo:\n',json.dumps(group_info, sort_keys=True, indent=4)
        sys.exit(1)
    print 'Move successful!'
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
