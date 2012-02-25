import unittest
import tempfile
import os

from www.storage import shelvedb

class TestShelveStorage(unittest.TestCase):

    def setUp(self):
        fd, self.filename = tempfile.mkstemp('awaf_storage_shevle.db', 'wn+b')
        os.close(fd)
        os.unlink(self.filename)
        self.db = shelvedb.Storage(self.filename)
        self.db.commit()

    def test_preconditions(self):
        self.assertFalse(self.db)

    def test_set_get(self):
        self.db['foo'] = 'bar'
        self.assertEqual(self.db['foo'], 'bar')

    def test_commit(self):
        self.db['cheese'] = 'spam'

        self.db.commit()
        self.db = shelvedb.Storage(self.filename)
        # XXX: shit something not working with tempfile.
        self.assertEqual(self.db.get('cheese'), 'spam')

if __name__ == '__main__':
    unittest.main()
