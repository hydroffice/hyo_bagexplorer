# Builds a single-file EXE for distribution.
# Note that an "unbundled" distribution launches much more quickly, but
# requires an installer program to distribute.
#
# To compile, execute the following within the source directory:
#
# python /path/to/pyinstaller.py freeze/BAGExplorer.1file.spec
#
# The resulting .exe file is placed in the dist/ folder.

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, BUNDLE, TOC
from PyInstaller import is_darwin
import os


def collect_pkg_data(package, include_py_files=False, subdir=None):
    """ helper function to collect data based on the passed package """
    from PyInstaller.utils.hooks import get_package_paths, remove_prefix, PY_IGNORE_EXTENSIONS

    # Accept only strings as packages.
    if type(package) is not str:
        raise ValueError

    pkg_base, pkg_dir = get_package_paths(package)
    if subdir:
        pkg_dir = os.path.join(pkg_dir, subdir)
    # Walk through all file in the given package, looking for data files.
    data_toc = TOC()
    for dir_path, dir_names, files in os.walk(pkg_dir):
        for f in files:
            extension = os.path.splitext(f)[1]
            if include_py_files or (extension not in PY_IGNORE_EXTENSIONS):
                source_file = os.path.join(dir_path, f)
                dest_folder = remove_prefix(dir_path, os.path.dirname(pkg_base) + os.sep)
                dest_file = os.path.join(dest_folder, f)
                data_toc.append((dest_file, source_file, 'DATA'))

    return data_toc

pkg_data_bag = collect_pkg_data('hydroffice.bag')
pkg_data_bagexplorer = collect_pkg_data('hydroffice.bagexplorer')
pkg_data_hdf_compass = collect_pkg_data('hdf_compass')
pkg_data_lxml = collect_pkg_data('lxml')
cartopy_aux = collect_pkg_data('cartopy')

icon_folder = os.path.abspath(os.path.join('hydroffice', 'bagexplorer', 'media'))
if not os.path.exists(icon_folder):
    raise RuntimeError("invalid path to icon folder: %s" % icon_folder)
icon_file = os.path.join(icon_folder, 'BAGExplorer.ico')
if is_darwin:
    icon_file = os.path.join(icon_folder, 'BAGExplorer.icns')

app_name = 'BAGExplorer'
    
a = Analysis(['BAGExplorer.py'],
             pathex=[],
             hiddenimports=['scipy.integrate'],
             excludes=["PySide", "PyQt4", "pandas", "IPython"],
             hookspath=None,
             runtime_hooks=None)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          pkg_data_bag,
          pkg_data_bagexplorer,
          pkg_data_hdf_compass,
          pkg_data_lxml,
          cartopy_aux,
          name=app_name,
          debug=False,
          strip=None,
          upx=False,
          console=True,
          icon=icon_file)
if is_darwin:
    app = BUNDLE(exe,
                 name='BAGExplorer.app',
                 icon=icon_file,
                 bundle_identifier=None)
