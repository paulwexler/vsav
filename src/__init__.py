#!/usr/bin/env python
"""
"""
import glob
import os
import sys

class VersionUtil(object):
    def diff(self, fname, *diffoptions):
        (ok, src, dst) = self.getnames(fname)
        if not ok:
            sys.stderr.write('cannot find backup version of %s\n' % dst)
            return
        if not os.access(src, os.R_OK):
            sys.stderr.write('cannot read %s\n' % src)
            return
        os.system('diff %s %s %s' % (src, dst, ' '.join(diffoptions)))

    @staticmethod
    def getnames(fname):
        """
        Returns tuple (ok, src, dst)
        """
        ok = 1
        src = fname
        flist = fname.split('.')
        if (len(flist) > 2
                and flist[-2] == 'v'
                and flist[-1].isdigit()
                and len(flist[-1]) >= 3):
            dst = '.'.join(flist[0 : -2])
        else:
            version = -1
            prefix = '%s.v.' % fname
            prefix_len = len(prefix)
            for f in glob.glob('%s*' % prefix):
                suffix = f[prefix_len:]
                if suffix.isdigit()  and  len(suffix) >= 3:
                    v = int(suffix)
                    if v > version:
                        version = v
            if version == -1:
                ok = 0
            src = '%s%03d' % (prefix, version)
            dst = fname
        return (ok, src, dst)

    def restore(self, fname):
        (ok, src, dst) = self.getnames(fname)
        if not ok:
            sys.stderr.write('cannot find backup version of %s\n' % dst)
            return
        if not os.access(src, os.R_OK):
            sys.stderr.write('cannot read %s\n' % src)
            return
        with open(src, 'r') as inf, open(dst, 'w') as ouf:
            ouf.write(inf.read())
        os.utime(dst, os.stat(src)[7:9])
        sys.stderr.write('%s restored from %s\n' % (dst, src))

    @staticmethod
    def save(fname):
        if not os.access(fname, os.R_OK):
            sys.stderr.write('cannot read %s\n' % fname)
            return
        version = -1
        prefix = '%s.v.' % fname
        prefix_len = len(prefix)
        for f in glob.glob('%s*' % prefix):
            suffix = f[prefix_len:]
            if suffix.isdigit()  and  len(suffix) >= 3:
                v = int(suffix)
                if v  > version:
                    version = v
        dst = '%s%03d' % (prefix, version + 1)
        inf = open(fname, 'r')
        ouf = open(dst, 'w')
        ouf.write(inf.read())
        ouf.close()
        inf.close()
        os.utime(dst, os.stat(fname)[7:9])
        sys.stderr.write('%s saved in %s\n' % (fname, dst))

version_util = VersionUtil()

def vdif():
    """vdif.  usage>
    Compare highest version to current version:
        vdif file [diff-option] ...

    Compare version nnn to current version:
        vdif file.v.nnn [diff-options] ...
    """
    if not sys.argv[1:]:
       sys.stderr.write(vdif.__doc__.strip() + '\n')
    else:
        fname = sys.argv[1]
        diffopts = sys.argv[2:]
        version_util.diff(fname, *diffopts)         

def vsav():
    """vsav.  usage>
    Save current version.
        vsav file ...
    """
    if not sys.argv[1:]:
       sys.stderr.write(vsav.__doc__.strip() + '\n')
    else:
        for src in sys.argv[1:]:
            version_util.save(src)

def vres():
    """vres.  usage>
    Restore current version from version nnn:
        vres file.v.nnn ...

    Restore current version from highest version:
        vres file ...
    """
    if not sys.argv[1:]:
       sys.stderr.write(vres.__doc__.strip() + '\n')
    else:
        for src in sys.argv[1:]:
            version_util.restore(src)

