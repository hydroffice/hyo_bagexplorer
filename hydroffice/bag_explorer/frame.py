from __future__ import absolute_import, division, print_function, unicode_literals

import os

import wx

import logging
log = logging.getLogger(__name__)

from hdf_compass import utils
from hdf_compass.compass_viewer import frame
from hdf_compass import compass_model

from hydroffice.bag import BAGFile, __version__ as bag_version
from hydroffice.bag.bbox import Bbox2Gdal
from hydroffice.bag.elevation import Elevation2Gdal
from hydroffice.bag.uncertainty import Uncertainty2Gdal
from hydroffice.bag.tracklist import TrackList2Csv

ID_ABOUT_BAG_TOOLS = wx.NewId()
ID_MANUAL_BAG_TOOLS = wx.NewId()
ID_ABOUT_HDF_COMPASS = wx.NewId()
ID_OPEN_SAMPLES = wx.NewId()

ID_TOOLS_BBOX_GJS = wx.NewId()
ID_TOOLS_BBOX_GML = wx.NewId()
ID_TOOLS_BBOX_KML = wx.NewId()
ID_TOOLS_BBOX_SHP = wx.NewId()

ID_TOOLS_UNC_ASC = wx.NewId()
ID_TOOLS_UNC_GTF = wx.NewId()
ID_TOOLS_UNC_XYZ = wx.NewId()

ID_TOOLS_ELV_ASC = wx.NewId()
ID_TOOLS_ELV_GTF = wx.NewId()
ID_TOOLS_ELV_XYZ = wx.NewId()

ID_TOOLS_TKL_CSV = wx.NewId()

ID_TOOLS_META_VAL = wx.NewId()
ID_TOOLS_META_XML = wx.NewId()

frame.BaseFrame.icon_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media'))


