from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import os
import wx

from hyo.bagexplorer.explorer import BagExplorerApp


class TestBagExplorerApp(unittest.TestCase):

    def setUp(self):
        self.app = BagExplorerApp(False)
        self.app.MainLoop()

    def tearDown(self):
        self.app.ExitMainLoop()

    def test_is_instance(self):
        self.assertTrue(isinstance(self.app, wx.App))


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBagExplorerApp))
    return s
