from __future__ import absolute_import, division, print_function, unicode_literals

import wx
import os

import logging
log = logging.getLogger(__name__)


class TextViewerFrame(wx.Frame):
    """ Text viewer. """

    icon_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media'))

    def __init__(self, data, title="Validation"):
        """ Create a new Matplotlib plotting window for a 1D line plot """
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title=title, size=(800, 400))

        # Frame icon
        ib = wx.IconBundle()
        icon_32 = wx.EmptyIcon()
        icon_32.CopyFromBitmap(wx.Bitmap(os.path.join(self.icon_folder, "favicon_32.png"), wx.BITMAP_TYPE_ANY))
        ib.AddIcon(icon_32)
        icon_48 = wx.EmptyIcon()
        icon_48.CopyFromBitmap(wx.Bitmap(os.path.join(self.icon_folder, "favicon_48.png"), wx.BITMAP_TYPE_ANY))
        ib.AddIcon(icon_48)
        self.SetIcons(ib)

        self.data = data

        self.txt = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.txt.SetValue(self.data)

        gridsizer = wx.BoxSizer(wx.VERTICAL)
        gridsizer.Add(self.txt, 1, wx.LEFT | wx.TOP | wx.GROW)

        self.view = gridsizer
