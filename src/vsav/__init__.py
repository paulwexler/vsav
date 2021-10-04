""" Save, restore, and diff versions of files.
"""
import argparse
import glob
import os
import sys

__version__ = '2.0.0'


class VersionUtil:
    """
    version suffixes: .v.nnn
    """
    @classmethod
    def diff(cls, fname, *diffoptions):
        """ diff `fname` `*diffoptions`
        """
        (aok, src, dst) = cls.get_names(fname)
        if not aok:
            sys.stderr.write(f'cannot find backup version of {dst}\n')
            return
        if not os.access(src, os.R_OK):
            sys.stderr.write(f'cannot read {src}\n')
            return
        os.system(f'diff {src} {dst} {" ".join(diffoptions)}')

    @staticmethod
    def get_highest_version(prefix):
        """
        return an int: the highest version of `prefix`
        or -1 if no version is found.
        """
        highest_version = -1
        prefix_len = len(prefix)
        for fname in glob.glob(f'{prefix}*'):
            suffix = fname[prefix_len:]
            if suffix.isdigit() and len(suffix) >= 3:
                version = int(suffix)
                highest_version = max(version, highest_version)
        return highest_version

    @classmethod
    def get_names(cls, fname):
        """
        Returns tuple (aok, src, dst)
        """
        aok = True
        src = fname
        flist = fname.split('.')
        if (len(flist) > 2
                and flist[-2] == 'v'
                and flist[-1].isdigit()
                and len(flist[-1]) >= 3):
            dst = '.'.join(flist[0 : -2])
        else:
            prefix = f'{fname}.v.'
            version = cls.get_highest_version(prefix)
            if version == -1:
                aok = False
            src = f'{prefix}{version:03d}'
            dst = fname
        return (aok, src, dst)

    @classmethod
    def restore(cls, fname):
        """
        Restore file from specific version or latest version.
        """
        (aok, src, dst) = cls.get_names(fname)
        if not aok:
            sys.stderr.write(f'cannot find backup version of {dst}\n')
            return
        if not os.access(src, os.R_OK):
            sys.stderr.write(f'cannot read {src}\n')
            return
        with open(src, 'r', encoding="utf-8") as inf:
            with open(dst, 'w', encoding="utf-8") as ouf:
                ouf.write(inf.read())
        os.utime(dst, os.stat(src)[7:9])
        sys.stderr.write(f'{dst} restored from {src}\n')

    @classmethod
    def save(cls, fname):
        """
        Save `fname` in highest version + 1.
        """
        if not os.access(fname, os.R_OK):
            sys.stderr.write(f'cannot read {fname}\n')
            return
        prefix = '%s.v.' % fname
        version = cls.get_highest_version(prefix) + 1
        dst = f'{prefix}{version:03d}'
        with open(fname, 'r', encoding="utf-8") as inf:
            with open(dst, 'w', encoding="utf-8") as ouf:
                ouf.write(inf.read())
        os.utime(dst, os.stat(fname)[7:9])
        sys.stderr.write(f'{fname} saved in {dst}\n')


def vdif():
    """vdif.  usage>
    Compare highest version or specific version to current version.
    """
    parser = argparse.ArgumentParser(description=vdif.__doc__)
    parser.add_argument(
            'fname',
            help='The file (or file.v.nnn) to compare)')
    parser.add_argument(
            'diff_option',
            nargs='*',
            help='options for diff')
    args = parser.parse_args()
    VersionUtil.diff(args.fname, *args.diff_option)

def vsav():
    """vsav.  usage>
    Save current version.
    """
    parser = argparse.ArgumentParser(description=vsav.__doc__)
    parser.add_argument(
            'fname',
            nargs='+',
            help='The file to save.')
    args = parser.parse_args()
    for fname in args.fname:
        VersionUtil.save(fname)

def vres():
    """vres.  usage>
    Restore current version from highest version or specific version.
    """
    parser = argparse.ArgumentParser(description=vres.__doc__)
    parser.add_argument(
            'fname',
            nargs='+',
            help='The file to restore.')
    args = parser.parse_args()
    for fname in args.fname:
        VersionUtil.restore(fname)
