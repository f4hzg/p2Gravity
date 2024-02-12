#coding: utf8

import sys

# a function to find an item on the p2 server.
# I took this from the old version of the GRAVITY p2 tools
def find_item(item_name, containerId, api, item_type=None):
    items, itemsVersion = api.getItems(containerId)
    for it in items:
        b_name = it['name'] == item_name
        if item_type is None:
            b_type = True
        else:
            b_type = it['itemType'] == item_type
        if (b_name & b_type):
            return it
    return None

def printinp(msg):
    """Request an input from the user using a message preceded by [INPUT]:"""
    r = input("[INPUT]: "+msg)
    return r

def args_to_dict(args):
    """Convert arguments to a dict. 
    Key/values are extracted from args given as "key=value".
    Args given as "--key" are converted to key = True in the dict.
    """
    d = {}
    d['script'] = args[0]
    for arg in args[1:]:
        if arg[0:2] == '--':
            d[arg[2:]] = "True"
        elif len(arg.split('=', 1)) == 2:
            d[arg.split('=', 1)[0]] = arg.split('=', 1)[1]
        else:
            continue
    return d

def printwar(msg):
    print("[WARNING] " + msg)

def printerr(msg):
    print("[ERROR] " + msg)
    sys.exit()

def printinf(msg):
    print("[INFO] " + msg)    
