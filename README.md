This script prints some basic index info about collection whether to use frequently.

Notice:
1. Statistics for an index will be reset on mongod restart or index drop and recreation.
2. Prior to version 3.2.3, the ops field value did not include $match or mapReduce operations that use indexes.
3. The statistics reported by the accesses field only includes index access driven by user requests. It does not include internal operations like deletion via TTL Indexes or chunk split and migration operations.

author:wangdongdong, author product environment: python 2.7.5