class InitFrame(frame.InitFrame):
    """ Frame displayed when the application starts up. """

    icon_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media'))

    def __init__(self):
        super(InitFrame, self).__init__()
        self.SetTitle("BAG Explorer")

        for m in self.GetMenuBar().GetMenus():
            if m[1] == '&File':
                m[0].Insert(2, ID_OPEN_SAMPLES, "Open &Samples\tCtrl-S", "Open data samples")
            if m[1] == '&Help':
                about_id = m[0].FindItem("&About HDFCompass")
                about_item = m[0].FindItemById(about_id)
                about_item.SetText("About BAG Explorer")
                m[0].RemoveItem(about_item)
                m[0].Append(ID_ABOUT_HDF_COMPASS, "&About HDF Compass", "Information about HDF Compass")
                m[0].AppendSeparator()
                m[0].Append(ID_MANUAL_BAG_TOOLS, "Online Manual", "Open the online documentation for BAG Tools")
                m[0].Append(ID_ABOUT_BAG_TOOLS, "&About BAG Tools", "Information about the BAG Tools")
                m[0].AppendSeparator()
                m[0].AppendItem(about_item)

        # Tools menu
        fm = wx.Menu()
        # Bbox
        bm = wx.Menu()
        bm.Append(ID_TOOLS_BBOX_GJS, "Export as GeoJSON", "Export bounding box and metadata as GeoJSON")
        bm.Append(ID_TOOLS_BBOX_GML, "Export as GML", "Export bounding box and metadata as GML")
        bm.Append(ID_TOOLS_BBOX_KML, "Export as KML", "Export bounding box and metadata as KML")
        bm.Append(ID_TOOLS_BBOX_SHP, "Export as Shapefile", "Export bounding box and metadata as Shapefile")
        fm.AppendMenu(wx.ID_ANY, "Bounding Box", bm)
        # Elevation
        em = wx.Menu()
        em.Append(ID_TOOLS_ELV_ASC, "Export as ASCII Grid", "Export Elevation layer as ASCII Grid")
        em.Append(ID_TOOLS_ELV_GTF, "Export as GeoTiff", "Export Elevation layer as ASCII Grid")
        em.Append(ID_TOOLS_ELV_XYZ, "Export as XYZ", "Export Elevation layer as XYZ")
        fm.AppendMenu(wx.ID_ANY, "Elevation", em)
        # Uncertainty
        um = wx.Menu()
        um.Append(ID_TOOLS_UNC_ASC, "Export as ASCII Grid", "Export Uncertainty layer as ASCII Grid")
        um.Append(ID_TOOLS_UNC_GTF, "Export as GeoTiff", "Export Uncertainty layer as ASCII Grid")
        um.Append(ID_TOOLS_UNC_XYZ, "Export as XYZ", "Export Uncertainty layer as XYZ")
        fm.AppendMenu(wx.ID_ANY, "Uncertainty", um)
        # Tracking list
        tm = wx.Menu()
        tm.Append(ID_TOOLS_TKL_CSV, "Export as CSV", "Export Tracking List as Comma Separated Values")
        fm.AppendMenu(wx.ID_ANY, "Tracking List", tm)
        # Metadata
        mm = wx.Menu()
        mm.Append(ID_TOOLS_META_VAL, "Validate", "Validate BAG Metadata")
        mm.Append(ID_TOOLS_META_XML, "Export as Xml", "Export as XML file")
        fm.AppendMenu(wx.ID_ANY, "Metadata", mm)
        self.GetMenuBar().Insert(1, fm, "BAG &Tools")

        self.Bind(wx.EVT_MENU, self.on_open_samples, id=ID_OPEN_SAMPLES)
        self.Bind(wx.EVT_MENU, self.on_about_bag_explorer, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.on_about_hdf_compass, id=ID_ABOUT_HDF_COMPASS)
        self.Bind(wx.EVT_MENU, self.on_manual_bag_tools, id=ID_MANUAL_BAG_TOOLS)
        self.Bind(wx.EVT_MENU, self.on_about_bag_tools, id=ID_ABOUT_BAG_TOOLS)

        # BAG tools
        self.Bind(wx.EVT_MENU, self.on_bbox_geojson, id=ID_TOOLS_BBOX_GJS)
        self.Bind(wx.EVT_MENU, self.on_bbox_gml, id=ID_TOOLS_BBOX_GML)
        self.Bind(wx.EVT_MENU, self.on_bbox_kml, id=ID_TOOLS_BBOX_KML)
        self.Bind(wx.EVT_MENU, self.on_bbox_shapefile, id=ID_TOOLS_BBOX_SHP)

        self.Bind(wx.EVT_MENU, self.on_elevation_ascii, id=ID_TOOLS_ELV_ASC)
        self.Bind(wx.EVT_MENU, self.on_elevation_geotiff, id=ID_TOOLS_ELV_GTF)
        self.Bind(wx.EVT_MENU, self.on_elevation_xyz, id=ID_TOOLS_ELV_XYZ)

        self.Bind(wx.EVT_MENU, self.on_uncertainty_ascii, id=ID_TOOLS_UNC_ASC)
        self.Bind(wx.EVT_MENU, self.on_uncertainty_geotiff, id=ID_TOOLS_UNC_GTF)
        self.Bind(wx.EVT_MENU, self.on_uncertainty_xyz, id=ID_TOOLS_UNC_XYZ)

        self.Bind(wx.EVT_MENU, self.on_tracklist_csv, id=ID_TOOLS_TKL_CSV)

        self.Bind(wx.EVT_MENU, self.on_meta_validate, id=ID_TOOLS_META_VAL)
        self.Bind(wx.EVT_MENU, self.on_meta_xml, id=ID_TOOLS_META_XML)

    def on_manual_bag_tools(self, evt):
        """ Open the url with the online documentation for BAG Tools """
        import webbrowser
        webbrowser.open('http://giumas.github.io/hyo_bag/stable/index.html')

    def on_about_bag_explorer(self, evt):
        """ Display an "About BAG Explorer" dialog """
        from . import __version__

        info = wx.AboutDialogInfo()
        info.Name = "BAG Explorer"
        info.Description = """
An application to browse and interact with Bathymetric Attributed Grid (BAG) files.
The application is based on HDF Compass and HydrOffice BAG Tools.

Developed by G.Masetti and B.R.Calder at the Center for Coastal and Ocean Mapping /
Joint Hydrographic Center (CCOM/JHC).
"""
        info.Version = __version__
        info.License = """
Copyright (c) 2015, University of New Hampshire
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list
of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or other
materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may
be used to endorse or promote products derived from this software without specific
prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
        """
        info.Copyright = "(c) 2015 University of New Hampshire"
        info.SetIcon(wx.Icon(os.path.join(self.icon_folder, 'BAGExplorer_128.png')))
        info.SetWebSite("http://ccom.unh.edu/hydroffice")
        wx.AboutBox(info)

    def on_about_hdf_compass(self, evt):
        """ Display an "About HDF_Compass" dialog """
        from datetime import date
        from hdf_compass.utils import __version__

        info = wx.AboutDialogInfo()
        info.Name = "HDF Compass"
        info.Version = __version__
        info.Copyright = "(c) 2014-%d The HDF Group" % date.today().year
        info.SetIcon(wx.Icon(os.path.join(self.icon_folder, "favicon_48.png")))
        info.SetWebSite("https://www.hdfgroup.org/projects/compass/")
        wx.AboutBox(info)

    def on_about_bag_tools(self, evt):
        """ Display an "About BAG Tools" dialog """
        info = wx.AboutDialogInfo()
        info.Name = "HydrOffice BAG Tools"
        info.Version = bag_version
        info.Copyright = "(c) 2015 G.Masetti, B.R.Calder"
        info.SetIcon(wx.Icon(os.path.join(self.icon_folder, 'BAG_48.png')))
        info.SetWebSite("https://bitbucket.org/gmasetti/hyo_bag")
        wx.AboutBox(info)

    def on_file_open(self, evt):
        """ Request to open a file via the Open entry in the File menu """

        def make_filter_string():
            """ Make a wxPython dialog filter string segment from dict """
            filter_string = []
            hdf_filter_string = []  # put HDF filters in the front
            for store in compass_model.get_stores():
                if len(store.file_extensions) == 0:
                    continue
                for key in store.file_extensions:
                    s = "{name} ({pattern_c})|{pattern_sc}".format(
                        name=key,
                        pattern_c=",".join(store.file_extensions[key]),
                        pattern_sc=";".join(store.file_extensions[key]) )
                    if s.startswith("BAG"):
                        hdf_filter_string.append(s)
                    else:
                        filter_string.append(s)
            filter_string = hdf_filter_string + filter_string
            filter_string.append('All Files (*.*)|*.*')
            pipe = "|"
            return pipe.join(filter_string)

        wc_string = make_filter_string()

        dlg = wx.FileDialog(self, "Open Local File", wildcard=wc_string, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() != wx.ID_OK:
            return
        path = dlg.GetPath()

        url = utils.path2url(path)
        self.open_url(url)

    def on_open_samples(self, evt):
        """ Request to open a file via the Open entry in the File menu """
        def make_filter_string():
            """ Make a wxPython dialog filter string segment from dict """
            filter_string = []
            hdf_filter_string = []  # put HDF filters in the front
            for store in compass_model.get_stores():
                if len(store.file_extensions) == 0:
                    continue
                for key in store.file_extensions:
                    s = "{name} ({pattern_c})|{pattern_sc}".format(
                        name=key,
                        pattern_c=",".join(store.file_extensions[key]),
                        pattern_sc=";".join(store.file_extensions[key]) )
                    if s.startswith("BAG"):
                        hdf_filter_string.append(s)
                    else:
                        filter_string.append(s)
            filter_string = hdf_filter_string + filter_string
            filter_string.append('All Files (*.*)|*.*')
            pipe = "|"
            return pipe.join(filter_string)

        wc_string = make_filter_string()

        samples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "bag", "samples"))
        if os.path.exists(samples_dir):
            log.debug("samples folder: %s" % samples_dir)
        else:
            log.warning("missing samples folder: %s" % samples_dir)
        dlg = wx.FileDialog(self, "Open Samples Folder", defaultDir=samples_dir, wildcard=wc_string,
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() != wx.ID_OK:
            return
        path = dlg.GetPath()

        url = utils.path2url(path)
        self.open_url(url)

    # BAG Tools

    # BAG Bbox

    bbox_formats = {
        "gml": ("gml", "GML"),
        "gjs": ("geojson", "GeoJSON"),
        "kml": ("kml", "KML"),
        "shp": ("shp", "Shapefile")
    }

    def on_bbox_geojson(self, evt):
        """ Export the bounding box and some metadata to a geojson file """
        self._bbox_export("gjs")

    def on_bbox_gml(self, evt):
        """ Export the bounding box and some metadata to a GML file """
        self._bbox_export("gml")

    def on_bbox_kml(self, evt):
        """ Export the bounding box and some metadata to a KML file """
        self._bbox_export("kml")

    def on_bbox_shapefile(self, evt):
        """ Export the bounding box and some metadata to a Shapefile file """
        self._bbox_export("shp")

    def _bbox_export(self, fmt='kml'):
        """ Helper function to be re-used for different output formats """
        bag_file = self._ask_bag_input()
        fmt_name = self.bbox_formats[fmt][1]
        fmt_ext = self.bbox_formats[fmt][0]
        out_file = self._ask_file_output(fmt_name=fmt_name, fmt_ext=fmt_ext)

        try:
            bag = BAGFile(bag_file)
            bag_meta = bag.populate_metadata()
            Bbox2Gdal(bag_meta, fmt=fmt, title=os.path.basename(bag_file), out_file=out_file)
        except Exception as e:
            dlg = wx.MessageDialog(parent=None, message="%s" % e, caption="Error", style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self._check_file_creation(out_file)

    # BAG Elevation

    _elevation_formats = {
        "ascii": ("asc", "ASCII Grid"),
        "geotiff": ("tif", "GeoTIFF"),
        "xyz": ("xyz", "XYZ")
    }

    def on_elevation_ascii(self, evt):
        """ Export the elevation layer to an ASCII Grid """
        self._elevation_export("ascii")

    def on_elevation_geotiff(self, evt):
        """ Export the elevation to a GeoTIFF file """
        self._elevation_export("geotiff")

    def on_elevation_xyz(self, evt):
        """ Export the elevation to an XYZ file """
        self._elevation_export("xyz")

    def _elevation_export(self, fmt='geotiff'):
        """ Helper function to be re-used for different output formats """
        bag_file = self._ask_bag_input()
        fmt_name = self._elevation_formats[fmt][1]
        fmt_ext = self._elevation_formats[fmt][0]
        out_file = self._ask_file_output(fmt_name=fmt_name, fmt_ext=fmt_ext)

        try:
            bag = BAGFile(bag_file)
            bag_meta = bag.populate_metadata()
            bag_elv = bag.elevation(mask_nan=False)
            Elevation2Gdal(bag_elevation=bag_elv, bag_meta=bag_meta, fmt=fmt, out_file=out_file)
        except Exception as e:
            dlg = wx.MessageDialog(parent=None, message="%s" % e, caption="Error", style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self._check_file_creation(out_file)

    # BAG Uncertainty

    _uncertainty_formats = {
        "ascii": ("asc", "ASCII Grid"),
        "geotiff": ("tif", "GeoTIFF"),
        "xyz": ("xyz", "XYZ")
    }

    def on_uncertainty_ascii(self, evt):
        """ Export the uncertainty layer to an ASCII Grid """
        self._uncertainty_export("ascii")

    def on_uncertainty_geotiff(self, evt):
        """ Export the uncertainty to a GeoTIFF file """
        self._uncertainty_export("geotiff")

    def on_uncertainty_xyz(self, evt):
        """ Export the uncertainty to an XYZ file """
        self._uncertainty_export("xyz")

    def _uncertainty_export(self, fmt='geotiff'):
        """ Helper function to be re-used for different output formats """
        bag_file = self._ask_bag_input()
        fmt_name = self._uncertainty_formats[fmt][1]
        fmt_ext = self._uncertainty_formats[fmt][0]
        out_file = self._ask_file_output(fmt_name=fmt_name, fmt_ext=fmt_ext)

        try:
            bag = BAGFile(bag_file)
            bag_meta = bag.populate_metadata()
            bag_unc = bag.uncertainty(mask_nan=False)
            Uncertainty2Gdal(bag_uncertainty=bag_unc, bag_meta=bag_meta, fmt=fmt, out_file=out_file)
        except Exception as e:
            dlg = wx.MessageDialog(parent=None, message="%s" % e, caption="Error", style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self._check_file_creation(out_file)

    # BAG Tracking List

    _tracklist_formats = {
        "csv": ("csv", "Comma Separated Values"),
    }

    def on_tracklist_csv(self, evt):
        """ Export the tracking list as Comma Separated Values """
        self._tracklist_export("csv")

    def _tracklist_export(self, fmt='csv'):
        """ Helper function to be re-used for different output formats """
        bag_file = self._ask_bag_input()
        fmt_name = self._tracklist_formats[fmt][1]
        fmt_ext = self._tracklist_formats[fmt][0]
        out_file = self._ask_file_output(fmt_name=fmt_name, fmt_ext=fmt_ext)

        try:
            bag = BAGFile(bag_file)
            bag_tkl = bag.tracking_list()
            if bag_tkl.size == 0:
                dlg = wx.MessageDialog(parent=None, message="Nothing to export! The Tracking List is empty.",
                                       caption="Information", style=wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                return

            bag_tkl_fields = bag.tracking_list_fields()
            TrackList2Csv(track_list=bag_tkl, header=bag_tkl_fields, csv_file=out_file)
        except Exception as e:
            dlg = wx.MessageDialog(parent=None, message="%s" % e, caption="Error", style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self._check_file_creation(out_file)

    # BAG Metadata

    _metadata_formats = {
        "xml": ("xml", "XML"),
    }

    def on_meta_xml(self, evt):
        """ Export the metadata as XML """
        self._metadata_export("xml")

    def _metadata_export(self, fmt='xml'):
        """ Helper function to be re-used for different output formats """
        bag_file = self._ask_bag_input()
        fmt_name = self._metadata_formats[fmt][1]
        fmt_ext = self._metadata_formats[fmt][0]
        out_file = self._ask_file_output(fmt_name=fmt_name, fmt_ext=fmt_ext)

        try:
            bag = BAGFile(bag_file)
            bag.extract_metadata(name=out_file)
        except Exception as e:
            dlg = wx.MessageDialog(parent=None, message="%s" % e, caption="Error", style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self._check_file_creation(out_file)

    def on_meta_validate(self, evt):
        """ Validate the metadata as XML """
        from .text_ctrl import TextViewerFrame
        bag_file = self._ask_bag_input()
        bag = BAGFile(bag_file)
        val_info = bag.validation_info()
        txt_frame = TextViewerFrame(data=val_info)
        txt_frame.Show()

    # BAG Tools helpers

    def _ask_bag_input(self):
        """ Open a file dialog to make the user to select the input BAG file """
        dlg = wx.FileDialog(self, "Select input BAG File", wildcard='BAG Files (*.bag)|*.bag|All Files (*.*)|*.*',
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() != wx.ID_OK:
            return
        bag_file = dlg.GetPath()
        log.debug("input: %s" % bag_file)
        return bag_file

    def _ask_file_output(self, fmt_name, fmt_ext):
        """ Open a file dialog to make the user to select the output filename """
        log.debug("format: %s [.%s]" % (fmt_name, fmt_ext))
        dlg = wx.FileDialog(self, "Select output %s File" % fmt_name,
                            wildcard='%s Files (*.%s)|*.%s|All Files (*.*)|*.*' % (fmt_name, fmt_ext, fmt_ext),
                            style=wx.FD_SAVE)
        if dlg.ShowModal() != wx.ID_OK:
            return
        out_file = dlg.GetPath()
        log.debug("output: %s" % out_file)
        return out_file

    @classmethod
    def _check_file_creation(cls, out_file):
        """ check file creation """
        if os.path.exists(out_file):
            dlg = wx.MessageDialog(parent=None, message="File created: %s" % out_file,
                                   caption="Information", style=wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dlg = wx.MessageDialog(parent=None, message="Unable to export as %s" % out_file,
                                   caption="Error", style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
