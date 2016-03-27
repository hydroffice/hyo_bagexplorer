""" A setuptools based setup module.See:https://packaging.python.org/en/latest/distributing.htmlhttps://github.com/pypa/sampleproject"""from __future__ import absolute_import, division, print_function  # unicode_literalsimport osimport sys# To use a consistent encodingfrom codecs import open# Always prefer setuptools over distutilsfrom setuptools import setup, find_packages# ---------------------------------------------------------------------------#                             Some helper stuff# ---------------------------------------------------------------------------if 'bdist_wininst' in sys.argv:    if len(sys.argv) > 2 and ('sdist' in sys.argv or 'bdist_rpm' in sys.argv):        print("Error: bdist_wininst must be run alone. Exiting.")        sys.exit(1)here = os.path.abspath(os.path.dirname(__file__))def is_windows():    """ Check if the current OS is Windows """    return (sys.platform == 'win32') or (os.name is "nt")def txt_read(*paths):    """ Build a file path from *paths* and return the textual contents """    with open(os.path.join(here, *paths), encoding='utf-8') as f:        return f.read()# ---------------------------------------------------------------------------#                      Populate dictionary with settings# ---------------------------------------------------------------------------# Create a dict with the basic information that is passed to setup after keys are added.setup_args = dict()setup_args['name'] = 'hydroffice.bagexplorer'setup_args['version'] = '0.2.0'setup_args['url'] = 'https://bitbucket.org/ccomjhc/hyo_bagexplorer/'setup_args['license'] = 'LGPLv3 license'setup_args['author'] = 'Giuseppe Masetti (CCOM,UNH); Brian R. Calder (CCOM,UNH)'setup_args['author_email'] = 'gmasetti@ccom.unh.edu, brc@ccom.unh.edu'## descriptive stuff#description = 'An application to browse and manage BAG files.'setup_args['description'] = descriptionif 'bdist_wininst' in sys.argv:    setup_args['long_description'] = descriptionelse:    setup_args['long_description'] = (txt_read('README.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read('HISTORY.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read('AUTHORS.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read(os.path.join('docs', 'how_to_contribute.rst')) +                                      '\n\n\"\"\"\"\"\"\"\n\n' + txt_read(os.path.join('docs', 'banner.rst')))setup_args['classifiers'] = \    [  # https://pypi.python.org/pypi?%3Aaction=list_classifiers        'Development Status :: 4 - Beta',        'Intended Audience :: Science/Research',        'Natural Language :: English',        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',        'Operating System :: OS Independent',        'Programming Language :: Python',        'Programming Language :: Python :: 2',        'Programming Language :: Python :: 2.7',        # 'Programming Language :: Python :: 3',        # 'Programming Language :: Python :: 3.4',        # 'Programming Language :: Python :: 3.5',        'Topic :: Scientific/Engineering :: GIS',        'Topic :: Office/Business :: Office Suites',    ]setup_args['keywords'] = "hydrography ocean mapping survey bag tools"## code stuff## requirementssetup_args['setup_requires'] =\    [        "setuptools",        "wheel",    ]setup_args['install_requires'] =\    [        #"hdf_compass",        "hydroffice.bag>=0.2.5"    ]# hydroffice namespace, packages and other filessetup_args['namespace_packages'] = ['hydroffice']setup_args['packages'] = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*.test*",                                                ])setup_args['package_data'] =\    {        '': ['media/*.png', 'media/*.ico', 'media/*.icns', 'media/*.txt'],    }setup_args['data_files'] = []setup_args['entry_points'] =\    {        'gui_scripts': ['BAGExplorer = hydroffice.bagexplorer.explorer:run'],    }setup_args['test_suite'] = "tests"setup_args['options'] = \    {        "bdist_wininst":        {            "bitmap": "hydroffice/bagexplorer/media/hydroffice_wininst.bmp",        }    }# ---------------------------------------------------------------------------#                            Do the actual setup now# ---------------------------------------------------------------------------print(" >> %s" % setup_args['packages'])setup(**setup_args)