#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script prints some basic index info about collection whether to use frequently.

Notice:
1. Statistics for an index will be reset on mongod restart or index drop and recreation.
2. Prior to version 3.2.3, the ops field value did not include $match or mapReduce operations that use indexes.
3. The statistics reported by the accesses field only includes index access driven by user requests. It does not include internal operations like deletion via TTL Indexes or chunk split and migration operations.
"""
import sys
import psutil
from prettytable import PrettyTable
from pymongo import MongoClient
from optparse import OptionParser

def get_cli_options():
    parser = OptionParser(usage="usage: python %prog [options]",
                          description="""This script prints some basic index info about collection whether to use frequently.""")
    parser.add_option("-H", "--host",
                      dest="host",
                      default="localhost",
                      metavar="HOST",
                      help="MongoDB host")
    parser.add_option("-p", "--port",
                      dest="port",
                      default=27017,
                      metavar="PORT",
                      help="MongoDB port")
    parser.add_option("-d", "--database",
                      dest="database",
                      default="",
                      metavar="DATABASE",
                      help="Target database to generate statistics. All if omitted.")
    parser.add_option("-u", "--user",
                      dest="user",
                      default="",
                      metavar="USER",
                      help="Admin username if authentication is enabled")
    parser.add_option("--password",
                      dest="password",
                      default="",
                      metavar="PASSWORD",
                      help="Admin password if authentication is enabled")
    (options, args) = parser.parse_args()
    return options

# Get MongoDB connection
def get_client(host, port, username, password):
    try:
        client = MongoClient(host=host,port=int(port),username=username,password=password,authSource='admin',authMechanism='SCRAM-SHA-1')
        return client
    except Exception as e:
        print('connect to server failed:%s' % e)

# Get index stat info
def get_index_stats(database, collection):
    pipeline = [{"$indexStats":{ }},{"$project":{"name":1,"accesses.ops":1,"accesses.since":1}}]
    index_stats = database.command('aggregate', collection, pipeline=pipeline, explain=False)
    return index_stats['result']

def main(options):
    client = get_client(options.host, options.port, options.user, options.password)
    all_index_stats = {}

    databases = []
    if options.database:
        databases.append(options.database)
    else:
        databases = client.database_names()

    for db in databases:
        if db == "local":
            continue
        database = client[db]
        all_index_stats[database.name] = []
        for collection_name in database.collection_names():
            index_stats = get_index_stats(database,collection_name)
            ns = db + '.' + collection_name
            all_index_stats[ns] = index_stats

    x = PrettyTable(["Collection", "Index Name", "Access Times", "Since Time"])
    x.align["Collection"]  = "l"
    x.align["Index Name"]  = "l"
    x.align["Access Times"]  = "l"
    x.align["Since Time"]  = "l"
    x.padding_width = 1

    for ns in all_index_stats:
        index_stats = all_index_stats[ns]
        for index_stat in index_stats:
            if index_stat["name"] != '_id_' and int(index_stat["accesses"]["ops"]) == 0:
                index_name = index_stat["name"].split(',')[0]
                x.add_row([ns,index_name,int(index_stat["accesses"]["ops"]),index_stat["accesses"]["since"]])
    print x.get_string(sortby="Collection")

if __name__ == "__main__":
    options = get_cli_options()
    main(options)
