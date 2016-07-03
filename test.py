import unittest

from travispy import TravisPy
from travispy.errors import TravisError


class MyTest(unittest.TestCase):
    def test(self):
      with self.assertRaises(TravisError):
        travis = TravisPy(token='invalid_token')
        travis.repo('some_repo')