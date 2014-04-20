from os.path import basename
from distutils.core import setup

import py2exe

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
    if basename(pathname).lower() in ("libogg-0.dll", "sdl_ttf.dll"):
        return 0
    return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

setup(windows=[{"script": "game.py"}],
      options={"py2exe": {"dist_dir": "dist"}})