# -*- coding=utf-8 -*-
# !/usr/bin/env python

from logging import getLogger
from json import dumps




class ResultHandler(object):
    def onResult(self, result):
        raise NotImplementedError

    def obj2str(self, result):
        if type(result) != str:
            # error is ignore
            return dumps(result, skipkeys=True)
        else:
            return result


class LogStore(ResultHandler):
    def __init__(self, name):
        self.logger = getLogger(name)

    def onResult(self, result):
        self.logger.info(self.obj2str(result))


class MongoDBStore(ResultHandler):
    def __init__(self, collection):
        self.collection = collection
        self.producer = get_producer(self.collection)

    def onResult(self, result):
        try:
            del result['_meta']['collection']
        except:
            pass
        self.producer.produce(self.obj2str(result).encode('utf8'))

    def __enter__(self):
        """Context manager entry point - start the producer"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit point - stop the producer"""
        self.producer.stop()


def buildStoreLogOnly(name):
    return LogStore(name)


def buildStoreMongoDB(collection):
    return MongoDBStore(collection)


# TODO: cache the result handler
def get_result_handler(result):
    # Result can be in python dictionary or list form. Convert either to list of dictionaries.
    meta = result.get('_meta', {'store': 'log', 'collection': b'test'})
    store = meta.get('store')
    if store == 'mongodb':
        return buildStoreMongoDB(meta.get('collection', b'test'))
    elif store == 'log':
        return buildStoreLogOnly(meta.get('name', 'test'))



