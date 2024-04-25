import os, sys
import json
import re

def helloworldProjectPaths():
    print('say helloworld')
    return "say helloworld"

def dilutePath(path_with_keyword):
    # ('dilutePath: '+path_with_keyword)
    diluted_path = path_with_keyword

    for i in range(1,30):
        diluted_path = diluted_path.replace('/','_')
        diluted_path = diluted_path.replace('\\','_')
        diluted_path = diluted_path.replace('(','_')
        diluted_path = diluted_path.replace(')','_')
        diluted_path = diluted_path.replace(' ','_')
        diluted_path = diluted_path.replace("__",'_')
        diluted_path = diluted_path.replace(".",'_')
        diluted_path = diluted_path.replace(",",'_')
        diluted_path = diluted_path.replace("$",'_')
        diluted_path = diluted_path.replace("|",'_')
        diluted_path = diluted_path.replace("+",'_')
        diluted_path = diluted_path.replace(":",'_')
        diluted_path = diluted_path.replace("-",'_')
        diluted_path = diluted_path.replace(".",'_')
        diluted_path = diluted_path.replace("__",'_')

        diluted_path = re.sub(r'\s+', '_', diluted_path)

        # re to replace the right most _
        diluted_path = re.sub(r'_+$', '', diluted_path)

    return diluted_path

# for testing
if __name__ =="__main__":
    # result = dilutePath(r'hello\world')
    # result = dilutePath(r'hello__world')
    result = dilutePath(r'hello____.........______........._---------_____.........______........._____|||||_.........______world')
    # result = dilutePath(r'Software Engineer (local/overseas/mainland graduates/IANG visa holders are...')

    # jobsdb_73981461_Director / Deputy Director, Intelligent IoT System
    # result = dilutePath(r'jobsdb_73981461_Director / Deputy Director, Intelligent IoT System')

    # result = dilutePath('hello world')
    print(result)
