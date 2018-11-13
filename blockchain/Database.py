import os
from sklearn.externals import joblib


def get_filepath(filepath):
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        filepath))


def initiate_database(filename):
    db = {}
    if filename is not None:
        filename_path = get_filepath(filename)
        if os.path.exists(filename_path):
            db = joblib.load(filename_path)
    return db


class Database(object):
    def __init__(self, filename=None):
        self._db = initiate_database(filename)
        self.filename = filename

    def get_index_count(self):
        return len(self._db.values())

    def get(self, key):
        return self._db[key]

    def put(self, key, value):
        self._db[key] = value

    def delete(self, key):
        del self._db[key]

    def commit(self):
        if self.filename is not None:
            joblib.dump(self._db, self.filename)
