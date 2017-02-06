"""
setup.py to install vsav

To create vsav distribution (.tar.gz and .zip files):
    $ python setup.py sdist --formats=gztar,zip

To install vsav:
    $ sudo python setup.py install
"""

long_description = 'vsav is hosted at https://github.com/pwexler/vsav'

from setuptools import setup

setup(
    name='vsav',
    version='1.0.0',
    description='save, restore, diff files by version',
    author='Paul Wexler',
    author_email='paul@yidnstl.com',
    packages=['vsav'],
    package_dir={'vsav': 'src'},
    entry_points={
            'console_scripts': [
                'vdif = vsav:vdif',
                'vres = vsav:vres',
                'vsav = vsav:vsav',
                ]},
    url='https://github.org/pwexler/vsav/',
    license='MIT',
    long_description=long_description,
    platforms = 'POSIX',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        ]
    )

