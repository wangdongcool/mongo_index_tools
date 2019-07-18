This script prints some basic index info about collection whether to use frequently.

Notice:
1. Statistics for an index will be reset on mongod restart or index drop and recreation.
2. Prior to version 3.2.3, the ops field value did not include $match or mapReduce operations that use indexes.
3. The statistics reported by the accesses field only includes index access driven by user requests. It does not include internal operations like deletion via TTL Indexes or chunk split and migration operations.

author:wangdongdong, author product environment: python 2.7.5

you can download it directory,before use it, You must install it relies on modules，execute pip install psutil/prettytable/pymongo/optparse

Usage: python mongo_index_access.py [options]

This script prints some basic index info about collection whether to use
frequently.

Options:
  -h, --help            show this help message and exit
  -H HOST, --host=HOST  MongoDB host
  -p PORT, --port=PORT  MongoDB port
  -d DATABASE, --database=DATABASE
                        Target database to generate statistics. All if
                        omitted.
  -u USER, --user=USER  Admin username if authentication is enabled
  --password=PASSWORD   Admin password if authentication is enabled
  
  If any problem, you can contact the author, send email to 986499346@qq.com

for example:
python mongo_index_access.py --host=localhost --user=username --password='123456' --port=27017  --database=py_grepwang
