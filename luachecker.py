#!/bin/python
# coding=utf-8

import os, os.path
from optparse import OptionParser
import subprocess
import sys


def getluaexe(path):
    exe = ''
    if path is not None:
        exe = os.path.abspath(path)
        if not os.path.exists(exe):
            exedir = os.path.dirname(os.path.abspath(__file__))
            exe = os.path.join(exedir, exe)
            if not os.path.exists(exe):
                exedir = os.path.join(exedir, 'lua')
                exe = os.path.join(exedir, path)
                if not os.path.exists(exe):
                    exe = os.path.join(exedir, path, '.exe')
                    if not os.path.exists(exe):
                        print 'can not found lua exe path: %s' % (path)
                        exit(1)
    else:
        exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lua/lua53.exe')

    return exe

def getpath():
    dir = '.'
    if len(sys.argv) == 2:
        dir = sys.argv[1]
    return os.path.abspath(dir)

def checkfile(path, luaexe, errlist):
    cmd = '"%s" "%s"' % (luaexe, path)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode
    if errcode != 0:
        errlist.append(err)


def dochecklua(luadir, luaexe, errlist):
    for root, dirs, files in os.walk(luadir):
        for f in files:
            if f.endswith('.lua'):
                checkfile(os.path.join(root, f), luaexe, errlist)

def docheckerr(errlist, luaexe, rootpath, verbose):
    if len(errlist) > 0:
        exelen = len(luaexe) + 2
        if len(rootpath) > 0:
            rootpath = rootpath + os.sep
        for err in errlist:
            err = err[exelen:]
            err = err.replace(rootpath, "")
            if not verbose:
                err = err[0:err.find('\n')]
            print err.strip()



# -------------- main --------------
if __name__ == '__main__':
    usage = "usage: %prog [options] [path]"
    parser = OptionParser(usage=usage)
    parser.add_option(
        '-v', '--verbose', dest='verbose', action='store_true', default=False,
        help='show verbose information')
    parser.add_option(
        '--lua', dest='lua',
        help='lua exe file path')
    (opts, args) = parser.parse_args()
    if len(args) > 1 :
        parser.error("")

    path = args[0] if len(args) == 1 else '.'
    path = os.path.abspath(path)

    luaexe = getluaexe(opts.lua)

    errlist = []
    dochecklua(path, luaexe, errlist)
    docheckerr(errlist, luaexe, os.path.abspath('.'), opts.verbose)

