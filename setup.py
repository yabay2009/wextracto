from setuptools import setup
from wex import __version__

setup(
    name='Wextracto',
    version=__version__,
    description='Web Data Extraction Library Written in Python',
    long_description='\n\n'.join([
        open('README.rst').read(),
        open('HISTORY.rst').read(),
    ]),
    author='Giles Brown',
    author_email='gsbrown@ebay.com',
    url='http://github.com/eBay/wextracto',
    license='BSD',
    include_package_data=True,
    packages=['wex'],
    package_dir={'wex': 'wex'},
    package_data={
        '': ['LICENSE.txt', 'NOTICES.txt'],
        'wex': ['logging.conf'],
    },
    zip_safe=False,
    install_requires=[
        'six',
        'requests',
        'lxml>=3',
        'cssselect',
        'publicsuffix',
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ),
    entry_points="""
        [console_scripts]
        wex = wex.command:main

        [pytest11]
        wex = wex.pytestplugin

        [wex.method.http]
        get = wex.http:request
        post = wex.http:request

        [wex.method.https]
        get = wex.http:request
        post = wex.http:request

        [wex.method.ftp]
        get = wex.ftp:get

        [wex]
        robots.txt = wex.sitemaps:urls_from_robots_txt
        sitemaps = wex.sitemaps:urls_from_sitemap
    """
)