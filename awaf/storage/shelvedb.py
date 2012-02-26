"""
A simple shelve implementation of Storage.
"""
import shelve

class Storage(shelve.DbfilenameShelf):
    """
    Storage class for a shelve database.
    """
    @staticmethod
    def create(self, filename, *args, **kwargs):
        return Storage(filename)

    commit = shelve.DbfilenameShelf.sync
    __del__ = shelve.DbfilenameShelf.close

