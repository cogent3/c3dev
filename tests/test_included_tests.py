#!/usr/bin/env python
from unittest import TestCase, main


def test_no_class_before(self):
    self.assertTrue(True)


class IncludedTestsTests(TestCase):

def test_bad_first_test(self):
    self.assertTrue(True)

    def setUp(self):
        self.assertTrue(True)

    def test_normal0(self):
        self.assertTrue(True)

    def test_normal1(self):
        self.assertTrue(True)

        def test_bad_indent(self):
            self.assertTrue(True)

    def test_normal2(self):
        self.assertTrue(True)

#    def test_line_comment(self):
        self.assertTrue(True)

"""  def test_multi_comment(self): """
#        self.assertTrue(True)

"""  
    Testing multi_comment edge case 
    def test_multi_comment(self):
        self.assertTrue(True)
"""

    def est_corrupted(self):
        self.assertTrue(True)

    def test_no_self():
        # not sure how this would compile...
        self.assertTrue(True)

    def test_normal3(self):
        self.assertTrue(True)


def test_no_class_after(self):
    self.assertTrue(True)


if __name__ == '__main__':
    main()
