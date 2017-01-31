'''Wrapper for lcms2.h

Generated with:
../ctypesgen/ctypesgen.py -llcms2 /usr/include/lcms2.h /usr/include/lcms2_plugin.h -o lcms2.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from c_char array
        elif isinstance(obj, c_char*len(obj)):
            return obj

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes,errcheck):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
        if errcheck:
          self.func.errcheck = errcheck
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import platform
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # FIXME / TODO return '.' and os.path.dirname(__file__)
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")
        dirs.append(os.path.dirname(__file__))

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")
        directories.append(os.path.dirname(__file__))

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        unix_lib_dirs_list = ['/lib', '/usr/lib', '/lib64', '/usr/lib64']
        if sys.platform.startswith('linux'):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            bitage = platform.architecture()[0]
            if bitage.startswith('32'):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ['/lib/i386-linux-gnu', '/usr/lib/i386-linux-gnu']
            elif bitage.startswith('64'):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ['/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu']
            else:
                # guess...
                unix_lib_dirs_list += glob.glob('/lib/*linux-gnu')
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    """
    Add libraries to search paths.
    If library paths are relative, convert them to absolute with respect to this
    file's directory
    """
    THIS_DIR = os.path.dirname(__file__)
    for F in other_dirs:
        if not os.path.isabs(F):
            F = os.path.abspath(os.path.join(THIS_DIR,F))
        loader.other_dirs.append(F)

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["lcms2"] = load_library("lcms2")

# 1 libraries
# End libraries

# No modules

__off_t = c_long # /usr/include/x86_64-linux-gnu/bits/types.h: 131

__off64_t = c_long # /usr/include/x86_64-linux-gnu/bits/types.h: 132

# /usr/include/libio.h: 241
class struct__IO_FILE(Structure):
    pass

FILE = struct__IO_FILE # /usr/include/stdio.h: 48

_IO_lock_t = None # /usr/include/libio.h: 150

# /usr/include/libio.h: 156
class struct__IO_marker(Structure):
    pass

struct__IO_marker.__slots__ = [
    '_next',
    '_sbuf',
    '_pos',
]
struct__IO_marker._fields_ = [
    ('_next', POINTER(struct__IO_marker)),
    ('_sbuf', POINTER(struct__IO_FILE)),
    ('_pos', c_int),
]

struct__IO_FILE.__slots__ = [
    '_flags',
    '_IO_read_ptr',
    '_IO_read_end',
    '_IO_read_base',
    '_IO_write_base',
    '_IO_write_ptr',
    '_IO_write_end',
    '_IO_buf_base',
    '_IO_buf_end',
    '_IO_save_base',
    '_IO_backup_base',
    '_IO_save_end',
    '_markers',
    '_chain',
    '_fileno',
    '_flags2',
    '_old_offset',
    '_cur_column',
    '_vtable_offset',
    '_shortbuf',
    '_lock',
    '_offset',
    '__pad1',
    '__pad2',
    '__pad3',
    '__pad4',
    '__pad5',
    '_mode',
    '_unused2',
]
struct__IO_FILE._fields_ = [
    ('_flags', c_int),
    ('_IO_read_ptr', String),
    ('_IO_read_end', String),
    ('_IO_read_base', String),
    ('_IO_write_base', String),
    ('_IO_write_ptr', String),
    ('_IO_write_end', String),
    ('_IO_buf_base', String),
    ('_IO_buf_end', String),
    ('_IO_save_base', String),
    ('_IO_backup_base', String),
    ('_IO_save_end', String),
    ('_markers', POINTER(struct__IO_marker)),
    ('_chain', POINTER(struct__IO_FILE)),
    ('_fileno', c_int),
    ('_flags2', c_int),
    ('_old_offset', __off_t),
    ('_cur_column', c_ushort),
    ('_vtable_offset', c_char),
    ('_shortbuf', c_char * 1),
    ('_lock', POINTER(_IO_lock_t)),
    ('_offset', __off64_t),
    ('__pad1', POINTER(None)),
    ('__pad2', POINTER(None)),
    ('__pad3', POINTER(None)),
    ('__pad4', POINTER(None)),
    ('__pad5', c_size_t),
    ('_mode', c_int),
    ('_unused2', c_char * (((15 * sizeof(c_int)) - (4 * sizeof(POINTER(None)))) - sizeof(c_size_t))),
]

# /usr/include/time.h: 133
class struct_tm(Structure):
    pass

struct_tm.__slots__ = [
    'tm_sec',
    'tm_min',
    'tm_hour',
    'tm_mday',
    'tm_mon',
    'tm_year',
    'tm_wday',
    'tm_yday',
    'tm_isdst',
    'tm_gmtoff',
    'tm_zone',
]
struct_tm._fields_ = [
    ('tm_sec', c_int),
    ('tm_min', c_int),
    ('tm_hour', c_int),
    ('tm_mday', c_int),
    ('tm_mon', c_int),
    ('tm_year', c_int),
    ('tm_wday', c_int),
    ('tm_yday', c_int),
    ('tm_isdst', c_int),
    ('tm_gmtoff', c_long),
    ('tm_zone', String),
]

cmsUInt8Number = c_ubyte # /usr/include/lcms2.h: 84

cmsInt8Number = c_char # /usr/include/lcms2.h: 85

cmsFloat32Number = c_float # /usr/include/lcms2.h: 92

cmsFloat64Number = c_double # /usr/include/lcms2.h: 93

cmsUInt16Number = c_ushort # /usr/include/lcms2.h: 97

cmsInt16Number = c_short # /usr/include/lcms2.h: 105

cmsUInt32Number = c_uint # /usr/include/lcms2.h: 114

cmsInt32Number = c_int # /usr/include/lcms2.h: 122

cmsUInt64Number = c_ulong # /usr/include/lcms2.h: 132

cmsInt64Number = c_long # /usr/include/lcms2.h: 139

cmsSignature = cmsUInt32Number # /usr/include/lcms2.h: 155

cmsU8Fixed8Number = cmsUInt16Number # /usr/include/lcms2.h: 156

cmsS15Fixed16Number = cmsInt32Number # /usr/include/lcms2.h: 157

cmsU16Fixed16Number = cmsUInt32Number # /usr/include/lcms2.h: 158

cmsBool = c_int # /usr/include/lcms2.h: 161

enum_anon_7 = c_int # /usr/include/lcms2.h: 312

cmsSigChromaticityType = 1667789421 # /usr/include/lcms2.h: 312

cmsSigColorantOrderType = 1668051567 # /usr/include/lcms2.h: 312

cmsSigColorantTableType = 1668051572 # /usr/include/lcms2.h: 312

cmsSigCrdInfoType = 1668441193 # /usr/include/lcms2.h: 312

cmsSigCurveType = 1668641398 # /usr/include/lcms2.h: 312

cmsSigDataType = 1684108385 # /usr/include/lcms2.h: 312

cmsSigDictType = 1684628340 # /usr/include/lcms2.h: 312

cmsSigDateTimeType = 1685350765 # /usr/include/lcms2.h: 312

cmsSigDeviceSettingsType = 1684371059 # /usr/include/lcms2.h: 312

cmsSigLut16Type = 1835430962 # /usr/include/lcms2.h: 312

cmsSigLut8Type = 1835430961 # /usr/include/lcms2.h: 312

cmsSigLutAtoBType = 1832993312 # /usr/include/lcms2.h: 312

cmsSigLutBtoAType = 1833058592 # /usr/include/lcms2.h: 312

cmsSigMeasurementType = 1835360627 # /usr/include/lcms2.h: 312

cmsSigMultiLocalizedUnicodeType = 1835824483 # /usr/include/lcms2.h: 312

cmsSigMultiProcessElementType = 1836082548 # /usr/include/lcms2.h: 312

cmsSigNamedColorType = 1852010348 # /usr/include/lcms2.h: 312

cmsSigNamedColor2Type = 1852009522 # /usr/include/lcms2.h: 312

cmsSigParametricCurveType = 1885434465 # /usr/include/lcms2.h: 312

cmsSigProfileSequenceDescType = 1886610801 # /usr/include/lcms2.h: 312

cmsSigProfileSequenceIdType = 1886611812 # /usr/include/lcms2.h: 312

cmsSigResponseCurveSet16Type = 1919120178 # /usr/include/lcms2.h: 312

cmsSigS15Fixed16ArrayType = 1936077618 # /usr/include/lcms2.h: 312

cmsSigScreeningType = 1935897198 # /usr/include/lcms2.h: 312

cmsSigSignatureType = 1936287520 # /usr/include/lcms2.h: 312

cmsSigTextType = 1952807028 # /usr/include/lcms2.h: 312

cmsSigTextDescriptionType = 1684370275 # /usr/include/lcms2.h: 312

cmsSigU16Fixed16ArrayType = 1969632050 # /usr/include/lcms2.h: 312

cmsSigUcrBgType = 1650877472 # /usr/include/lcms2.h: 312

cmsSigUInt16ArrayType = 1969828150 # /usr/include/lcms2.h: 312

cmsSigUInt32ArrayType = 1969828658 # /usr/include/lcms2.h: 312

cmsSigUInt64ArrayType = 1969829428 # /usr/include/lcms2.h: 312

cmsSigUInt8ArrayType = 1969827896 # /usr/include/lcms2.h: 312

cmsSigVcgtType = 1986226036 # /usr/include/lcms2.h: 312

cmsSigViewingConditionsType = 1986618743 # /usr/include/lcms2.h: 312

cmsSigXYZType = 1482250784 # /usr/include/lcms2.h: 312

cmsTagTypeSignature = enum_anon_7 # /usr/include/lcms2.h: 312

enum_anon_8 = c_int # /usr/include/lcms2.h: 388

cmsSigAToB0Tag = 1093812784 # /usr/include/lcms2.h: 388

cmsSigAToB1Tag = 1093812785 # /usr/include/lcms2.h: 388

cmsSigAToB2Tag = 1093812786 # /usr/include/lcms2.h: 388

cmsSigBlueColorantTag = 1649957210 # /usr/include/lcms2.h: 388

cmsSigBlueMatrixColumnTag = 1649957210 # /usr/include/lcms2.h: 388

cmsSigBlueTRCTag = 1649693251 # /usr/include/lcms2.h: 388

cmsSigBToA0Tag = 1110589744 # /usr/include/lcms2.h: 388

cmsSigBToA1Tag = 1110589745 # /usr/include/lcms2.h: 388

cmsSigBToA2Tag = 1110589746 # /usr/include/lcms2.h: 388

cmsSigCalibrationDateTimeTag = 1667329140 # /usr/include/lcms2.h: 388

cmsSigCharTargetTag = 1952543335 # /usr/include/lcms2.h: 388

cmsSigChromaticAdaptationTag = 1667785060 # /usr/include/lcms2.h: 388

cmsSigChromaticityTag = 1667789421 # /usr/include/lcms2.h: 388

cmsSigColorantOrderTag = 1668051567 # /usr/include/lcms2.h: 388

cmsSigColorantTableTag = 1668051572 # /usr/include/lcms2.h: 388

cmsSigColorantTableOutTag = 1668050804 # /usr/include/lcms2.h: 388

cmsSigColorimetricIntentImageStateTag = 1667852659 # /usr/include/lcms2.h: 388

cmsSigCopyrightTag = 1668313716 # /usr/include/lcms2.h: 388

cmsSigCrdInfoTag = 1668441193 # /usr/include/lcms2.h: 388

cmsSigDataTag = 1684108385 # /usr/include/lcms2.h: 388

cmsSigDateTimeTag = 1685350765 # /usr/include/lcms2.h: 388

cmsSigDeviceMfgDescTag = 1684893284 # /usr/include/lcms2.h: 388

cmsSigDeviceModelDescTag = 1684890724 # /usr/include/lcms2.h: 388

cmsSigDeviceSettingsTag = 1684371059 # /usr/include/lcms2.h: 388

cmsSigDToB0Tag = 1144144432 # /usr/include/lcms2.h: 388

cmsSigDToB1Tag = 1144144433 # /usr/include/lcms2.h: 388

cmsSigDToB2Tag = 1144144434 # /usr/include/lcms2.h: 388

cmsSigDToB3Tag = 1144144435 # /usr/include/lcms2.h: 388

cmsSigBToD0Tag = 1110590512 # /usr/include/lcms2.h: 388

cmsSigBToD1Tag = 1110590513 # /usr/include/lcms2.h: 388

cmsSigBToD2Tag = 1110590514 # /usr/include/lcms2.h: 388

cmsSigBToD3Tag = 1110590515 # /usr/include/lcms2.h: 388

cmsSigGamutTag = 1734438260 # /usr/include/lcms2.h: 388

cmsSigGrayTRCTag = 1800688195 # /usr/include/lcms2.h: 388

cmsSigGreenColorantTag = 1733843290 # /usr/include/lcms2.h: 388

cmsSigGreenMatrixColumnTag = 1733843290 # /usr/include/lcms2.h: 388

cmsSigGreenTRCTag = 1733579331 # /usr/include/lcms2.h: 388

cmsSigLuminanceTag = 1819635049 # /usr/include/lcms2.h: 388

cmsSigMeasurementTag = 1835360627 # /usr/include/lcms2.h: 388

cmsSigMediaBlackPointTag = 1651208308 # /usr/include/lcms2.h: 388

cmsSigMediaWhitePointTag = 2004119668 # /usr/include/lcms2.h: 388

cmsSigNamedColorTag = 1852010348 # /usr/include/lcms2.h: 388

cmsSigNamedColor2Tag = 1852009522 # /usr/include/lcms2.h: 388

cmsSigOutputResponseTag = 1919251312 # /usr/include/lcms2.h: 388

cmsSigPerceptualRenderingIntentGamutTag = 1919510320 # /usr/include/lcms2.h: 388

cmsSigPreview0Tag = 1886545200 # /usr/include/lcms2.h: 388

cmsSigPreview1Tag = 1886545201 # /usr/include/lcms2.h: 388

cmsSigPreview2Tag = 1886545202 # /usr/include/lcms2.h: 388

cmsSigProfileDescriptionTag = 1684370275 # /usr/include/lcms2.h: 388

cmsSigProfileDescriptionMLTag = 1685283693 # /usr/include/lcms2.h: 388

cmsSigProfileSequenceDescTag = 1886610801 # /usr/include/lcms2.h: 388

cmsSigProfileSequenceIdTag = 1886611812 # /usr/include/lcms2.h: 388

cmsSigPs2CRD0Tag = 1886610480 # /usr/include/lcms2.h: 388

cmsSigPs2CRD1Tag = 1886610481 # /usr/include/lcms2.h: 388

cmsSigPs2CRD2Tag = 1886610482 # /usr/include/lcms2.h: 388

cmsSigPs2CRD3Tag = 1886610483 # /usr/include/lcms2.h: 388

cmsSigPs2CSATag = 1886597747 # /usr/include/lcms2.h: 388

cmsSigPs2RenderingIntentTag = 1886597737 # /usr/include/lcms2.h: 388

cmsSigRedColorantTag = 1918392666 # /usr/include/lcms2.h: 388

cmsSigRedMatrixColumnTag = 1918392666 # /usr/include/lcms2.h: 388

cmsSigRedTRCTag = 1918128707 # /usr/include/lcms2.h: 388

cmsSigSaturationRenderingIntentGamutTag = 1919510322 # /usr/include/lcms2.h: 388

cmsSigScreeningDescTag = 1935897188 # /usr/include/lcms2.h: 388

cmsSigScreeningTag = 1935897198 # /usr/include/lcms2.h: 388

cmsSigTechnologyTag = 1952801640 # /usr/include/lcms2.h: 388

cmsSigUcrBgTag = 1650877472 # /usr/include/lcms2.h: 388

cmsSigViewingCondDescTag = 1987405156 # /usr/include/lcms2.h: 388

cmsSigViewingConditionsTag = 1986618743 # /usr/include/lcms2.h: 388

cmsSigVcgtTag = 1986226036 # /usr/include/lcms2.h: 388

cmsSigMetaTag = 1835365473 # /usr/include/lcms2.h: 388

cmsSigArgyllArtsTag = 1634890867 # /usr/include/lcms2.h: 388

cmsTagSignature = enum_anon_8 # /usr/include/lcms2.h: 388

enum_anon_9 = c_int # /usr/include/lcms2.h: 420

cmsSigDigitalCamera = 1684234605 # /usr/include/lcms2.h: 420

cmsSigFilmScanner = 1718838126 # /usr/include/lcms2.h: 420

cmsSigReflectiveScanner = 1920164718 # /usr/include/lcms2.h: 420

cmsSigInkJetPrinter = 1768580468 # /usr/include/lcms2.h: 420

cmsSigThermalWaxPrinter = 1953980792 # /usr/include/lcms2.h: 420

cmsSigElectrophotographicPrinter = 1701865583 # /usr/include/lcms2.h: 420

cmsSigElectrostaticPrinter = 1702065249 # /usr/include/lcms2.h: 420

cmsSigDyeSublimationPrinter = 1685288290 # /usr/include/lcms2.h: 420

cmsSigPhotographicPaperPrinter = 1919969391 # /usr/include/lcms2.h: 420

cmsSigFilmWriter = 1718645358 # /usr/include/lcms2.h: 420

cmsSigVideoMonitor = 1986618477 # /usr/include/lcms2.h: 420

cmsSigVideoCamera = 1986618467 # /usr/include/lcms2.h: 420

cmsSigProjectionTelevision = 1886024822 # /usr/include/lcms2.h: 420

cmsSigCRTDisplay = 1129468960 # /usr/include/lcms2.h: 420

cmsSigPMDisplay = 1347240992 # /usr/include/lcms2.h: 420

cmsSigAMDisplay = 1095582752 # /usr/include/lcms2.h: 420

cmsSigPhotoCD = 1263551300 # /usr/include/lcms2.h: 420

cmsSigPhotoImageSetter = 1768777587 # /usr/include/lcms2.h: 420

cmsSigGravure = 1735549302 # /usr/include/lcms2.h: 420

cmsSigOffsetLithography = 1868981875 # /usr/include/lcms2.h: 420

cmsSigSilkscreen = 1936288875 # /usr/include/lcms2.h: 420

cmsSigFlexography = 1718379896 # /usr/include/lcms2.h: 420

cmsSigMotionPictureFilmScanner = 1836082803 # /usr/include/lcms2.h: 420

cmsSigMotionPictureFilmRecorder = 1836082802 # /usr/include/lcms2.h: 420

cmsSigDigitalMotionPictureCamera = 1684893795 # /usr/include/lcms2.h: 420

cmsSigDigitalCinemaProjector = 1684236912 # /usr/include/lcms2.h: 420

cmsTechnologySignature = enum_anon_9 # /usr/include/lcms2.h: 420

enum_anon_10 = c_int # /usr/include/lcms2.h: 469

cmsSigXYZData = 1482250784 # /usr/include/lcms2.h: 469

cmsSigLabData = 1281450528 # /usr/include/lcms2.h: 469

cmsSigLuvData = 1282766368 # /usr/include/lcms2.h: 469

cmsSigYCbCrData = 1497588338 # /usr/include/lcms2.h: 469

cmsSigYxyData = 1501067552 # /usr/include/lcms2.h: 469

cmsSigRgbData = 1380401696 # /usr/include/lcms2.h: 469

cmsSigGrayData = 1196573017 # /usr/include/lcms2.h: 469

cmsSigHsvData = 1213421088 # /usr/include/lcms2.h: 469

cmsSigHlsData = 1212961568 # /usr/include/lcms2.h: 469

cmsSigCmykData = 1129142603 # /usr/include/lcms2.h: 469

cmsSigCmyData = 1129142560 # /usr/include/lcms2.h: 469

cmsSigMCH1Data = 1296255025 # /usr/include/lcms2.h: 469

cmsSigMCH2Data = 1296255026 # /usr/include/lcms2.h: 469

cmsSigMCH3Data = 1296255027 # /usr/include/lcms2.h: 469

cmsSigMCH4Data = 1296255028 # /usr/include/lcms2.h: 469

cmsSigMCH5Data = 1296255029 # /usr/include/lcms2.h: 469

cmsSigMCH6Data = 1296255030 # /usr/include/lcms2.h: 469

cmsSigMCH7Data = 1296255031 # /usr/include/lcms2.h: 469

cmsSigMCH8Data = 1296255032 # /usr/include/lcms2.h: 469

cmsSigMCH9Data = 1296255033 # /usr/include/lcms2.h: 469

cmsSigMCHAData = 1296255041 # /usr/include/lcms2.h: 469

cmsSigMCHBData = 1296255042 # /usr/include/lcms2.h: 469

cmsSigMCHCData = 1296255043 # /usr/include/lcms2.h: 469

cmsSigMCHDData = 1296255044 # /usr/include/lcms2.h: 469

cmsSigMCHEData = 1296255045 # /usr/include/lcms2.h: 469

cmsSigMCHFData = 1296255046 # /usr/include/lcms2.h: 469

cmsSigNamedData = 1852662636 # /usr/include/lcms2.h: 469

cmsSig1colorData = 826494034 # /usr/include/lcms2.h: 469

cmsSig2colorData = 843271250 # /usr/include/lcms2.h: 469

cmsSig3colorData = 860048466 # /usr/include/lcms2.h: 469

cmsSig4colorData = 876825682 # /usr/include/lcms2.h: 469

cmsSig5colorData = 893602898 # /usr/include/lcms2.h: 469

cmsSig6colorData = 910380114 # /usr/include/lcms2.h: 469

cmsSig7colorData = 927157330 # /usr/include/lcms2.h: 469

cmsSig8colorData = 943934546 # /usr/include/lcms2.h: 469

cmsSig9colorData = 960711762 # /usr/include/lcms2.h: 469

cmsSig10colorData = 1094929490 # /usr/include/lcms2.h: 469

cmsSig11colorData = 1111706706 # /usr/include/lcms2.h: 469

cmsSig12colorData = 1128483922 # /usr/include/lcms2.h: 469

cmsSig13colorData = 1145261138 # /usr/include/lcms2.h: 469

cmsSig14colorData = 1162038354 # /usr/include/lcms2.h: 469

cmsSig15colorData = 1178815570 # /usr/include/lcms2.h: 469

cmsSigLuvKData = 1282766411 # /usr/include/lcms2.h: 469

cmsColorSpaceSignature = enum_anon_10 # /usr/include/lcms2.h: 469

enum_anon_11 = c_int # /usr/include/lcms2.h: 481

cmsSigInputClass = 1935896178 # /usr/include/lcms2.h: 481

cmsSigDisplayClass = 1835955314 # /usr/include/lcms2.h: 481

cmsSigOutputClass = 1886549106 # /usr/include/lcms2.h: 481

cmsSigLinkClass = 1818848875 # /usr/include/lcms2.h: 481

cmsSigAbstractClass = 1633842036 # /usr/include/lcms2.h: 481

cmsSigColorSpaceClass = 1936744803 # /usr/include/lcms2.h: 481

cmsSigNamedColorClass = 1852662636 # /usr/include/lcms2.h: 481

cmsProfileClassSignature = enum_anon_11 # /usr/include/lcms2.h: 481

enum_anon_12 = c_int # /usr/include/lcms2.h: 492

cmsSigMacintosh = 1095782476 # /usr/include/lcms2.h: 492

cmsSigMicrosoft = 1297303124 # /usr/include/lcms2.h: 492

cmsSigSolaris = 1398099543 # /usr/include/lcms2.h: 492

cmsSigSGI = 1397180704 # /usr/include/lcms2.h: 492

cmsSigTaligent = 1413959252 # /usr/include/lcms2.h: 492

cmsSigUnices = 711879032 # /usr/include/lcms2.h: 492

cmsPlatformSignature = enum_anon_12 # /usr/include/lcms2.h: 492

enum_anon_13 = c_int # /usr/include/lcms2.h: 530

cmsSigCurveSetElemType = 1668707188 # /usr/include/lcms2.h: 530

cmsSigMatrixElemType = 1835103334 # /usr/include/lcms2.h: 530

cmsSigCLutElemType = 1668052340 # /usr/include/lcms2.h: 530

cmsSigBAcsElemType = 1648444243 # /usr/include/lcms2.h: 530

cmsSigEAcsElemType = 1698775891 # /usr/include/lcms2.h: 530

cmsSigXYZ2LabElemType = 1815246880 # /usr/include/lcms2.h: 530

cmsSigLab2XYZElemType = 2016570400 # /usr/include/lcms2.h: 530

cmsSigNamedColorElemType = 1852009504 # /usr/include/lcms2.h: 530

cmsSigLabV2toV4 = 840971296 # /usr/include/lcms2.h: 530

cmsSigLabV4toV2 = 874525216 # /usr/include/lcms2.h: 530

cmsSigIdentityElemType = 1768189472 # /usr/include/lcms2.h: 530

cmsSigLab2FloatPCS = 1681026080 # /usr/include/lcms2.h: 530

cmsSigFloatPCS2Lab = 1815241760 # /usr/include/lcms2.h: 530

cmsSigXYZ2FloatPCS = 1681029152 # /usr/include/lcms2.h: 530

cmsSigFloatPCS2XYZ = 2016568352 # /usr/include/lcms2.h: 530

cmsSigClipNegativesElemType = 1668050976 # /usr/include/lcms2.h: 530

cmsStageSignature = enum_anon_13 # /usr/include/lcms2.h: 530

enum_anon_14 = c_int # /usr/include/lcms2.h: 539

cmsSigFormulaCurveSeg = 1885434470 # /usr/include/lcms2.h: 539

cmsSigSampledCurveSeg = 1935764838 # /usr/include/lcms2.h: 539

cmsSigSegmentedCurve = 1668641382 # /usr/include/lcms2.h: 539

cmsCurveSegSignature = enum_anon_14 # /usr/include/lcms2.h: 539

# /usr/include/lcms2.h: 565
class struct_anon_15(Structure):
    pass

struct_anon_15.__slots__ = [
    'len',
    'flag',
    'data',
]
struct_anon_15._fields_ = [
    ('len', cmsUInt32Number),
    ('flag', cmsUInt32Number),
    ('data', cmsUInt8Number * 1),
]

cmsICCData = struct_anon_15 # /usr/include/lcms2.h: 565

# /usr/include/lcms2.h: 576
class struct_anon_16(Structure):
    pass

struct_anon_16.__slots__ = [
    'year',
    'month',
    'day',
    'hours',
    'minutes',
    'seconds',
]
struct_anon_16._fields_ = [
    ('year', cmsUInt16Number),
    ('month', cmsUInt16Number),
    ('day', cmsUInt16Number),
    ('hours', cmsUInt16Number),
    ('minutes', cmsUInt16Number),
    ('seconds', cmsUInt16Number),
]

cmsDateTimeNumber = struct_anon_16 # /usr/include/lcms2.h: 576

# /usr/include/lcms2.h: 584
class struct_anon_17(Structure):
    pass

struct_anon_17.__slots__ = [
    'X',
    'Y',
    'Z',
]
struct_anon_17._fields_ = [
    ('X', cmsS15Fixed16Number),
    ('Y', cmsS15Fixed16Number),
    ('Z', cmsS15Fixed16Number),
]

cmsEncodedXYZNumber = struct_anon_17 # /usr/include/lcms2.h: 584

# /usr/include/lcms2.h: 593
class union_anon_18(Union):
    pass

union_anon_18.__slots__ = [
    'ID8',
    'ID16',
    'ID32',
]
union_anon_18._fields_ = [
    ('ID8', cmsUInt8Number * 16),
    ('ID16', cmsUInt16Number * 8),
    ('ID32', cmsUInt32Number * 4),
]

cmsProfileID = union_anon_18 # /usr/include/lcms2.h: 593

# /usr/include/lcms2.h: 621
class struct_anon_19(Structure):
    pass

struct_anon_19.__slots__ = [
    'size',
    'cmmId',
    'version',
    'deviceClass',
    'colorSpace',
    'pcs',
    'date',
    'magic',
    'platform',
    'flags',
    'manufacturer',
    'model',
    'attributes',
    'renderingIntent',
    'illuminant',
    'creator',
    'profileID',
    'reserved',
]
struct_anon_19._fields_ = [
    ('size', cmsUInt32Number),
    ('cmmId', cmsSignature),
    ('version', cmsUInt32Number),
    ('deviceClass', cmsProfileClassSignature),
    ('colorSpace', cmsColorSpaceSignature),
    ('pcs', cmsColorSpaceSignature),
    ('date', cmsDateTimeNumber),
    ('magic', cmsSignature),
    ('platform', cmsPlatformSignature),
    ('flags', cmsUInt32Number),
    ('manufacturer', cmsSignature),
    ('model', cmsUInt32Number),
    ('attributes', cmsUInt64Number),
    ('renderingIntent', cmsUInt32Number),
    ('illuminant', cmsEncodedXYZNumber),
    ('creator', cmsSignature),
    ('profileID', cmsProfileID),
    ('reserved', cmsInt8Number * 28),
]

cmsICCHeader = struct_anon_19 # /usr/include/lcms2.h: 621

# /usr/include/lcms2.h: 628
class struct_anon_20(Structure):
    pass

struct_anon_20.__slots__ = [
    'sig',
    'reserved',
]
struct_anon_20._fields_ = [
    ('sig', cmsTagTypeSignature),
    ('reserved', cmsInt8Number * 4),
]

cmsTagBase = struct_anon_20 # /usr/include/lcms2.h: 628

# /usr/include/lcms2.h: 636
class struct_anon_21(Structure):
    pass

struct_anon_21.__slots__ = [
    'sig',
    'offset',
    'size',
]
struct_anon_21._fields_ = [
    ('sig', cmsTagSignature),
    ('offset', cmsUInt32Number),
    ('size', cmsUInt32Number),
]

cmsTagEntry = struct_anon_21 # /usr/include/lcms2.h: 636

cmsHANDLE = POINTER(None) # /usr/include/lcms2.h: 642

cmsHPROFILE = POINTER(None) # /usr/include/lcms2.h: 643

cmsHTRANSFORM = POINTER(None) # /usr/include/lcms2.h: 644

# /usr/include/lcms2.h: 935
class struct_anon_22(Structure):
    pass

struct_anon_22.__slots__ = [
    'X',
    'Y',
    'Z',
]
struct_anon_22._fields_ = [
    ('X', cmsFloat64Number),
    ('Y', cmsFloat64Number),
    ('Z', cmsFloat64Number),
]

cmsCIEXYZ = struct_anon_22 # /usr/include/lcms2.h: 935

# /usr/include/lcms2.h: 942
class struct_anon_23(Structure):
    pass

struct_anon_23.__slots__ = [
    'x',
    'y',
    'Y',
]
struct_anon_23._fields_ = [
    ('x', cmsFloat64Number),
    ('y', cmsFloat64Number),
    ('Y', cmsFloat64Number),
]

cmsCIExyY = struct_anon_23 # /usr/include/lcms2.h: 942

# /usr/include/lcms2.h: 949
class struct_anon_24(Structure):
    pass

struct_anon_24.__slots__ = [
    'L',
    'a',
    'b',
]
struct_anon_24._fields_ = [
    ('L', cmsFloat64Number),
    ('a', cmsFloat64Number),
    ('b', cmsFloat64Number),
]

cmsCIELab = struct_anon_24 # /usr/include/lcms2.h: 949

# /usr/include/lcms2.h: 956
class struct_anon_25(Structure):
    pass

struct_anon_25.__slots__ = [
    'L',
    'C',
    'h',
]
struct_anon_25._fields_ = [
    ('L', cmsFloat64Number),
    ('C', cmsFloat64Number),
    ('h', cmsFloat64Number),
]

cmsCIELCh = struct_anon_25 # /usr/include/lcms2.h: 956

# /usr/include/lcms2.h: 963
class struct_anon_26(Structure):
    pass

struct_anon_26.__slots__ = [
    'J',
    'C',
    'h',
]
struct_anon_26._fields_ = [
    ('J', cmsFloat64Number),
    ('C', cmsFloat64Number),
    ('h', cmsFloat64Number),
]

cmsJCh = struct_anon_26 # /usr/include/lcms2.h: 963

# /usr/include/lcms2.h: 970
class struct_anon_27(Structure):
    pass

struct_anon_27.__slots__ = [
    'Red',
    'Green',
    'Blue',
]
struct_anon_27._fields_ = [
    ('Red', cmsCIEXYZ),
    ('Green', cmsCIEXYZ),
    ('Blue', cmsCIEXYZ),
]

cmsCIEXYZTRIPLE = struct_anon_27 # /usr/include/lcms2.h: 970

# /usr/include/lcms2.h: 977
class struct_anon_28(Structure):
    pass

struct_anon_28.__slots__ = [
    'Red',
    'Green',
    'Blue',
]
struct_anon_28._fields_ = [
    ('Red', cmsCIExyY),
    ('Green', cmsCIExyY),
    ('Blue', cmsCIExyY),
]

cmsCIExyYTRIPLE = struct_anon_28 # /usr/include/lcms2.h: 977

# /usr/include/lcms2.h: 997
class struct_anon_29(Structure):
    pass

struct_anon_29.__slots__ = [
    'Observer',
    'Backing',
    'Geometry',
    'Flare',
    'IlluminantType',
]
struct_anon_29._fields_ = [
    ('Observer', cmsUInt32Number),
    ('Backing', cmsCIEXYZ),
    ('Geometry', cmsUInt32Number),
    ('Flare', cmsFloat64Number),
    ('IlluminantType', cmsUInt32Number),
]

cmsICCMeasurementConditions = struct_anon_29 # /usr/include/lcms2.h: 997

# /usr/include/lcms2.h: 1004
class struct_anon_30(Structure):
    pass

struct_anon_30.__slots__ = [
    'IlluminantXYZ',
    'SurroundXYZ',
    'IlluminantType',
]
struct_anon_30._fields_ = [
    ('IlluminantXYZ', cmsCIEXYZ),
    ('SurroundXYZ', cmsCIEXYZ),
    ('IlluminantType', cmsUInt32Number),
]

cmsICCViewingConditions = struct_anon_30 # /usr/include/lcms2.h: 1004

# /usr/include/lcms2.h: 1008
if hasattr(_libs['lcms2'], 'cmsGetEncodedCMMversion'):
    cmsGetEncodedCMMversion = _libs['lcms2'].cmsGetEncodedCMMversion
    cmsGetEncodedCMMversion.argtypes = []
    cmsGetEncodedCMMversion.restype = c_int

# /usr/include/lcms2.h: 1012
if hasattr(_libs['lcms2'], 'cmsstrcasecmp'):
    cmsstrcasecmp = _libs['lcms2'].cmsstrcasecmp
    cmsstrcasecmp.argtypes = [String, String]
    cmsstrcasecmp.restype = c_int

# /usr/include/lcms2.h: 1013
if hasattr(_libs['lcms2'], 'cmsfilelength'):
    cmsfilelength = _libs['lcms2'].cmsfilelength
    cmsfilelength.argtypes = [POINTER(FILE)]
    cmsfilelength.restype = c_long

# /usr/include/lcms2.h: 1021
class struct__cmsContext_struct(Structure):
    pass

cmsContext = POINTER(struct__cmsContext_struct) # /usr/include/lcms2.h: 1021

# /usr/include/lcms2.h: 1023
if hasattr(_libs['lcms2'], 'cmsCreateContext'):
    cmsCreateContext = _libs['lcms2'].cmsCreateContext
    cmsCreateContext.argtypes = [POINTER(None), POINTER(None)]
    cmsCreateContext.restype = cmsContext

# /usr/include/lcms2.h: 1024
if hasattr(_libs['lcms2'], 'cmsDeleteContext'):
    cmsDeleteContext = _libs['lcms2'].cmsDeleteContext
    cmsDeleteContext.argtypes = [cmsContext]
    cmsDeleteContext.restype = None

# /usr/include/lcms2.h: 1025
if hasattr(_libs['lcms2'], 'cmsDupContext'):
    cmsDupContext = _libs['lcms2'].cmsDupContext
    cmsDupContext.argtypes = [cmsContext, POINTER(None)]
    cmsDupContext.restype = cmsContext

# /usr/include/lcms2.h: 1026
if hasattr(_libs['lcms2'], 'cmsGetContextUserData'):
    cmsGetContextUserData = _libs['lcms2'].cmsGetContextUserData
    cmsGetContextUserData.argtypes = [cmsContext]
    cmsGetContextUserData.restype = POINTER(c_ubyte)
    cmsGetContextUserData.errcheck = lambda v,*a : cast(v, c_void_p)

# /usr/include/lcms2.h: 1030
if hasattr(_libs['lcms2'], 'cmsPlugin'):
    cmsPlugin = _libs['lcms2'].cmsPlugin
    cmsPlugin.argtypes = [POINTER(None)]
    cmsPlugin.restype = cmsBool

# /usr/include/lcms2.h: 1031
if hasattr(_libs['lcms2'], 'cmsPluginTHR'):
    cmsPluginTHR = _libs['lcms2'].cmsPluginTHR
    cmsPluginTHR.argtypes = [cmsContext, POINTER(None)]
    cmsPluginTHR.restype = cmsBool

# /usr/include/lcms2.h: 1032
if hasattr(_libs['lcms2'], 'cmsUnregisterPlugins'):
    cmsUnregisterPlugins = _libs['lcms2'].cmsUnregisterPlugins
    cmsUnregisterPlugins.argtypes = []
    cmsUnregisterPlugins.restype = None

# /usr/include/lcms2.h: 1033
if hasattr(_libs['lcms2'], 'cmsUnregisterPluginsTHR'):
    cmsUnregisterPluginsTHR = _libs['lcms2'].cmsUnregisterPluginsTHR
    cmsUnregisterPluginsTHR.argtypes = [cmsContext]
    cmsUnregisterPluginsTHR.restype = None

cmsLogErrorHandlerFunction = CFUNCTYPE(UNCHECKED(None), cmsContext, cmsUInt32Number, String) # /usr/include/lcms2.h: 1066

# /usr/include/lcms2.h: 1069
if hasattr(_libs['lcms2'], 'cmsSetLogErrorHandler'):
    cmsSetLogErrorHandler = _libs['lcms2'].cmsSetLogErrorHandler
    cmsSetLogErrorHandler.argtypes = [cmsLogErrorHandlerFunction]
    cmsSetLogErrorHandler.restype = None

# /usr/include/lcms2.h: 1070
if hasattr(_libs['lcms2'], 'cmsSetLogErrorHandlerTHR'):
    cmsSetLogErrorHandlerTHR = _libs['lcms2'].cmsSetLogErrorHandlerTHR
    cmsSetLogErrorHandlerTHR.argtypes = [cmsContext, cmsLogErrorHandlerFunction]
    cmsSetLogErrorHandlerTHR.restype = None

# /usr/include/lcms2.h: 1075
if hasattr(_libs['lcms2'], 'cmsD50_XYZ'):
    cmsD50_XYZ = _libs['lcms2'].cmsD50_XYZ
    cmsD50_XYZ.argtypes = []
    cmsD50_XYZ.restype = POINTER(cmsCIEXYZ)

# /usr/include/lcms2.h: 1076
if hasattr(_libs['lcms2'], 'cmsD50_xyY'):
    cmsD50_xyY = _libs['lcms2'].cmsD50_xyY
    cmsD50_xyY.argtypes = []
    cmsD50_xyY.restype = POINTER(cmsCIExyY)

# /usr/include/lcms2.h: 1079
if hasattr(_libs['lcms2'], 'cmsXYZ2xyY'):
    cmsXYZ2xyY = _libs['lcms2'].cmsXYZ2xyY
    cmsXYZ2xyY.argtypes = [POINTER(cmsCIExyY), POINTER(cmsCIEXYZ)]
    cmsXYZ2xyY.restype = None

# /usr/include/lcms2.h: 1080
if hasattr(_libs['lcms2'], 'cmsxyY2XYZ'):
    cmsxyY2XYZ = _libs['lcms2'].cmsxyY2XYZ
    cmsxyY2XYZ.argtypes = [POINTER(cmsCIEXYZ), POINTER(cmsCIExyY)]
    cmsxyY2XYZ.restype = None

# /usr/include/lcms2.h: 1081
if hasattr(_libs['lcms2'], 'cmsXYZ2Lab'):
    cmsXYZ2Lab = _libs['lcms2'].cmsXYZ2Lab
    cmsXYZ2Lab.argtypes = [POINTER(cmsCIEXYZ), POINTER(cmsCIELab), POINTER(cmsCIEXYZ)]
    cmsXYZ2Lab.restype = None

# /usr/include/lcms2.h: 1082
if hasattr(_libs['lcms2'], 'cmsLab2XYZ'):
    cmsLab2XYZ = _libs['lcms2'].cmsLab2XYZ
    cmsLab2XYZ.argtypes = [POINTER(cmsCIEXYZ), POINTER(cmsCIEXYZ), POINTER(cmsCIELab)]
    cmsLab2XYZ.restype = None

# /usr/include/lcms2.h: 1083
if hasattr(_libs['lcms2'], 'cmsLab2LCh'):
    cmsLab2LCh = _libs['lcms2'].cmsLab2LCh
    cmsLab2LCh.argtypes = [POINTER(cmsCIELCh), POINTER(cmsCIELab)]
    cmsLab2LCh.restype = None

# /usr/include/lcms2.h: 1084
if hasattr(_libs['lcms2'], 'cmsLCh2Lab'):
    cmsLCh2Lab = _libs['lcms2'].cmsLCh2Lab
    cmsLCh2Lab.argtypes = [POINTER(cmsCIELab), POINTER(cmsCIELCh)]
    cmsLCh2Lab.restype = None

# /usr/include/lcms2.h: 1087
if hasattr(_libs['lcms2'], 'cmsLabEncoded2Float'):
    cmsLabEncoded2Float = _libs['lcms2'].cmsLabEncoded2Float
    cmsLabEncoded2Float.argtypes = [POINTER(cmsCIELab), cmsUInt16Number * 3]
    cmsLabEncoded2Float.restype = None

# /usr/include/lcms2.h: 1088
if hasattr(_libs['lcms2'], 'cmsLabEncoded2FloatV2'):
    cmsLabEncoded2FloatV2 = _libs['lcms2'].cmsLabEncoded2FloatV2
    cmsLabEncoded2FloatV2.argtypes = [POINTER(cmsCIELab), cmsUInt16Number * 3]
    cmsLabEncoded2FloatV2.restype = None

# /usr/include/lcms2.h: 1089
if hasattr(_libs['lcms2'], 'cmsFloat2LabEncoded'):
    cmsFloat2LabEncoded = _libs['lcms2'].cmsFloat2LabEncoded
    cmsFloat2LabEncoded.argtypes = [cmsUInt16Number * 3, POINTER(cmsCIELab)]
    cmsFloat2LabEncoded.restype = None

# /usr/include/lcms2.h: 1090
if hasattr(_libs['lcms2'], 'cmsFloat2LabEncodedV2'):
    cmsFloat2LabEncodedV2 = _libs['lcms2'].cmsFloat2LabEncodedV2
    cmsFloat2LabEncodedV2.argtypes = [cmsUInt16Number * 3, POINTER(cmsCIELab)]
    cmsFloat2LabEncodedV2.restype = None

# /usr/include/lcms2.h: 1091
if hasattr(_libs['lcms2'], 'cmsXYZEncoded2Float'):
    cmsXYZEncoded2Float = _libs['lcms2'].cmsXYZEncoded2Float
    cmsXYZEncoded2Float.argtypes = [POINTER(cmsCIEXYZ), cmsUInt16Number * 3]
    cmsXYZEncoded2Float.restype = None

# /usr/include/lcms2.h: 1092
if hasattr(_libs['lcms2'], 'cmsFloat2XYZEncoded'):
    cmsFloat2XYZEncoded = _libs['lcms2'].cmsFloat2XYZEncoded
    cmsFloat2XYZEncoded.argtypes = [cmsUInt16Number * 3, POINTER(cmsCIEXYZ)]
    cmsFloat2XYZEncoded.restype = None

# /usr/include/lcms2.h: 1095
if hasattr(_libs['lcms2'], 'cmsDeltaE'):
    cmsDeltaE = _libs['lcms2'].cmsDeltaE
    cmsDeltaE.argtypes = [POINTER(cmsCIELab), POINTER(cmsCIELab)]
    cmsDeltaE.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1096
if hasattr(_libs['lcms2'], 'cmsCIE94DeltaE'):
    cmsCIE94DeltaE = _libs['lcms2'].cmsCIE94DeltaE
    cmsCIE94DeltaE.argtypes = [POINTER(cmsCIELab), POINTER(cmsCIELab)]
    cmsCIE94DeltaE.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1097
if hasattr(_libs['lcms2'], 'cmsBFDdeltaE'):
    cmsBFDdeltaE = _libs['lcms2'].cmsBFDdeltaE
    cmsBFDdeltaE.argtypes = [POINTER(cmsCIELab), POINTER(cmsCIELab)]
    cmsBFDdeltaE.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1098
if hasattr(_libs['lcms2'], 'cmsCMCdeltaE'):
    cmsCMCdeltaE = _libs['lcms2'].cmsCMCdeltaE
    cmsCMCdeltaE.argtypes = [POINTER(cmsCIELab), POINTER(cmsCIELab), cmsFloat64Number, cmsFloat64Number]
    cmsCMCdeltaE.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1099
if hasattr(_libs['lcms2'], 'cmsCIE2000DeltaE'):
    cmsCIE2000DeltaE = _libs['lcms2'].cmsCIE2000DeltaE
    cmsCIE2000DeltaE.argtypes = [POINTER(cmsCIELab), POINTER(cmsCIELab), cmsFloat64Number, cmsFloat64Number, cmsFloat64Number]
    cmsCIE2000DeltaE.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1102
if hasattr(_libs['lcms2'], 'cmsWhitePointFromTemp'):
    cmsWhitePointFromTemp = _libs['lcms2'].cmsWhitePointFromTemp
    cmsWhitePointFromTemp.argtypes = [POINTER(cmsCIExyY), cmsFloat64Number]
    cmsWhitePointFromTemp.restype = cmsBool

# /usr/include/lcms2.h: 1103
if hasattr(_libs['lcms2'], 'cmsTempFromWhitePoint'):
    cmsTempFromWhitePoint = _libs['lcms2'].cmsTempFromWhitePoint
    cmsTempFromWhitePoint.argtypes = [POINTER(cmsFloat64Number), POINTER(cmsCIExyY)]
    cmsTempFromWhitePoint.restype = cmsBool

# /usr/include/lcms2.h: 1106
if hasattr(_libs['lcms2'], 'cmsAdaptToIlluminant'):
    cmsAdaptToIlluminant = _libs['lcms2'].cmsAdaptToIlluminant
    cmsAdaptToIlluminant.argtypes = [POINTER(cmsCIEXYZ), POINTER(cmsCIEXYZ), POINTER(cmsCIEXYZ), POINTER(cmsCIEXYZ)]
    cmsAdaptToIlluminant.restype = cmsBool

# /usr/include/lcms2.h: 1131
class struct_anon_31(Structure):
    pass

struct_anon_31.__slots__ = [
    'whitePoint',
    'Yb',
    'La',
    'surround',
    'D_value',
]
struct_anon_31._fields_ = [
    ('whitePoint', cmsCIEXYZ),
    ('Yb', cmsFloat64Number),
    ('La', cmsFloat64Number),
    ('surround', c_int),
    ('D_value', cmsFloat64Number),
]

cmsViewingConditions = struct_anon_31 # /usr/include/lcms2.h: 1131

# /usr/include/lcms2.h: 1133
if hasattr(_libs['lcms2'], 'cmsCIECAM02Init'):
    cmsCIECAM02Init = _libs['lcms2'].cmsCIECAM02Init
    cmsCIECAM02Init.argtypes = [cmsContext, POINTER(cmsViewingConditions)]
    cmsCIECAM02Init.restype = cmsHANDLE

# /usr/include/lcms2.h: 1134
if hasattr(_libs['lcms2'], 'cmsCIECAM02Done'):
    cmsCIECAM02Done = _libs['lcms2'].cmsCIECAM02Done
    cmsCIECAM02Done.argtypes = [cmsHANDLE]
    cmsCIECAM02Done.restype = None

# /usr/include/lcms2.h: 1135
if hasattr(_libs['lcms2'], 'cmsCIECAM02Forward'):
    cmsCIECAM02Forward = _libs['lcms2'].cmsCIECAM02Forward
    cmsCIECAM02Forward.argtypes = [cmsHANDLE, POINTER(cmsCIEXYZ), POINTER(cmsJCh)]
    cmsCIECAM02Forward.restype = None

# /usr/include/lcms2.h: 1136
if hasattr(_libs['lcms2'], 'cmsCIECAM02Reverse'):
    cmsCIECAM02Reverse = _libs['lcms2'].cmsCIECAM02Reverse
    cmsCIECAM02Reverse.argtypes = [cmsHANDLE, POINTER(cmsJCh), POINTER(cmsCIEXYZ)]
    cmsCIECAM02Reverse.restype = None

# /usr/include/lcms2.h: 1151
class struct_anon_32(Structure):
    pass

struct_anon_32.__slots__ = [
    'x0',
    'x1',
    'Type',
    'Params',
    'nGridPoints',
    'SampledPoints',
]
struct_anon_32._fields_ = [
    ('x0', cmsFloat32Number),
    ('x1', cmsFloat32Number),
    ('Type', cmsInt32Number),
    ('Params', cmsFloat64Number * 10),
    ('nGridPoints', cmsUInt32Number),
    ('SampledPoints', POINTER(cmsFloat32Number)),
]

cmsCurveSegment = struct_anon_32 # /usr/include/lcms2.h: 1151

# /usr/include/lcms2.h: 1154
class struct__cms_curve_struct(Structure):
    pass

cmsToneCurve = struct__cms_curve_struct # /usr/include/lcms2.h: 1154

# /usr/include/lcms2.h: 1156
if hasattr(_libs['lcms2'], 'cmsBuildSegmentedToneCurve'):
    cmsBuildSegmentedToneCurve = _libs['lcms2'].cmsBuildSegmentedToneCurve
    cmsBuildSegmentedToneCurve.argtypes = [cmsContext, cmsInt32Number, POINTER(cmsCurveSegment)]
    cmsBuildSegmentedToneCurve.restype = POINTER(cmsToneCurve)

# /usr/include/lcms2.h: 1157
if hasattr(_libs['lcms2'], 'cmsBuildParametricToneCurve'):
    cmsBuildParametricToneCurve = _libs['lcms2'].cmsBuildParametricToneCurve
    cmsBuildParametricToneCurve.argtypes = [cmsContext, cmsInt32Number, POINTER(cmsFloat64Number)]
    cmsBuildParametricToneCurve.restype = POINTER(cmsToneCurve)

# /usr/include/lcms2.h: 1158
if hasattr(_libs['lcms2'], 'cmsBuildGamma'):
    cmsBuildGamma = _libs['lcms2'].cmsBuildGamma
    cmsBuildGamma.argtypes = [cmsContext, cmsFloat64Number]
    cmsBuildGamma.restype = POINTER(cmsToneCurve)

# /usr/include/lcms2.h: 1159
if hasattr(_libs['lcms2'], 'cmsBuildTabulatedToneCurve16'):
    cmsBuildTabulatedToneCurve16 = _libs['lcms2'].cmsBuildTabulatedToneCurve16
    cmsBuildTabulatedToneCurve16.argtypes = [cmsContext, cmsInt32Number, POINTER(cmsUInt16Number)]
    cmsBuildTabulatedToneCurve16.restype = POINTER(cmsToneCurve)

# /usr/include/lcms2.h: 1160
if hasattr(_libs['lcms2'], 'cmsBuildTabulatedToneCurveFloat'):
    cmsBuildTabulatedToneCurveFloat = _libs['lcms2'].cmsBuildTabulatedToneCurveFloat
    cmsBuildTabulatedToneCurveFloat.argtypes = [cmsContext, cmsUInt32Number, POINTER(cmsFloat32Number)]
    cmsBuildTabulatedToneCurveFloat.restype = POINTER(cmsToneCurve)

# /usr/include/lcms2.h: 1161
if hasattr(_libs['lcms2'], 'cmsFreeToneCurve'):
    cmsFreeToneCurve = _libs['lcms2'].cmsFreeToneCurve
    cmsFreeToneCurve.argtypes = [POINTER(cmsToneCurve)]
    cmsFreeToneCurve.restype = None

# /usr/include/lcms2.h: 1162
if hasattr(_libs['lcms2'], 'cmsFreeToneCurveTriple'):
    cmsFreeToneCurveTriple = _libs['lcms2'].cmsFreeToneCurveTriple
    cmsFreeToneCurveTriple.argtypes = [POINTER(cmsToneCurve) * 3]
    cmsFreeToneCurveTriple.restype = None

# /usr/include/lcms2.h: 1163
if hasattr(_libs['lcms2'], 'cmsDupToneCurve'):
    cmsDupToneCurve = _libs['lcms2'].cmsDupToneCurve
    cmsDupToneCurve.argtypes = [POINTER(cmsToneCurve)]
    cmsDupToneCurve.restype = POINTER(cmsToneCurve)

# /usr/include/lcms2.h: 1164
if hasattr(_libs['lcms2'], 'cmsReverseToneCurve'):
    cmsReverseToneCurve = _libs['lcms2'].cmsReverseToneCurve
    cmsReverseToneCurve.argtypes = [POINTER(cmsToneCurve)]
    cmsReverseToneCurve.restype = POINTER(cmsToneCurve)

# /usr/include/lcms2.h: 1165
if hasattr(_libs['lcms2'], 'cmsReverseToneCurveEx'):
    cmsReverseToneCurveEx = _libs['lcms2'].cmsReverseToneCurveEx
    cmsReverseToneCurveEx.argtypes = [cmsInt32Number, POINTER(cmsToneCurve)]
    cmsReverseToneCurveEx.restype = POINTER(cmsToneCurve)

# /usr/include/lcms2.h: 1166
if hasattr(_libs['lcms2'], 'cmsJoinToneCurve'):
    cmsJoinToneCurve = _libs['lcms2'].cmsJoinToneCurve
    cmsJoinToneCurve.argtypes = [cmsContext, POINTER(cmsToneCurve), POINTER(cmsToneCurve), cmsUInt32Number]
    cmsJoinToneCurve.restype = POINTER(cmsToneCurve)

# /usr/include/lcms2.h: 1167
if hasattr(_libs['lcms2'], 'cmsSmoothToneCurve'):
    cmsSmoothToneCurve = _libs['lcms2'].cmsSmoothToneCurve
    cmsSmoothToneCurve.argtypes = [POINTER(cmsToneCurve), cmsFloat64Number]
    cmsSmoothToneCurve.restype = cmsBool

# /usr/include/lcms2.h: 1168
if hasattr(_libs['lcms2'], 'cmsEvalToneCurveFloat'):
    cmsEvalToneCurveFloat = _libs['lcms2'].cmsEvalToneCurveFloat
    cmsEvalToneCurveFloat.argtypes = [POINTER(cmsToneCurve), cmsFloat32Number]
    cmsEvalToneCurveFloat.restype = cmsFloat32Number

# /usr/include/lcms2.h: 1169
if hasattr(_libs['lcms2'], 'cmsEvalToneCurve16'):
    cmsEvalToneCurve16 = _libs['lcms2'].cmsEvalToneCurve16
    cmsEvalToneCurve16.argtypes = [POINTER(cmsToneCurve), cmsUInt16Number]
    cmsEvalToneCurve16.restype = cmsUInt16Number

# /usr/include/lcms2.h: 1170
if hasattr(_libs['lcms2'], 'cmsIsToneCurveMultisegment'):
    cmsIsToneCurveMultisegment = _libs['lcms2'].cmsIsToneCurveMultisegment
    cmsIsToneCurveMultisegment.argtypes = [POINTER(cmsToneCurve)]
    cmsIsToneCurveMultisegment.restype = cmsBool

# /usr/include/lcms2.h: 1171
if hasattr(_libs['lcms2'], 'cmsIsToneCurveLinear'):
    cmsIsToneCurveLinear = _libs['lcms2'].cmsIsToneCurveLinear
    cmsIsToneCurveLinear.argtypes = [POINTER(cmsToneCurve)]
    cmsIsToneCurveLinear.restype = cmsBool

# /usr/include/lcms2.h: 1172
if hasattr(_libs['lcms2'], 'cmsIsToneCurveMonotonic'):
    cmsIsToneCurveMonotonic = _libs['lcms2'].cmsIsToneCurveMonotonic
    cmsIsToneCurveMonotonic.argtypes = [POINTER(cmsToneCurve)]
    cmsIsToneCurveMonotonic.restype = cmsBool

# /usr/include/lcms2.h: 1173
if hasattr(_libs['lcms2'], 'cmsIsToneCurveDescending'):
    cmsIsToneCurveDescending = _libs['lcms2'].cmsIsToneCurveDescending
    cmsIsToneCurveDescending.argtypes = [POINTER(cmsToneCurve)]
    cmsIsToneCurveDescending.restype = cmsBool

# /usr/include/lcms2.h: 1174
if hasattr(_libs['lcms2'], 'cmsGetToneCurveParametricType'):
    cmsGetToneCurveParametricType = _libs['lcms2'].cmsGetToneCurveParametricType
    cmsGetToneCurveParametricType.argtypes = [POINTER(cmsToneCurve)]
    cmsGetToneCurveParametricType.restype = cmsInt32Number

# /usr/include/lcms2.h: 1175
if hasattr(_libs['lcms2'], 'cmsEstimateGamma'):
    cmsEstimateGamma = _libs['lcms2'].cmsEstimateGamma
    cmsEstimateGamma.argtypes = [POINTER(cmsToneCurve), cmsFloat64Number]
    cmsEstimateGamma.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1178
if hasattr(_libs['lcms2'], 'cmsGetToneCurveEstimatedTableEntries'):
    cmsGetToneCurveEstimatedTableEntries = _libs['lcms2'].cmsGetToneCurveEstimatedTableEntries
    cmsGetToneCurveEstimatedTableEntries.argtypes = [POINTER(cmsToneCurve)]
    cmsGetToneCurveEstimatedTableEntries.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1179
if hasattr(_libs['lcms2'], 'cmsGetToneCurveEstimatedTable'):
    cmsGetToneCurveEstimatedTable = _libs['lcms2'].cmsGetToneCurveEstimatedTable
    cmsGetToneCurveEstimatedTable.argtypes = [POINTER(cmsToneCurve)]
    cmsGetToneCurveEstimatedTable.restype = POINTER(cmsUInt16Number)

# /usr/include/lcms2.h: 1185
class struct__cmsPipeline_struct(Structure):
    pass

cmsPipeline = struct__cmsPipeline_struct # /usr/include/lcms2.h: 1185

# /usr/include/lcms2.h: 1186
class struct__cmsStage_struct(Structure):
    pass

cmsStage = struct__cmsStage_struct # /usr/include/lcms2.h: 1186

# /usr/include/lcms2.h: 1189
if hasattr(_libs['lcms2'], 'cmsPipelineAlloc'):
    cmsPipelineAlloc = _libs['lcms2'].cmsPipelineAlloc
    cmsPipelineAlloc.argtypes = [cmsContext, cmsUInt32Number, cmsUInt32Number]
    cmsPipelineAlloc.restype = POINTER(cmsPipeline)

# /usr/include/lcms2.h: 1190
if hasattr(_libs['lcms2'], 'cmsPipelineFree'):
    cmsPipelineFree = _libs['lcms2'].cmsPipelineFree
    cmsPipelineFree.argtypes = [POINTER(cmsPipeline)]
    cmsPipelineFree.restype = None

# /usr/include/lcms2.h: 1191
if hasattr(_libs['lcms2'], 'cmsPipelineDup'):
    cmsPipelineDup = _libs['lcms2'].cmsPipelineDup
    cmsPipelineDup.argtypes = [POINTER(cmsPipeline)]
    cmsPipelineDup.restype = POINTER(cmsPipeline)

# /usr/include/lcms2.h: 1193
if hasattr(_libs['lcms2'], 'cmsGetPipelineContextID'):
    cmsGetPipelineContextID = _libs['lcms2'].cmsGetPipelineContextID
    cmsGetPipelineContextID.argtypes = [POINTER(cmsPipeline)]
    cmsGetPipelineContextID.restype = cmsContext

# /usr/include/lcms2.h: 1194
if hasattr(_libs['lcms2'], 'cmsPipelineInputChannels'):
    cmsPipelineInputChannels = _libs['lcms2'].cmsPipelineInputChannels
    cmsPipelineInputChannels.argtypes = [POINTER(cmsPipeline)]
    cmsPipelineInputChannels.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1195
if hasattr(_libs['lcms2'], 'cmsPipelineOutputChannels'):
    cmsPipelineOutputChannels = _libs['lcms2'].cmsPipelineOutputChannels
    cmsPipelineOutputChannels.argtypes = [POINTER(cmsPipeline)]
    cmsPipelineOutputChannels.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1197
if hasattr(_libs['lcms2'], 'cmsPipelineStageCount'):
    cmsPipelineStageCount = _libs['lcms2'].cmsPipelineStageCount
    cmsPipelineStageCount.argtypes = [POINTER(cmsPipeline)]
    cmsPipelineStageCount.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1198
if hasattr(_libs['lcms2'], 'cmsPipelineGetPtrToFirstStage'):
    cmsPipelineGetPtrToFirstStage = _libs['lcms2'].cmsPipelineGetPtrToFirstStage
    cmsPipelineGetPtrToFirstStage.argtypes = [POINTER(cmsPipeline)]
    cmsPipelineGetPtrToFirstStage.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1199
if hasattr(_libs['lcms2'], 'cmsPipelineGetPtrToLastStage'):
    cmsPipelineGetPtrToLastStage = _libs['lcms2'].cmsPipelineGetPtrToLastStage
    cmsPipelineGetPtrToLastStage.argtypes = [POINTER(cmsPipeline)]
    cmsPipelineGetPtrToLastStage.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1201
if hasattr(_libs['lcms2'], 'cmsPipelineEval16'):
    cmsPipelineEval16 = _libs['lcms2'].cmsPipelineEval16
    cmsPipelineEval16.argtypes = [POINTER(cmsUInt16Number), POINTER(cmsUInt16Number), POINTER(cmsPipeline)]
    cmsPipelineEval16.restype = None

# /usr/include/lcms2.h: 1202
if hasattr(_libs['lcms2'], 'cmsPipelineEvalFloat'):
    cmsPipelineEvalFloat = _libs['lcms2'].cmsPipelineEvalFloat
    cmsPipelineEvalFloat.argtypes = [POINTER(cmsFloat32Number), POINTER(cmsFloat32Number), POINTER(cmsPipeline)]
    cmsPipelineEvalFloat.restype = None

# /usr/include/lcms2.h: 1203
if hasattr(_libs['lcms2'], 'cmsPipelineEvalReverseFloat'):
    cmsPipelineEvalReverseFloat = _libs['lcms2'].cmsPipelineEvalReverseFloat
    cmsPipelineEvalReverseFloat.argtypes = [POINTER(cmsFloat32Number), POINTER(cmsFloat32Number), POINTER(cmsFloat32Number), POINTER(cmsPipeline)]
    cmsPipelineEvalReverseFloat.restype = cmsBool

# /usr/include/lcms2.h: 1204
if hasattr(_libs['lcms2'], 'cmsPipelineCat'):
    cmsPipelineCat = _libs['lcms2'].cmsPipelineCat
    cmsPipelineCat.argtypes = [POINTER(cmsPipeline), POINTER(cmsPipeline)]
    cmsPipelineCat.restype = cmsBool

# /usr/include/lcms2.h: 1205
if hasattr(_libs['lcms2'], 'cmsPipelineSetSaveAs8bitsFlag'):
    cmsPipelineSetSaveAs8bitsFlag = _libs['lcms2'].cmsPipelineSetSaveAs8bitsFlag
    cmsPipelineSetSaveAs8bitsFlag.argtypes = [POINTER(cmsPipeline), cmsBool]
    cmsPipelineSetSaveAs8bitsFlag.restype = cmsBool

enum_anon_33 = c_int # /usr/include/lcms2.h: 1208

cmsAT_BEGIN = 0 # /usr/include/lcms2.h: 1208

cmsAT_END = (cmsAT_BEGIN + 1) # /usr/include/lcms2.h: 1208

cmsStageLoc = enum_anon_33 # /usr/include/lcms2.h: 1208

# /usr/include/lcms2.h: 1210
if hasattr(_libs['lcms2'], 'cmsPipelineInsertStage'):
    cmsPipelineInsertStage = _libs['lcms2'].cmsPipelineInsertStage
    cmsPipelineInsertStage.argtypes = [POINTER(cmsPipeline), cmsStageLoc, POINTER(cmsStage)]
    cmsPipelineInsertStage.restype = c_int

# /usr/include/lcms2.h: 1211
if hasattr(_libs['lcms2'], 'cmsPipelineUnlinkStage'):
    cmsPipelineUnlinkStage = _libs['lcms2'].cmsPipelineUnlinkStage
    cmsPipelineUnlinkStage.argtypes = [POINTER(cmsPipeline), cmsStageLoc, POINTER(POINTER(cmsStage))]
    cmsPipelineUnlinkStage.restype = None

# /usr/include/lcms2.h: 1218
if hasattr(_libs['lcms2'], 'cmsPipelineCheckAndRetreiveStages'):
    _func = _libs['lcms2'].cmsPipelineCheckAndRetreiveStages
    _restype = cmsBool
    _errcheck = None
    _argtypes = [POINTER(cmsPipeline), cmsUInt32Number]
    cmsPipelineCheckAndRetreiveStages = _variadic_function(_func,_restype,_argtypes,_errcheck)

# /usr/include/lcms2.h: 1222
if hasattr(_libs['lcms2'], 'cmsStageAllocIdentity'):
    cmsStageAllocIdentity = _libs['lcms2'].cmsStageAllocIdentity
    cmsStageAllocIdentity.argtypes = [cmsContext, cmsUInt32Number]
    cmsStageAllocIdentity.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1223
if hasattr(_libs['lcms2'], 'cmsStageAllocToneCurves'):
    cmsStageAllocToneCurves = _libs['lcms2'].cmsStageAllocToneCurves
    cmsStageAllocToneCurves.argtypes = [cmsContext, cmsUInt32Number, POINTER(POINTER(cmsToneCurve))]
    cmsStageAllocToneCurves.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1224
if hasattr(_libs['lcms2'], 'cmsStageAllocMatrix'):
    cmsStageAllocMatrix = _libs['lcms2'].cmsStageAllocMatrix
    cmsStageAllocMatrix.argtypes = [cmsContext, cmsUInt32Number, cmsUInt32Number, POINTER(cmsFloat64Number), POINTER(cmsFloat64Number)]
    cmsStageAllocMatrix.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1226
if hasattr(_libs['lcms2'], 'cmsStageAllocCLut16bit'):
    cmsStageAllocCLut16bit = _libs['lcms2'].cmsStageAllocCLut16bit
    cmsStageAllocCLut16bit.argtypes = [cmsContext, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, POINTER(cmsUInt16Number)]
    cmsStageAllocCLut16bit.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1227
if hasattr(_libs['lcms2'], 'cmsStageAllocCLutFloat'):
    cmsStageAllocCLutFloat = _libs['lcms2'].cmsStageAllocCLutFloat
    cmsStageAllocCLutFloat.argtypes = [cmsContext, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, POINTER(cmsFloat32Number)]
    cmsStageAllocCLutFloat.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1229
if hasattr(_libs['lcms2'], 'cmsStageAllocCLut16bitGranular'):
    cmsStageAllocCLut16bitGranular = _libs['lcms2'].cmsStageAllocCLut16bitGranular
    cmsStageAllocCLut16bitGranular.argtypes = [cmsContext, POINTER(cmsUInt32Number), cmsUInt32Number, cmsUInt32Number, POINTER(cmsUInt16Number)]
    cmsStageAllocCLut16bitGranular.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1230
if hasattr(_libs['lcms2'], 'cmsStageAllocCLutFloatGranular'):
    cmsStageAllocCLutFloatGranular = _libs['lcms2'].cmsStageAllocCLutFloatGranular
    cmsStageAllocCLutFloatGranular.argtypes = [cmsContext, POINTER(cmsUInt32Number), cmsUInt32Number, cmsUInt32Number, POINTER(cmsFloat32Number)]
    cmsStageAllocCLutFloatGranular.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1232
if hasattr(_libs['lcms2'], 'cmsStageDup'):
    cmsStageDup = _libs['lcms2'].cmsStageDup
    cmsStageDup.argtypes = [POINTER(cmsStage)]
    cmsStageDup.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1233
if hasattr(_libs['lcms2'], 'cmsStageFree'):
    cmsStageFree = _libs['lcms2'].cmsStageFree
    cmsStageFree.argtypes = [POINTER(cmsStage)]
    cmsStageFree.restype = None

# /usr/include/lcms2.h: 1234
if hasattr(_libs['lcms2'], 'cmsStageNext'):
    cmsStageNext = _libs['lcms2'].cmsStageNext
    cmsStageNext.argtypes = [POINTER(cmsStage)]
    cmsStageNext.restype = POINTER(cmsStage)

# /usr/include/lcms2.h: 1236
if hasattr(_libs['lcms2'], 'cmsStageInputChannels'):
    cmsStageInputChannels = _libs['lcms2'].cmsStageInputChannels
    cmsStageInputChannels.argtypes = [POINTER(cmsStage)]
    cmsStageInputChannels.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1237
if hasattr(_libs['lcms2'], 'cmsStageOutputChannels'):
    cmsStageOutputChannels = _libs['lcms2'].cmsStageOutputChannels
    cmsStageOutputChannels.argtypes = [POINTER(cmsStage)]
    cmsStageOutputChannels.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1238
if hasattr(_libs['lcms2'], 'cmsStageType'):
    cmsStageType = _libs['lcms2'].cmsStageType
    cmsStageType.argtypes = [POINTER(cmsStage)]
    cmsStageType.restype = cmsStageSignature

# /usr/include/lcms2.h: 1239
if hasattr(_libs['lcms2'], 'cmsStageData'):
    cmsStageData = _libs['lcms2'].cmsStageData
    cmsStageData.argtypes = [POINTER(cmsStage)]
    cmsStageData.restype = POINTER(c_ubyte)
    cmsStageData.errcheck = lambda v,*a : cast(v, c_void_p)

cmsSAMPLER16 = CFUNCTYPE(UNCHECKED(cmsInt32Number), POINTER(cmsUInt16Number), POINTER(cmsUInt16Number), POINTER(None)) # /usr/include/lcms2.h: 1242

cmsSAMPLERFLOAT = CFUNCTYPE(UNCHECKED(cmsInt32Number), POINTER(cmsFloat32Number), POINTER(cmsFloat32Number), POINTER(None)) # /usr/include/lcms2.h: 1246

# /usr/include/lcms2.h: 1254
if hasattr(_libs['lcms2'], 'cmsStageSampleCLut16bit'):
    cmsStageSampleCLut16bit = _libs['lcms2'].cmsStageSampleCLut16bit
    cmsStageSampleCLut16bit.argtypes = [POINTER(cmsStage), cmsSAMPLER16, POINTER(None), cmsUInt32Number]
    cmsStageSampleCLut16bit.restype = cmsBool

# /usr/include/lcms2.h: 1255
if hasattr(_libs['lcms2'], 'cmsStageSampleCLutFloat'):
    cmsStageSampleCLutFloat = _libs['lcms2'].cmsStageSampleCLutFloat
    cmsStageSampleCLutFloat.argtypes = [POINTER(cmsStage), cmsSAMPLERFLOAT, POINTER(None), cmsUInt32Number]
    cmsStageSampleCLutFloat.restype = cmsBool

# /usr/include/lcms2.h: 1258
if hasattr(_libs['lcms2'], 'cmsSliceSpace16'):
    cmsSliceSpace16 = _libs['lcms2'].cmsSliceSpace16
    cmsSliceSpace16.argtypes = [cmsUInt32Number, POINTER(cmsUInt32Number), cmsSAMPLER16, POINTER(None)]
    cmsSliceSpace16.restype = cmsBool

# /usr/include/lcms2.h: 1261
if hasattr(_libs['lcms2'], 'cmsSliceSpaceFloat'):
    cmsSliceSpaceFloat = _libs['lcms2'].cmsSliceSpaceFloat
    cmsSliceSpaceFloat.argtypes = [cmsUInt32Number, POINTER(cmsUInt32Number), cmsSAMPLERFLOAT, POINTER(None)]
    cmsSliceSpaceFloat.restype = cmsBool

# /usr/include/lcms2.h: 1266
class struct__cms_MLU_struct(Structure):
    pass

cmsMLU = struct__cms_MLU_struct # /usr/include/lcms2.h: 1266

# /usr/include/lcms2.h: 1271
if hasattr(_libs['lcms2'], 'cmsMLUalloc'):
    cmsMLUalloc = _libs['lcms2'].cmsMLUalloc
    cmsMLUalloc.argtypes = [cmsContext, cmsUInt32Number]
    cmsMLUalloc.restype = POINTER(cmsMLU)

# /usr/include/lcms2.h: 1272
if hasattr(_libs['lcms2'], 'cmsMLUfree'):
    cmsMLUfree = _libs['lcms2'].cmsMLUfree
    cmsMLUfree.argtypes = [POINTER(cmsMLU)]
    cmsMLUfree.restype = None

# /usr/include/lcms2.h: 1273
if hasattr(_libs['lcms2'], 'cmsMLUdup'):
    cmsMLUdup = _libs['lcms2'].cmsMLUdup
    cmsMLUdup.argtypes = [POINTER(cmsMLU)]
    cmsMLUdup.restype = POINTER(cmsMLU)

# /usr/include/lcms2.h: 1275
if hasattr(_libs['lcms2'], 'cmsMLUsetASCII'):
    cmsMLUsetASCII = _libs['lcms2'].cmsMLUsetASCII
    cmsMLUsetASCII.argtypes = [POINTER(cmsMLU), c_char * 3, c_char * 3, String]
    cmsMLUsetASCII.restype = cmsBool

# /usr/include/lcms2.h: 1278
if hasattr(_libs['lcms2'], 'cmsMLUsetWide'):
    cmsMLUsetWide = _libs['lcms2'].cmsMLUsetWide
    cmsMLUsetWide.argtypes = [POINTER(cmsMLU), c_char * 3, c_char * 3, POINTER(c_wchar)]
    cmsMLUsetWide.restype = cmsBool

# /usr/include/lcms2.h: 1282
if hasattr(_libs['lcms2'], 'cmsMLUgetASCII'):
    cmsMLUgetASCII = _libs['lcms2'].cmsMLUgetASCII
    cmsMLUgetASCII.argtypes = [POINTER(cmsMLU), c_char * 3, c_char * 3, String, cmsUInt32Number]
    cmsMLUgetASCII.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1286
if hasattr(_libs['lcms2'], 'cmsMLUgetWide'):
    cmsMLUgetWide = _libs['lcms2'].cmsMLUgetWide
    cmsMLUgetWide.argtypes = [POINTER(cmsMLU), c_char * 3, c_char * 3, POINTER(c_wchar), cmsUInt32Number]
    cmsMLUgetWide.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1290
if hasattr(_libs['lcms2'], 'cmsMLUgetTranslation'):
    cmsMLUgetTranslation = _libs['lcms2'].cmsMLUgetTranslation
    cmsMLUgetTranslation.argtypes = [POINTER(cmsMLU), c_char * 3, c_char * 3, c_char * 3, c_char * 3]
    cmsMLUgetTranslation.restype = cmsBool

# /usr/include/lcms2.h: 1294
if hasattr(_libs['lcms2'], 'cmsMLUtranslationsCount'):
    cmsMLUtranslationsCount = _libs['lcms2'].cmsMLUtranslationsCount
    cmsMLUtranslationsCount.argtypes = [POINTER(cmsMLU)]
    cmsMLUtranslationsCount.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1296
if hasattr(_libs['lcms2'], 'cmsMLUtranslationsCodes'):
    cmsMLUtranslationsCodes = _libs['lcms2'].cmsMLUtranslationsCodes
    cmsMLUtranslationsCodes.argtypes = [POINTER(cmsMLU), cmsUInt32Number, c_char * 3, c_char * 3]
    cmsMLUtranslationsCodes.restype = cmsBool

# /usr/include/lcms2.h: 1308
class struct_anon_34(Structure):
    pass

struct_anon_34.__slots__ = [
    'Ucr',
    'Bg',
    'Desc',
]
struct_anon_34._fields_ = [
    ('Ucr', POINTER(cmsToneCurve)),
    ('Bg', POINTER(cmsToneCurve)),
    ('Desc', POINTER(cmsMLU)),
]

cmsUcrBg = struct_anon_34 # /usr/include/lcms2.h: 1308

# /usr/include/lcms2.h: 1330
class struct_anon_35(Structure):
    pass

struct_anon_35.__slots__ = [
    'Frequency',
    'ScreenAngle',
    'SpotShape',
]
struct_anon_35._fields_ = [
    ('Frequency', cmsFloat64Number),
    ('ScreenAngle', cmsFloat64Number),
    ('SpotShape', cmsUInt32Number),
]

cmsScreeningChannel = struct_anon_35 # /usr/include/lcms2.h: 1330

# /usr/include/lcms2.h: 1337
class struct_anon_36(Structure):
    pass

struct_anon_36.__slots__ = [
    'Flag',
    'nChannels',
    'Channels',
]
struct_anon_36._fields_ = [
    ('Flag', cmsUInt32Number),
    ('nChannels', cmsUInt32Number),
    ('Channels', cmsScreeningChannel * 16),
]

cmsScreening = struct_anon_36 # /usr/include/lcms2.h: 1337

# /usr/include/lcms2.h: 1342
class struct__cms_NAMEDCOLORLIST_struct(Structure):
    pass

cmsNAMEDCOLORLIST = struct__cms_NAMEDCOLORLIST_struct # /usr/include/lcms2.h: 1342

# /usr/include/lcms2.h: 1344
if hasattr(_libs['lcms2'], 'cmsAllocNamedColorList'):
    cmsAllocNamedColorList = _libs['lcms2'].cmsAllocNamedColorList
    cmsAllocNamedColorList.argtypes = [cmsContext, cmsUInt32Number, cmsUInt32Number, String, String]
    cmsAllocNamedColorList.restype = POINTER(cmsNAMEDCOLORLIST)

# /usr/include/lcms2.h: 1349
if hasattr(_libs['lcms2'], 'cmsFreeNamedColorList'):
    cmsFreeNamedColorList = _libs['lcms2'].cmsFreeNamedColorList
    cmsFreeNamedColorList.argtypes = [POINTER(cmsNAMEDCOLORLIST)]
    cmsFreeNamedColorList.restype = None

# /usr/include/lcms2.h: 1350
if hasattr(_libs['lcms2'], 'cmsDupNamedColorList'):
    cmsDupNamedColorList = _libs['lcms2'].cmsDupNamedColorList
    cmsDupNamedColorList.argtypes = [POINTER(cmsNAMEDCOLORLIST)]
    cmsDupNamedColorList.restype = POINTER(cmsNAMEDCOLORLIST)

# /usr/include/lcms2.h: 1351
if hasattr(_libs['lcms2'], 'cmsAppendNamedColor'):
    cmsAppendNamedColor = _libs['lcms2'].cmsAppendNamedColor
    cmsAppendNamedColor.argtypes = [POINTER(cmsNAMEDCOLORLIST), String, cmsUInt16Number * 3, cmsUInt16Number * 16]
    cmsAppendNamedColor.restype = cmsBool

# /usr/include/lcms2.h: 1355
if hasattr(_libs['lcms2'], 'cmsNamedColorCount'):
    cmsNamedColorCount = _libs['lcms2'].cmsNamedColorCount
    cmsNamedColorCount.argtypes = [POINTER(cmsNAMEDCOLORLIST)]
    cmsNamedColorCount.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1356
if hasattr(_libs['lcms2'], 'cmsNamedColorIndex'):
    cmsNamedColorIndex = _libs['lcms2'].cmsNamedColorIndex
    cmsNamedColorIndex.argtypes = [POINTER(cmsNAMEDCOLORLIST), String]
    cmsNamedColorIndex.restype = cmsInt32Number

# /usr/include/lcms2.h: 1358
if hasattr(_libs['lcms2'], 'cmsNamedColorInfo'):
    cmsNamedColorInfo = _libs['lcms2'].cmsNamedColorInfo
    cmsNamedColorInfo.argtypes = [POINTER(cmsNAMEDCOLORLIST), cmsUInt32Number, String, String, String, POINTER(cmsUInt16Number), POINTER(cmsUInt16Number)]
    cmsNamedColorInfo.restype = cmsBool

# /usr/include/lcms2.h: 1366
if hasattr(_libs['lcms2'], 'cmsGetNamedColorList'):
    cmsGetNamedColorList = _libs['lcms2'].cmsGetNamedColorList
    cmsGetNamedColorList.argtypes = [cmsHTRANSFORM]
    cmsGetNamedColorList.restype = POINTER(cmsNAMEDCOLORLIST)

# /usr/include/lcms2.h: 1383
class struct_anon_37(Structure):
    pass

struct_anon_37.__slots__ = [
    'deviceMfg',
    'deviceModel',
    'attributes',
    'technology',
    'ProfileID',
    'Manufacturer',
    'Model',
    'Description',
]
struct_anon_37._fields_ = [
    ('deviceMfg', cmsSignature),
    ('deviceModel', cmsSignature),
    ('attributes', cmsUInt64Number),
    ('technology', cmsTechnologySignature),
    ('ProfileID', cmsProfileID),
    ('Manufacturer', POINTER(cmsMLU)),
    ('Model', POINTER(cmsMLU)),
    ('Description', POINTER(cmsMLU)),
]

cmsPSEQDESC = struct_anon_37 # /usr/include/lcms2.h: 1383

# /usr/include/lcms2.h: 1391
class struct_anon_38(Structure):
    pass

struct_anon_38.__slots__ = [
    'n',
    'ContextID',
    'seq',
]
struct_anon_38._fields_ = [
    ('n', cmsUInt32Number),
    ('ContextID', cmsContext),
    ('seq', POINTER(cmsPSEQDESC)),
]

cmsSEQ = struct_anon_38 # /usr/include/lcms2.h: 1391

# /usr/include/lcms2.h: 1393
if hasattr(_libs['lcms2'], 'cmsAllocProfileSequenceDescription'):
    cmsAllocProfileSequenceDescription = _libs['lcms2'].cmsAllocProfileSequenceDescription
    cmsAllocProfileSequenceDescription.argtypes = [cmsContext, cmsUInt32Number]
    cmsAllocProfileSequenceDescription.restype = POINTER(cmsSEQ)

# /usr/include/lcms2.h: 1394
if hasattr(_libs['lcms2'], 'cmsDupProfileSequenceDescription'):
    cmsDupProfileSequenceDescription = _libs['lcms2'].cmsDupProfileSequenceDescription
    cmsDupProfileSequenceDescription.argtypes = [POINTER(cmsSEQ)]
    cmsDupProfileSequenceDescription.restype = POINTER(cmsSEQ)

# /usr/include/lcms2.h: 1395
if hasattr(_libs['lcms2'], 'cmsFreeProfileSequenceDescription'):
    cmsFreeProfileSequenceDescription = _libs['lcms2'].cmsFreeProfileSequenceDescription
    cmsFreeProfileSequenceDescription.argtypes = [POINTER(cmsSEQ)]
    cmsFreeProfileSequenceDescription.restype = None

# /usr/include/lcms2.h: 1399
class struct__cmsDICTentry_struct(Structure):
    pass

struct__cmsDICTentry_struct.__slots__ = [
    'Next',
    'DisplayName',
    'DisplayValue',
    'Name',
    'Value',
]
struct__cmsDICTentry_struct._fields_ = [
    ('Next', POINTER(struct__cmsDICTentry_struct)),
    ('DisplayName', POINTER(cmsMLU)),
    ('DisplayValue', POINTER(cmsMLU)),
    ('Name', POINTER(c_wchar)),
    ('Value', POINTER(c_wchar)),
]

cmsDICTentry = struct__cmsDICTentry_struct # /usr/include/lcms2.h: 1408

# /usr/include/lcms2.h: 1410
if hasattr(_libs['lcms2'], 'cmsDictAlloc'):
    cmsDictAlloc = _libs['lcms2'].cmsDictAlloc
    cmsDictAlloc.argtypes = [cmsContext]
    cmsDictAlloc.restype = cmsHANDLE

# /usr/include/lcms2.h: 1411
if hasattr(_libs['lcms2'], 'cmsDictFree'):
    cmsDictFree = _libs['lcms2'].cmsDictFree
    cmsDictFree.argtypes = [cmsHANDLE]
    cmsDictFree.restype = None

# /usr/include/lcms2.h: 1412
if hasattr(_libs['lcms2'], 'cmsDictDup'):
    cmsDictDup = _libs['lcms2'].cmsDictDup
    cmsDictDup.argtypes = [cmsHANDLE]
    cmsDictDup.restype = cmsHANDLE

# /usr/include/lcms2.h: 1414
if hasattr(_libs['lcms2'], 'cmsDictAddEntry'):
    cmsDictAddEntry = _libs['lcms2'].cmsDictAddEntry
    cmsDictAddEntry.argtypes = [cmsHANDLE, POINTER(c_wchar), POINTER(c_wchar), POINTER(cmsMLU), POINTER(cmsMLU)]
    cmsDictAddEntry.restype = cmsBool

# /usr/include/lcms2.h: 1415
if hasattr(_libs['lcms2'], 'cmsDictGetEntryList'):
    cmsDictGetEntryList = _libs['lcms2'].cmsDictGetEntryList
    cmsDictGetEntryList.argtypes = [cmsHANDLE]
    cmsDictGetEntryList.restype = POINTER(cmsDICTentry)

# /usr/include/lcms2.h: 1416
if hasattr(_libs['lcms2'], 'cmsDictNextEntry'):
    cmsDictNextEntry = _libs['lcms2'].cmsDictNextEntry
    cmsDictNextEntry.argtypes = [POINTER(cmsDICTentry)]
    cmsDictNextEntry.restype = POINTER(cmsDICTentry)

# /usr/include/lcms2.h: 1419
if hasattr(_libs['lcms2'], 'cmsCreateProfilePlaceholder'):
    cmsCreateProfilePlaceholder = _libs['lcms2'].cmsCreateProfilePlaceholder
    cmsCreateProfilePlaceholder.argtypes = [cmsContext]
    cmsCreateProfilePlaceholder.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1421
if hasattr(_libs['lcms2'], 'cmsGetProfileContextID'):
    cmsGetProfileContextID = _libs['lcms2'].cmsGetProfileContextID
    cmsGetProfileContextID.argtypes = [cmsHPROFILE]
    cmsGetProfileContextID.restype = cmsContext

# /usr/include/lcms2.h: 1422
if hasattr(_libs['lcms2'], 'cmsGetTagCount'):
    cmsGetTagCount = _libs['lcms2'].cmsGetTagCount
    cmsGetTagCount.argtypes = [cmsHPROFILE]
    cmsGetTagCount.restype = cmsInt32Number

# /usr/include/lcms2.h: 1423
if hasattr(_libs['lcms2'], 'cmsGetTagSignature'):
    cmsGetTagSignature = _libs['lcms2'].cmsGetTagSignature
    cmsGetTagSignature.argtypes = [cmsHPROFILE, cmsUInt32Number]
    cmsGetTagSignature.restype = cmsTagSignature

# /usr/include/lcms2.h: 1424
if hasattr(_libs['lcms2'], 'cmsIsTag'):
    cmsIsTag = _libs['lcms2'].cmsIsTag
    cmsIsTag.argtypes = [cmsHPROFILE, cmsTagSignature]
    cmsIsTag.restype = cmsBool

# /usr/include/lcms2.h: 1427
if hasattr(_libs['lcms2'], 'cmsReadTag'):
    cmsReadTag = _libs['lcms2'].cmsReadTag
    cmsReadTag.argtypes = [cmsHPROFILE, cmsTagSignature]
    cmsReadTag.restype = POINTER(c_ubyte)
    cmsReadTag.errcheck = lambda v,*a : cast(v, c_void_p)

# /usr/include/lcms2.h: 1428
if hasattr(_libs['lcms2'], 'cmsWriteTag'):
    cmsWriteTag = _libs['lcms2'].cmsWriteTag
    cmsWriteTag.argtypes = [cmsHPROFILE, cmsTagSignature, POINTER(None)]
    cmsWriteTag.restype = cmsBool

# /usr/include/lcms2.h: 1429
if hasattr(_libs['lcms2'], 'cmsLinkTag'):
    cmsLinkTag = _libs['lcms2'].cmsLinkTag
    cmsLinkTag.argtypes = [cmsHPROFILE, cmsTagSignature, cmsTagSignature]
    cmsLinkTag.restype = cmsBool

# /usr/include/lcms2.h: 1430
if hasattr(_libs['lcms2'], 'cmsTagLinkedTo'):
    cmsTagLinkedTo = _libs['lcms2'].cmsTagLinkedTo
    cmsTagLinkedTo.argtypes = [cmsHPROFILE, cmsTagSignature]
    cmsTagLinkedTo.restype = cmsTagSignature

# /usr/include/lcms2.h: 1433
if hasattr(_libs['lcms2'], 'cmsReadRawTag'):
    cmsReadRawTag = _libs['lcms2'].cmsReadRawTag
    cmsReadRawTag.argtypes = [cmsHPROFILE, cmsTagSignature, POINTER(None), cmsUInt32Number]
    cmsReadRawTag.restype = cmsInt32Number

# /usr/include/lcms2.h: 1434
if hasattr(_libs['lcms2'], 'cmsWriteRawTag'):
    cmsWriteRawTag = _libs['lcms2'].cmsWriteRawTag
    cmsWriteRawTag.argtypes = [cmsHPROFILE, cmsTagSignature, POINTER(None), cmsUInt32Number]
    cmsWriteRawTag.restype = cmsBool

# /usr/include/lcms2.h: 1442
if hasattr(_libs['lcms2'], 'cmsGetHeaderFlags'):
    cmsGetHeaderFlags = _libs['lcms2'].cmsGetHeaderFlags
    cmsGetHeaderFlags.argtypes = [cmsHPROFILE]
    cmsGetHeaderFlags.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1443
if hasattr(_libs['lcms2'], 'cmsGetHeaderAttributes'):
    cmsGetHeaderAttributes = _libs['lcms2'].cmsGetHeaderAttributes
    cmsGetHeaderAttributes.argtypes = [cmsHPROFILE, POINTER(cmsUInt64Number)]
    cmsGetHeaderAttributes.restype = None

# /usr/include/lcms2.h: 1444
if hasattr(_libs['lcms2'], 'cmsGetHeaderProfileID'):
    cmsGetHeaderProfileID = _libs['lcms2'].cmsGetHeaderProfileID
    cmsGetHeaderProfileID.argtypes = [cmsHPROFILE, POINTER(cmsUInt8Number)]
    cmsGetHeaderProfileID.restype = None

# /usr/include/lcms2.h: 1445
if hasattr(_libs['lcms2'], 'cmsGetHeaderCreationDateTime'):
    cmsGetHeaderCreationDateTime = _libs['lcms2'].cmsGetHeaderCreationDateTime
    cmsGetHeaderCreationDateTime.argtypes = [cmsHPROFILE, POINTER(struct_tm)]
    cmsGetHeaderCreationDateTime.restype = cmsBool

# /usr/include/lcms2.h: 1446
if hasattr(_libs['lcms2'], 'cmsGetHeaderRenderingIntent'):
    cmsGetHeaderRenderingIntent = _libs['lcms2'].cmsGetHeaderRenderingIntent
    cmsGetHeaderRenderingIntent.argtypes = [cmsHPROFILE]
    cmsGetHeaderRenderingIntent.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1448
if hasattr(_libs['lcms2'], 'cmsSetHeaderFlags'):
    cmsSetHeaderFlags = _libs['lcms2'].cmsSetHeaderFlags
    cmsSetHeaderFlags.argtypes = [cmsHPROFILE, cmsUInt32Number]
    cmsSetHeaderFlags.restype = None

# /usr/include/lcms2.h: 1449
if hasattr(_libs['lcms2'], 'cmsGetHeaderManufacturer'):
    cmsGetHeaderManufacturer = _libs['lcms2'].cmsGetHeaderManufacturer
    cmsGetHeaderManufacturer.argtypes = [cmsHPROFILE]
    cmsGetHeaderManufacturer.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1450
if hasattr(_libs['lcms2'], 'cmsSetHeaderManufacturer'):
    cmsSetHeaderManufacturer = _libs['lcms2'].cmsSetHeaderManufacturer
    cmsSetHeaderManufacturer.argtypes = [cmsHPROFILE, cmsUInt32Number]
    cmsSetHeaderManufacturer.restype = None

# /usr/include/lcms2.h: 1451
if hasattr(_libs['lcms2'], 'cmsGetHeaderCreator'):
    cmsGetHeaderCreator = _libs['lcms2'].cmsGetHeaderCreator
    cmsGetHeaderCreator.argtypes = [cmsHPROFILE]
    cmsGetHeaderCreator.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1452
if hasattr(_libs['lcms2'], 'cmsGetHeaderModel'):
    cmsGetHeaderModel = _libs['lcms2'].cmsGetHeaderModel
    cmsGetHeaderModel.argtypes = [cmsHPROFILE]
    cmsGetHeaderModel.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1453
if hasattr(_libs['lcms2'], 'cmsSetHeaderModel'):
    cmsSetHeaderModel = _libs['lcms2'].cmsSetHeaderModel
    cmsSetHeaderModel.argtypes = [cmsHPROFILE, cmsUInt32Number]
    cmsSetHeaderModel.restype = None

# /usr/include/lcms2.h: 1454
if hasattr(_libs['lcms2'], 'cmsSetHeaderAttributes'):
    cmsSetHeaderAttributes = _libs['lcms2'].cmsSetHeaderAttributes
    cmsSetHeaderAttributes.argtypes = [cmsHPROFILE, cmsUInt64Number]
    cmsSetHeaderAttributes.restype = None

# /usr/include/lcms2.h: 1455
if hasattr(_libs['lcms2'], 'cmsSetHeaderProfileID'):
    cmsSetHeaderProfileID = _libs['lcms2'].cmsSetHeaderProfileID
    cmsSetHeaderProfileID.argtypes = [cmsHPROFILE, POINTER(cmsUInt8Number)]
    cmsSetHeaderProfileID.restype = None

# /usr/include/lcms2.h: 1456
if hasattr(_libs['lcms2'], 'cmsSetHeaderRenderingIntent'):
    cmsSetHeaderRenderingIntent = _libs['lcms2'].cmsSetHeaderRenderingIntent
    cmsSetHeaderRenderingIntent.argtypes = [cmsHPROFILE, cmsUInt32Number]
    cmsSetHeaderRenderingIntent.restype = None

# /usr/include/lcms2.h: 1459
if hasattr(_libs['lcms2'], 'cmsGetPCS'):
    cmsGetPCS = _libs['lcms2'].cmsGetPCS
    cmsGetPCS.argtypes = [cmsHPROFILE]
    cmsGetPCS.restype = cmsColorSpaceSignature

# /usr/include/lcms2.h: 1460
if hasattr(_libs['lcms2'], 'cmsSetPCS'):
    cmsSetPCS = _libs['lcms2'].cmsSetPCS
    cmsSetPCS.argtypes = [cmsHPROFILE, cmsColorSpaceSignature]
    cmsSetPCS.restype = None

# /usr/include/lcms2.h: 1462
if hasattr(_libs['lcms2'], 'cmsGetColorSpace'):
    cmsGetColorSpace = _libs['lcms2'].cmsGetColorSpace
    cmsGetColorSpace.argtypes = [cmsHPROFILE]
    cmsGetColorSpace.restype = cmsColorSpaceSignature

# /usr/include/lcms2.h: 1463
if hasattr(_libs['lcms2'], 'cmsSetColorSpace'):
    cmsSetColorSpace = _libs['lcms2'].cmsSetColorSpace
    cmsSetColorSpace.argtypes = [cmsHPROFILE, cmsColorSpaceSignature]
    cmsSetColorSpace.restype = None

# /usr/include/lcms2.h: 1465
if hasattr(_libs['lcms2'], 'cmsGetDeviceClass'):
    cmsGetDeviceClass = _libs['lcms2'].cmsGetDeviceClass
    cmsGetDeviceClass.argtypes = [cmsHPROFILE]
    cmsGetDeviceClass.restype = cmsProfileClassSignature

# /usr/include/lcms2.h: 1466
if hasattr(_libs['lcms2'], 'cmsSetDeviceClass'):
    cmsSetDeviceClass = _libs['lcms2'].cmsSetDeviceClass
    cmsSetDeviceClass.argtypes = [cmsHPROFILE, cmsProfileClassSignature]
    cmsSetDeviceClass.restype = None

# /usr/include/lcms2.h: 1467
if hasattr(_libs['lcms2'], 'cmsSetProfileVersion'):
    cmsSetProfileVersion = _libs['lcms2'].cmsSetProfileVersion
    cmsSetProfileVersion.argtypes = [cmsHPROFILE, cmsFloat64Number]
    cmsSetProfileVersion.restype = None

# /usr/include/lcms2.h: 1468
if hasattr(_libs['lcms2'], 'cmsGetProfileVersion'):
    cmsGetProfileVersion = _libs['lcms2'].cmsGetProfileVersion
    cmsGetProfileVersion.argtypes = [cmsHPROFILE]
    cmsGetProfileVersion.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1470
if hasattr(_libs['lcms2'], 'cmsGetEncodedICCversion'):
    cmsGetEncodedICCversion = _libs['lcms2'].cmsGetEncodedICCversion
    cmsGetEncodedICCversion.argtypes = [cmsHPROFILE]
    cmsGetEncodedICCversion.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1471
if hasattr(_libs['lcms2'], 'cmsSetEncodedICCversion'):
    cmsSetEncodedICCversion = _libs['lcms2'].cmsSetEncodedICCversion
    cmsSetEncodedICCversion.argtypes = [cmsHPROFILE, cmsUInt32Number]
    cmsSetEncodedICCversion.restype = None

# /usr/include/lcms2.h: 1478
if hasattr(_libs['lcms2'], 'cmsIsIntentSupported'):
    cmsIsIntentSupported = _libs['lcms2'].cmsIsIntentSupported
    cmsIsIntentSupported.argtypes = [cmsHPROFILE, cmsUInt32Number, cmsUInt32Number]
    cmsIsIntentSupported.restype = cmsBool

# /usr/include/lcms2.h: 1479
if hasattr(_libs['lcms2'], 'cmsIsMatrixShaper'):
    cmsIsMatrixShaper = _libs['lcms2'].cmsIsMatrixShaper
    cmsIsMatrixShaper.argtypes = [cmsHPROFILE]
    cmsIsMatrixShaper.restype = cmsBool

# /usr/include/lcms2.h: 1480
if hasattr(_libs['lcms2'], 'cmsIsCLUT'):
    cmsIsCLUT = _libs['lcms2'].cmsIsCLUT
    cmsIsCLUT.argtypes = [cmsHPROFILE, cmsUInt32Number, cmsUInt32Number]
    cmsIsCLUT.restype = cmsBool

# /usr/include/lcms2.h: 1483
if hasattr(_libs['lcms2'], '_cmsICCcolorSpace'):
    _cmsICCcolorSpace = _libs['lcms2']._cmsICCcolorSpace
    _cmsICCcolorSpace.argtypes = [c_int]
    _cmsICCcolorSpace.restype = cmsColorSpaceSignature

# /usr/include/lcms2.h: 1484
if hasattr(_libs['lcms2'], '_cmsLCMScolorSpace'):
    _cmsLCMScolorSpace = _libs['lcms2']._cmsLCMScolorSpace
    _cmsLCMScolorSpace.argtypes = [cmsColorSpaceSignature]
    _cmsLCMScolorSpace.restype = c_int

# /usr/include/lcms2.h: 1486
if hasattr(_libs['lcms2'], 'cmsChannelsOf'):
    cmsChannelsOf = _libs['lcms2'].cmsChannelsOf
    cmsChannelsOf.argtypes = [cmsColorSpaceSignature]
    cmsChannelsOf.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1489
if hasattr(_libs['lcms2'], 'cmsFormatterForColorspaceOfProfile'):
    cmsFormatterForColorspaceOfProfile = _libs['lcms2'].cmsFormatterForColorspaceOfProfile
    cmsFormatterForColorspaceOfProfile.argtypes = [cmsHPROFILE, cmsUInt32Number, cmsBool]
    cmsFormatterForColorspaceOfProfile.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1490
if hasattr(_libs['lcms2'], 'cmsFormatterForPCSOfProfile'):
    cmsFormatterForPCSOfProfile = _libs['lcms2'].cmsFormatterForPCSOfProfile
    cmsFormatterForPCSOfProfile.argtypes = [cmsHPROFILE, cmsUInt32Number, cmsBool]
    cmsFormatterForPCSOfProfile.restype = cmsUInt32Number

enum_anon_39 = c_int # /usr/include/lcms2.h: 1499

cmsInfoDescription = 0 # /usr/include/lcms2.h: 1499

cmsInfoManufacturer = 1 # /usr/include/lcms2.h: 1499

cmsInfoModel = 2 # /usr/include/lcms2.h: 1499

cmsInfoCopyright = 3 # /usr/include/lcms2.h: 1499

cmsInfoType = enum_anon_39 # /usr/include/lcms2.h: 1499

# /usr/include/lcms2.h: 1501
if hasattr(_libs['lcms2'], 'cmsGetProfileInfo'):
    cmsGetProfileInfo = _libs['lcms2'].cmsGetProfileInfo
    cmsGetProfileInfo.argtypes = [cmsHPROFILE, cmsInfoType, c_char * 3, c_char * 3, POINTER(c_wchar), cmsUInt32Number]
    cmsGetProfileInfo.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1505
if hasattr(_libs['lcms2'], 'cmsGetProfileInfoASCII'):
    cmsGetProfileInfoASCII = _libs['lcms2'].cmsGetProfileInfoASCII
    cmsGetProfileInfoASCII.argtypes = [cmsHPROFILE, cmsInfoType, c_char * 3, c_char * 3, String, cmsUInt32Number]
    cmsGetProfileInfoASCII.restype = cmsUInt32Number

# /usr/include/lcms2_plugin.h: 112
class struct__cms_io_handler(Structure):
    pass

cmsIOHANDLER = struct__cms_io_handler # /usr/include/lcms2.h: 1511

# /usr/include/lcms2.h: 1513
if hasattr(_libs['lcms2'], 'cmsOpenIOhandlerFromFile'):
    cmsOpenIOhandlerFromFile = _libs['lcms2'].cmsOpenIOhandlerFromFile
    cmsOpenIOhandlerFromFile.argtypes = [cmsContext, String, String]
    cmsOpenIOhandlerFromFile.restype = POINTER(cmsIOHANDLER)

# /usr/include/lcms2.h: 1514
if hasattr(_libs['lcms2'], 'cmsOpenIOhandlerFromStream'):
    cmsOpenIOhandlerFromStream = _libs['lcms2'].cmsOpenIOhandlerFromStream
    cmsOpenIOhandlerFromStream.argtypes = [cmsContext, POINTER(FILE)]
    cmsOpenIOhandlerFromStream.restype = POINTER(cmsIOHANDLER)

# /usr/include/lcms2.h: 1515
if hasattr(_libs['lcms2'], 'cmsOpenIOhandlerFromMem'):
    cmsOpenIOhandlerFromMem = _libs['lcms2'].cmsOpenIOhandlerFromMem
    cmsOpenIOhandlerFromMem.argtypes = [cmsContext, POINTER(None), cmsUInt32Number, String]
    cmsOpenIOhandlerFromMem.restype = POINTER(cmsIOHANDLER)

# /usr/include/lcms2.h: 1516
if hasattr(_libs['lcms2'], 'cmsOpenIOhandlerFromNULL'):
    cmsOpenIOhandlerFromNULL = _libs['lcms2'].cmsOpenIOhandlerFromNULL
    cmsOpenIOhandlerFromNULL.argtypes = [cmsContext]
    cmsOpenIOhandlerFromNULL.restype = POINTER(cmsIOHANDLER)

# /usr/include/lcms2.h: 1517
if hasattr(_libs['lcms2'], 'cmsGetProfileIOhandler'):
    cmsGetProfileIOhandler = _libs['lcms2'].cmsGetProfileIOhandler
    cmsGetProfileIOhandler.argtypes = [cmsHPROFILE]
    cmsGetProfileIOhandler.restype = POINTER(cmsIOHANDLER)

# /usr/include/lcms2.h: 1518
if hasattr(_libs['lcms2'], 'cmsCloseIOhandler'):
    cmsCloseIOhandler = _libs['lcms2'].cmsCloseIOhandler
    cmsCloseIOhandler.argtypes = [POINTER(cmsIOHANDLER)]
    cmsCloseIOhandler.restype = cmsBool

# /usr/include/lcms2.h: 1522
if hasattr(_libs['lcms2'], 'cmsMD5computeID'):
    cmsMD5computeID = _libs['lcms2'].cmsMD5computeID
    cmsMD5computeID.argtypes = [cmsHPROFILE]
    cmsMD5computeID.restype = cmsBool

# /usr/include/lcms2.h: 1526
if hasattr(_libs['lcms2'], 'cmsOpenProfileFromFile'):
    cmsOpenProfileFromFile = _libs['lcms2'].cmsOpenProfileFromFile
    cmsOpenProfileFromFile.argtypes = [String, String]
    cmsOpenProfileFromFile.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1527
if hasattr(_libs['lcms2'], 'cmsOpenProfileFromFileTHR'):
    cmsOpenProfileFromFileTHR = _libs['lcms2'].cmsOpenProfileFromFileTHR
    cmsOpenProfileFromFileTHR.argtypes = [cmsContext, String, String]
    cmsOpenProfileFromFileTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1528
if hasattr(_libs['lcms2'], 'cmsOpenProfileFromStream'):
    cmsOpenProfileFromStream = _libs['lcms2'].cmsOpenProfileFromStream
    cmsOpenProfileFromStream.argtypes = [POINTER(FILE), String]
    cmsOpenProfileFromStream.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1529
if hasattr(_libs['lcms2'], 'cmsOpenProfileFromStreamTHR'):
    cmsOpenProfileFromStreamTHR = _libs['lcms2'].cmsOpenProfileFromStreamTHR
    cmsOpenProfileFromStreamTHR.argtypes = [cmsContext, POINTER(FILE), String]
    cmsOpenProfileFromStreamTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1530
if hasattr(_libs['lcms2'], 'cmsOpenProfileFromMem'):
    cmsOpenProfileFromMem = _libs['lcms2'].cmsOpenProfileFromMem
    cmsOpenProfileFromMem.argtypes = [POINTER(None), cmsUInt32Number]
    cmsOpenProfileFromMem.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1531
if hasattr(_libs['lcms2'], 'cmsOpenProfileFromMemTHR'):
    cmsOpenProfileFromMemTHR = _libs['lcms2'].cmsOpenProfileFromMemTHR
    cmsOpenProfileFromMemTHR.argtypes = [cmsContext, POINTER(None), cmsUInt32Number]
    cmsOpenProfileFromMemTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1532
if hasattr(_libs['lcms2'], 'cmsOpenProfileFromIOhandlerTHR'):
    cmsOpenProfileFromIOhandlerTHR = _libs['lcms2'].cmsOpenProfileFromIOhandlerTHR
    cmsOpenProfileFromIOhandlerTHR.argtypes = [cmsContext, POINTER(cmsIOHANDLER)]
    cmsOpenProfileFromIOhandlerTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1533
if hasattr(_libs['lcms2'], 'cmsOpenProfileFromIOhandler2THR'):
    cmsOpenProfileFromIOhandler2THR = _libs['lcms2'].cmsOpenProfileFromIOhandler2THR
    cmsOpenProfileFromIOhandler2THR.argtypes = [cmsContext, POINTER(cmsIOHANDLER), cmsBool]
    cmsOpenProfileFromIOhandler2THR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1534
if hasattr(_libs['lcms2'], 'cmsCloseProfile'):
    cmsCloseProfile = _libs['lcms2'].cmsCloseProfile
    cmsCloseProfile.argtypes = [cmsHPROFILE]
    cmsCloseProfile.restype = cmsBool

# /usr/include/lcms2.h: 1536
if hasattr(_libs['lcms2'], 'cmsSaveProfileToFile'):
    cmsSaveProfileToFile = _libs['lcms2'].cmsSaveProfileToFile
    cmsSaveProfileToFile.argtypes = [cmsHPROFILE, String]
    cmsSaveProfileToFile.restype = cmsBool

# /usr/include/lcms2.h: 1537
if hasattr(_libs['lcms2'], 'cmsSaveProfileToStream'):
    cmsSaveProfileToStream = _libs['lcms2'].cmsSaveProfileToStream
    cmsSaveProfileToStream.argtypes = [cmsHPROFILE, POINTER(FILE)]
    cmsSaveProfileToStream.restype = cmsBool

# /usr/include/lcms2.h: 1538
if hasattr(_libs['lcms2'], 'cmsSaveProfileToMem'):
    cmsSaveProfileToMem = _libs['lcms2'].cmsSaveProfileToMem
    cmsSaveProfileToMem.argtypes = [cmsHPROFILE, POINTER(None), POINTER(cmsUInt32Number)]
    cmsSaveProfileToMem.restype = cmsBool

# /usr/include/lcms2.h: 1539
if hasattr(_libs['lcms2'], 'cmsSaveProfileToIOhandler'):
    cmsSaveProfileToIOhandler = _libs['lcms2'].cmsSaveProfileToIOhandler
    cmsSaveProfileToIOhandler.argtypes = [cmsHPROFILE, POINTER(cmsIOHANDLER)]
    cmsSaveProfileToIOhandler.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1543
if hasattr(_libs['lcms2'], 'cmsCreateRGBProfileTHR'):
    cmsCreateRGBProfileTHR = _libs['lcms2'].cmsCreateRGBProfileTHR
    cmsCreateRGBProfileTHR.argtypes = [cmsContext, POINTER(cmsCIExyY), POINTER(cmsCIExyYTRIPLE), POINTER(cmsToneCurve) * 3]
    cmsCreateRGBProfileTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1548
if hasattr(_libs['lcms2'], 'cmsCreateRGBProfile'):
    cmsCreateRGBProfile = _libs['lcms2'].cmsCreateRGBProfile
    cmsCreateRGBProfile.argtypes = [POINTER(cmsCIExyY), POINTER(cmsCIExyYTRIPLE), POINTER(cmsToneCurve) * 3]
    cmsCreateRGBProfile.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1552
if hasattr(_libs['lcms2'], 'cmsCreateGrayProfileTHR'):
    cmsCreateGrayProfileTHR = _libs['lcms2'].cmsCreateGrayProfileTHR
    cmsCreateGrayProfileTHR.argtypes = [cmsContext, POINTER(cmsCIExyY), POINTER(cmsToneCurve)]
    cmsCreateGrayProfileTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1556
if hasattr(_libs['lcms2'], 'cmsCreateGrayProfile'):
    cmsCreateGrayProfile = _libs['lcms2'].cmsCreateGrayProfile
    cmsCreateGrayProfile.argtypes = [POINTER(cmsCIExyY), POINTER(cmsToneCurve)]
    cmsCreateGrayProfile.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1559
if hasattr(_libs['lcms2'], 'cmsCreateLinearizationDeviceLinkTHR'):
    cmsCreateLinearizationDeviceLinkTHR = _libs['lcms2'].cmsCreateLinearizationDeviceLinkTHR
    cmsCreateLinearizationDeviceLinkTHR.argtypes = [cmsContext, cmsColorSpaceSignature, POINTER(POINTER(cmsToneCurve))]
    cmsCreateLinearizationDeviceLinkTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1563
if hasattr(_libs['lcms2'], 'cmsCreateLinearizationDeviceLink'):
    cmsCreateLinearizationDeviceLink = _libs['lcms2'].cmsCreateLinearizationDeviceLink
    cmsCreateLinearizationDeviceLink.argtypes = [cmsColorSpaceSignature, POINTER(POINTER(cmsToneCurve))]
    cmsCreateLinearizationDeviceLink.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1566
if hasattr(_libs['lcms2'], 'cmsCreateInkLimitingDeviceLinkTHR'):
    cmsCreateInkLimitingDeviceLinkTHR = _libs['lcms2'].cmsCreateInkLimitingDeviceLinkTHR
    cmsCreateInkLimitingDeviceLinkTHR.argtypes = [cmsContext, cmsColorSpaceSignature, cmsFloat64Number]
    cmsCreateInkLimitingDeviceLinkTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1569
if hasattr(_libs['lcms2'], 'cmsCreateInkLimitingDeviceLink'):
    cmsCreateInkLimitingDeviceLink = _libs['lcms2'].cmsCreateInkLimitingDeviceLink
    cmsCreateInkLimitingDeviceLink.argtypes = [cmsColorSpaceSignature, cmsFloat64Number]
    cmsCreateInkLimitingDeviceLink.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1572
if hasattr(_libs['lcms2'], 'cmsCreateLab2ProfileTHR'):
    cmsCreateLab2ProfileTHR = _libs['lcms2'].cmsCreateLab2ProfileTHR
    cmsCreateLab2ProfileTHR.argtypes = [cmsContext, POINTER(cmsCIExyY)]
    cmsCreateLab2ProfileTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1573
if hasattr(_libs['lcms2'], 'cmsCreateLab2Profile'):
    cmsCreateLab2Profile = _libs['lcms2'].cmsCreateLab2Profile
    cmsCreateLab2Profile.argtypes = [POINTER(cmsCIExyY)]
    cmsCreateLab2Profile.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1574
if hasattr(_libs['lcms2'], 'cmsCreateLab4ProfileTHR'):
    cmsCreateLab4ProfileTHR = _libs['lcms2'].cmsCreateLab4ProfileTHR
    cmsCreateLab4ProfileTHR.argtypes = [cmsContext, POINTER(cmsCIExyY)]
    cmsCreateLab4ProfileTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1575
if hasattr(_libs['lcms2'], 'cmsCreateLab4Profile'):
    cmsCreateLab4Profile = _libs['lcms2'].cmsCreateLab4Profile
    cmsCreateLab4Profile.argtypes = [POINTER(cmsCIExyY)]
    cmsCreateLab4Profile.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1577
if hasattr(_libs['lcms2'], 'cmsCreateXYZProfileTHR'):
    cmsCreateXYZProfileTHR = _libs['lcms2'].cmsCreateXYZProfileTHR
    cmsCreateXYZProfileTHR.argtypes = [cmsContext]
    cmsCreateXYZProfileTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1578
if hasattr(_libs['lcms2'], 'cmsCreateXYZProfile'):
    cmsCreateXYZProfile = _libs['lcms2'].cmsCreateXYZProfile
    cmsCreateXYZProfile.argtypes = []
    cmsCreateXYZProfile.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1580
if hasattr(_libs['lcms2'], 'cmsCreate_sRGBProfileTHR'):
    cmsCreate_sRGBProfileTHR = _libs['lcms2'].cmsCreate_sRGBProfileTHR
    cmsCreate_sRGBProfileTHR.argtypes = [cmsContext]
    cmsCreate_sRGBProfileTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1581
if hasattr(_libs['lcms2'], 'cmsCreate_sRGBProfile'):
    cmsCreate_sRGBProfile = _libs['lcms2'].cmsCreate_sRGBProfile
    cmsCreate_sRGBProfile.argtypes = []
    cmsCreate_sRGBProfile.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1583
if hasattr(_libs['lcms2'], 'cmsCreateBCHSWabstractProfileTHR'):
    cmsCreateBCHSWabstractProfileTHR = _libs['lcms2'].cmsCreateBCHSWabstractProfileTHR
    cmsCreateBCHSWabstractProfileTHR.argtypes = [cmsContext, c_int, cmsFloat64Number, cmsFloat64Number, cmsFloat64Number, cmsFloat64Number, c_int, c_int]
    cmsCreateBCHSWabstractProfileTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1592
if hasattr(_libs['lcms2'], 'cmsCreateBCHSWabstractProfile'):
    cmsCreateBCHSWabstractProfile = _libs['lcms2'].cmsCreateBCHSWabstractProfile
    cmsCreateBCHSWabstractProfile.argtypes = [c_int, cmsFloat64Number, cmsFloat64Number, cmsFloat64Number, cmsFloat64Number, c_int, c_int]
    cmsCreateBCHSWabstractProfile.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1600
if hasattr(_libs['lcms2'], 'cmsCreateNULLProfileTHR'):
    cmsCreateNULLProfileTHR = _libs['lcms2'].cmsCreateNULLProfileTHR
    cmsCreateNULLProfileTHR.argtypes = [cmsContext]
    cmsCreateNULLProfileTHR.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1601
if hasattr(_libs['lcms2'], 'cmsCreateNULLProfile'):
    cmsCreateNULLProfile = _libs['lcms2'].cmsCreateNULLProfile
    cmsCreateNULLProfile.argtypes = []
    cmsCreateNULLProfile.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1604
if hasattr(_libs['lcms2'], 'cmsTransform2DeviceLink'):
    cmsTransform2DeviceLink = _libs['lcms2'].cmsTransform2DeviceLink
    cmsTransform2DeviceLink.argtypes = [cmsHTRANSFORM, cmsFloat64Number, cmsUInt32Number]
    cmsTransform2DeviceLink.restype = cmsHPROFILE

# /usr/include/lcms2.h: 1623
if hasattr(_libs['lcms2'], 'cmsGetSupportedIntents'):
    cmsGetSupportedIntents = _libs['lcms2'].cmsGetSupportedIntents
    cmsGetSupportedIntents.argtypes = [cmsUInt32Number, POINTER(cmsUInt32Number), POINTER(POINTER(c_char))]
    cmsGetSupportedIntents.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1624
if hasattr(_libs['lcms2'], 'cmsGetSupportedIntentsTHR'):
    cmsGetSupportedIntentsTHR = _libs['lcms2'].cmsGetSupportedIntentsTHR
    cmsGetSupportedIntentsTHR.argtypes = [cmsContext, cmsUInt32Number, POINTER(cmsUInt32Number), POINTER(POINTER(c_char))]
    cmsGetSupportedIntentsTHR.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1666
if hasattr(_libs['lcms2'], 'cmsCreateTransformTHR'):
    cmsCreateTransformTHR = _libs['lcms2'].cmsCreateTransformTHR
    cmsCreateTransformTHR.argtypes = [cmsContext, cmsHPROFILE, cmsUInt32Number, cmsHPROFILE, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number]
    cmsCreateTransformTHR.restype = cmsHTRANSFORM

# /usr/include/lcms2.h: 1674
if hasattr(_libs['lcms2'], 'cmsCreateTransform'):
    cmsCreateTransform = _libs['lcms2'].cmsCreateTransform
    cmsCreateTransform.argtypes = [cmsHPROFILE, cmsUInt32Number, cmsHPROFILE, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number]
    cmsCreateTransform.restype = cmsHTRANSFORM

# /usr/include/lcms2.h: 1681
if hasattr(_libs['lcms2'], 'cmsCreateProofingTransformTHR'):
    cmsCreateProofingTransformTHR = _libs['lcms2'].cmsCreateProofingTransformTHR
    cmsCreateProofingTransformTHR.argtypes = [cmsContext, cmsHPROFILE, cmsUInt32Number, cmsHPROFILE, cmsUInt32Number, cmsHPROFILE, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number]
    cmsCreateProofingTransformTHR.restype = cmsHTRANSFORM

# /usr/include/lcms2.h: 1691
if hasattr(_libs['lcms2'], 'cmsCreateProofingTransform'):
    cmsCreateProofingTransform = _libs['lcms2'].cmsCreateProofingTransform
    cmsCreateProofingTransform.argtypes = [cmsHPROFILE, cmsUInt32Number, cmsHPROFILE, cmsUInt32Number, cmsHPROFILE, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number]
    cmsCreateProofingTransform.restype = cmsHTRANSFORM

# /usr/include/lcms2.h: 1700
if hasattr(_libs['lcms2'], 'cmsCreateMultiprofileTransformTHR'):
    cmsCreateMultiprofileTransformTHR = _libs['lcms2'].cmsCreateMultiprofileTransformTHR
    cmsCreateMultiprofileTransformTHR.argtypes = [cmsContext, POINTER(cmsHPROFILE), cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number]
    cmsCreateMultiprofileTransformTHR.restype = cmsHTRANSFORM

# /usr/include/lcms2.h: 1709
if hasattr(_libs['lcms2'], 'cmsCreateMultiprofileTransform'):
    cmsCreateMultiprofileTransform = _libs['lcms2'].cmsCreateMultiprofileTransform
    cmsCreateMultiprofileTransform.argtypes = [POINTER(cmsHPROFILE), cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number]
    cmsCreateMultiprofileTransform.restype = cmsHTRANSFORM

# /usr/include/lcms2.h: 1717
if hasattr(_libs['lcms2'], 'cmsCreateExtendedTransform'):
    cmsCreateExtendedTransform = _libs['lcms2'].cmsCreateExtendedTransform
    cmsCreateExtendedTransform.argtypes = [cmsContext, cmsUInt32Number, POINTER(cmsHPROFILE), POINTER(cmsBool), POINTER(cmsUInt32Number), POINTER(cmsFloat64Number), cmsHPROFILE, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number]
    cmsCreateExtendedTransform.restype = cmsHTRANSFORM

# /usr/include/lcms2.h: 1728
if hasattr(_libs['lcms2'], 'cmsDeleteTransform'):
    cmsDeleteTransform = _libs['lcms2'].cmsDeleteTransform
    cmsDeleteTransform.argtypes = [cmsHTRANSFORM]
    cmsDeleteTransform.restype = None

# /usr/include/lcms2.h: 1730
if hasattr(_libs['lcms2'], 'cmsDoTransform'):
    cmsDoTransform = _libs['lcms2'].cmsDoTransform
    cmsDoTransform.argtypes = [cmsHTRANSFORM, POINTER(None), POINTER(None), cmsUInt32Number]
    cmsDoTransform.restype = None

# /usr/include/lcms2.h: 1735
if hasattr(_libs['lcms2'], 'cmsDoTransformStride'):
    cmsDoTransformStride = _libs['lcms2'].cmsDoTransformStride
    cmsDoTransformStride.argtypes = [cmsHTRANSFORM, POINTER(None), POINTER(None), cmsUInt32Number, cmsUInt32Number]
    cmsDoTransformStride.restype = None

# /usr/include/lcms2.h: 1741
if hasattr(_libs['lcms2'], 'cmsDoTransformLineStride'):
    cmsDoTransformLineStride = _libs['lcms2'].cmsDoTransformLineStride
    cmsDoTransformLineStride.argtypes = [cmsHTRANSFORM, POINTER(None), POINTER(None), cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number, cmsUInt32Number]
    cmsDoTransformLineStride.restype = None

# /usr/include/lcms2.h: 1752
if hasattr(_libs['lcms2'], 'cmsSetAlarmCodes'):
    cmsSetAlarmCodes = _libs['lcms2'].cmsSetAlarmCodes
    cmsSetAlarmCodes.argtypes = [cmsUInt16Number * 16]
    cmsSetAlarmCodes.restype = None

# /usr/include/lcms2.h: 1753
if hasattr(_libs['lcms2'], 'cmsGetAlarmCodes'):
    cmsGetAlarmCodes = _libs['lcms2'].cmsGetAlarmCodes
    cmsGetAlarmCodes.argtypes = [cmsUInt16Number * 16]
    cmsGetAlarmCodes.restype = None

# /usr/include/lcms2.h: 1756
if hasattr(_libs['lcms2'], 'cmsSetAlarmCodesTHR'):
    cmsSetAlarmCodesTHR = _libs['lcms2'].cmsSetAlarmCodesTHR
    cmsSetAlarmCodesTHR.argtypes = [cmsContext, cmsUInt16Number * 16]
    cmsSetAlarmCodesTHR.restype = None

# /usr/include/lcms2.h: 1758
if hasattr(_libs['lcms2'], 'cmsGetAlarmCodesTHR'):
    cmsGetAlarmCodesTHR = _libs['lcms2'].cmsGetAlarmCodesTHR
    cmsGetAlarmCodesTHR.argtypes = [cmsContext, cmsUInt16Number * 16]
    cmsGetAlarmCodesTHR.restype = None

# /usr/include/lcms2.h: 1764
if hasattr(_libs['lcms2'], 'cmsSetAdaptationState'):
    cmsSetAdaptationState = _libs['lcms2'].cmsSetAdaptationState
    cmsSetAdaptationState.argtypes = [cmsFloat64Number]
    cmsSetAdaptationState.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1765
if hasattr(_libs['lcms2'], 'cmsSetAdaptationStateTHR'):
    cmsSetAdaptationStateTHR = _libs['lcms2'].cmsSetAdaptationStateTHR
    cmsSetAdaptationStateTHR.argtypes = [cmsContext, cmsFloat64Number]
    cmsSetAdaptationStateTHR.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1770
if hasattr(_libs['lcms2'], 'cmsGetTransformContextID'):
    cmsGetTransformContextID = _libs['lcms2'].cmsGetTransformContextID
    cmsGetTransformContextID.argtypes = [cmsHTRANSFORM]
    cmsGetTransformContextID.restype = cmsContext

# /usr/include/lcms2.h: 1773
if hasattr(_libs['lcms2'], 'cmsGetTransformInputFormat'):
    cmsGetTransformInputFormat = _libs['lcms2'].cmsGetTransformInputFormat
    cmsGetTransformInputFormat.argtypes = [cmsHTRANSFORM]
    cmsGetTransformInputFormat.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1774
if hasattr(_libs['lcms2'], 'cmsGetTransformOutputFormat'):
    cmsGetTransformOutputFormat = _libs['lcms2'].cmsGetTransformOutputFormat
    cmsGetTransformOutputFormat.argtypes = [cmsHTRANSFORM]
    cmsGetTransformOutputFormat.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1777
if hasattr(_libs['lcms2'], 'cmsChangeBuffersFormat'):
    cmsChangeBuffersFormat = _libs['lcms2'].cmsChangeBuffersFormat
    cmsChangeBuffersFormat.argtypes = [cmsHTRANSFORM, cmsUInt32Number, cmsUInt32Number]
    cmsChangeBuffersFormat.restype = cmsBool

enum_anon_40 = c_int # /usr/include/lcms2.h: 1785

cmsPS_RESOURCE_CSA = 0 # /usr/include/lcms2.h: 1785

cmsPS_RESOURCE_CRD = (cmsPS_RESOURCE_CSA + 1) # /usr/include/lcms2.h: 1785

cmsPSResourceType = enum_anon_40 # /usr/include/lcms2.h: 1785

# /usr/include/lcms2.h: 1788
if hasattr(_libs['lcms2'], 'cmsGetPostScriptColorResource'):
    cmsGetPostScriptColorResource = _libs['lcms2'].cmsGetPostScriptColorResource
    cmsGetPostScriptColorResource.argtypes = [cmsContext, cmsPSResourceType, cmsHPROFILE, cmsUInt32Number, cmsUInt32Number, POINTER(cmsIOHANDLER)]
    cmsGetPostScriptColorResource.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1795
if hasattr(_libs['lcms2'], 'cmsGetPostScriptCSA'):
    cmsGetPostScriptCSA = _libs['lcms2'].cmsGetPostScriptCSA
    cmsGetPostScriptCSA.argtypes = [cmsContext, cmsHPROFILE, cmsUInt32Number, cmsUInt32Number, POINTER(None), cmsUInt32Number]
    cmsGetPostScriptCSA.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1796
if hasattr(_libs['lcms2'], 'cmsGetPostScriptCRD'):
    cmsGetPostScriptCRD = _libs['lcms2'].cmsGetPostScriptCRD
    cmsGetPostScriptCRD.argtypes = [cmsContext, cmsHPROFILE, cmsUInt32Number, cmsUInt32Number, POINTER(None), cmsUInt32Number]
    cmsGetPostScriptCRD.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1801
if hasattr(_libs['lcms2'], 'cmsIT8Alloc'):
    cmsIT8Alloc = _libs['lcms2'].cmsIT8Alloc
    cmsIT8Alloc.argtypes = [cmsContext]
    cmsIT8Alloc.restype = cmsHANDLE

# /usr/include/lcms2.h: 1802
if hasattr(_libs['lcms2'], 'cmsIT8Free'):
    cmsIT8Free = _libs['lcms2'].cmsIT8Free
    cmsIT8Free.argtypes = [cmsHANDLE]
    cmsIT8Free.restype = None

# /usr/include/lcms2.h: 1805
if hasattr(_libs['lcms2'], 'cmsIT8TableCount'):
    cmsIT8TableCount = _libs['lcms2'].cmsIT8TableCount
    cmsIT8TableCount.argtypes = [cmsHANDLE]
    cmsIT8TableCount.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1806
if hasattr(_libs['lcms2'], 'cmsIT8SetTable'):
    cmsIT8SetTable = _libs['lcms2'].cmsIT8SetTable
    cmsIT8SetTable.argtypes = [cmsHANDLE, cmsUInt32Number]
    cmsIT8SetTable.restype = cmsInt32Number

# /usr/include/lcms2.h: 1809
if hasattr(_libs['lcms2'], 'cmsIT8LoadFromFile'):
    cmsIT8LoadFromFile = _libs['lcms2'].cmsIT8LoadFromFile
    cmsIT8LoadFromFile.argtypes = [cmsContext, String]
    cmsIT8LoadFromFile.restype = cmsHANDLE

# /usr/include/lcms2.h: 1810
if hasattr(_libs['lcms2'], 'cmsIT8LoadFromMem'):
    cmsIT8LoadFromMem = _libs['lcms2'].cmsIT8LoadFromMem
    cmsIT8LoadFromMem.argtypes = [cmsContext, POINTER(None), cmsUInt32Number]
    cmsIT8LoadFromMem.restype = cmsHANDLE

# /usr/include/lcms2.h: 1813
if hasattr(_libs['lcms2'], 'cmsIT8SaveToFile'):
    cmsIT8SaveToFile = _libs['lcms2'].cmsIT8SaveToFile
    cmsIT8SaveToFile.argtypes = [cmsHANDLE, String]
    cmsIT8SaveToFile.restype = cmsBool

# /usr/include/lcms2.h: 1814
if hasattr(_libs['lcms2'], 'cmsIT8SaveToMem'):
    cmsIT8SaveToMem = _libs['lcms2'].cmsIT8SaveToMem
    cmsIT8SaveToMem.argtypes = [cmsHANDLE, POINTER(None), POINTER(cmsUInt32Number)]
    cmsIT8SaveToMem.restype = cmsBool

# /usr/include/lcms2.h: 1817
if hasattr(_libs['lcms2'], 'cmsIT8GetSheetType'):
    cmsIT8GetSheetType = _libs['lcms2'].cmsIT8GetSheetType
    cmsIT8GetSheetType.argtypes = [cmsHANDLE]
    cmsIT8GetSheetType.restype = c_char_p

# /usr/include/lcms2.h: 1818
if hasattr(_libs['lcms2'], 'cmsIT8SetSheetType'):
    cmsIT8SetSheetType = _libs['lcms2'].cmsIT8SetSheetType
    cmsIT8SetSheetType.argtypes = [cmsHANDLE, String]
    cmsIT8SetSheetType.restype = cmsBool

# /usr/include/lcms2.h: 1820
if hasattr(_libs['lcms2'], 'cmsIT8SetComment'):
    cmsIT8SetComment = _libs['lcms2'].cmsIT8SetComment
    cmsIT8SetComment.argtypes = [cmsHANDLE, String]
    cmsIT8SetComment.restype = cmsBool

# /usr/include/lcms2.h: 1822
if hasattr(_libs['lcms2'], 'cmsIT8SetPropertyStr'):
    cmsIT8SetPropertyStr = _libs['lcms2'].cmsIT8SetPropertyStr
    cmsIT8SetPropertyStr.argtypes = [cmsHANDLE, String, String]
    cmsIT8SetPropertyStr.restype = cmsBool

# /usr/include/lcms2.h: 1823
if hasattr(_libs['lcms2'], 'cmsIT8SetPropertyDbl'):
    cmsIT8SetPropertyDbl = _libs['lcms2'].cmsIT8SetPropertyDbl
    cmsIT8SetPropertyDbl.argtypes = [cmsHANDLE, String, cmsFloat64Number]
    cmsIT8SetPropertyDbl.restype = cmsBool

# /usr/include/lcms2.h: 1824
if hasattr(_libs['lcms2'], 'cmsIT8SetPropertyHex'):
    cmsIT8SetPropertyHex = _libs['lcms2'].cmsIT8SetPropertyHex
    cmsIT8SetPropertyHex.argtypes = [cmsHANDLE, String, cmsUInt32Number]
    cmsIT8SetPropertyHex.restype = cmsBool

# /usr/include/lcms2.h: 1825
if hasattr(_libs['lcms2'], 'cmsIT8SetPropertyMulti'):
    cmsIT8SetPropertyMulti = _libs['lcms2'].cmsIT8SetPropertyMulti
    cmsIT8SetPropertyMulti.argtypes = [cmsHANDLE, String, String, String]
    cmsIT8SetPropertyMulti.restype = cmsBool

# /usr/include/lcms2.h: 1826
if hasattr(_libs['lcms2'], 'cmsIT8SetPropertyUncooked'):
    cmsIT8SetPropertyUncooked = _libs['lcms2'].cmsIT8SetPropertyUncooked
    cmsIT8SetPropertyUncooked.argtypes = [cmsHANDLE, String, String]
    cmsIT8SetPropertyUncooked.restype = cmsBool

# /usr/include/lcms2.h: 1829
if hasattr(_libs['lcms2'], 'cmsIT8GetProperty'):
    cmsIT8GetProperty = _libs['lcms2'].cmsIT8GetProperty
    cmsIT8GetProperty.argtypes = [cmsHANDLE, String]
    cmsIT8GetProperty.restype = c_char_p

# /usr/include/lcms2.h: 1830
if hasattr(_libs['lcms2'], 'cmsIT8GetPropertyDbl'):
    cmsIT8GetPropertyDbl = _libs['lcms2'].cmsIT8GetPropertyDbl
    cmsIT8GetPropertyDbl.argtypes = [cmsHANDLE, String]
    cmsIT8GetPropertyDbl.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1831
if hasattr(_libs['lcms2'], 'cmsIT8GetPropertyMulti'):
    cmsIT8GetPropertyMulti = _libs['lcms2'].cmsIT8GetPropertyMulti
    cmsIT8GetPropertyMulti.argtypes = [cmsHANDLE, String, String]
    cmsIT8GetPropertyMulti.restype = c_char_p

# /usr/include/lcms2.h: 1832
if hasattr(_libs['lcms2'], 'cmsIT8EnumProperties'):
    cmsIT8EnumProperties = _libs['lcms2'].cmsIT8EnumProperties
    cmsIT8EnumProperties.argtypes = [cmsHANDLE, POINTER(POINTER(POINTER(c_char)))]
    cmsIT8EnumProperties.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1833
if hasattr(_libs['lcms2'], 'cmsIT8EnumPropertyMulti'):
    cmsIT8EnumPropertyMulti = _libs['lcms2'].cmsIT8EnumPropertyMulti
    cmsIT8EnumPropertyMulti.argtypes = [cmsHANDLE, String, POINTER(POINTER(POINTER(c_char)))]
    cmsIT8EnumPropertyMulti.restype = cmsUInt32Number

# /usr/include/lcms2.h: 1836
if hasattr(_libs['lcms2'], 'cmsIT8GetDataRowCol'):
    cmsIT8GetDataRowCol = _libs['lcms2'].cmsIT8GetDataRowCol
    cmsIT8GetDataRowCol.argtypes = [cmsHANDLE, c_int, c_int]
    cmsIT8GetDataRowCol.restype = c_char_p

# /usr/include/lcms2.h: 1837
if hasattr(_libs['lcms2'], 'cmsIT8GetDataRowColDbl'):
    cmsIT8GetDataRowColDbl = _libs['lcms2'].cmsIT8GetDataRowColDbl
    cmsIT8GetDataRowColDbl.argtypes = [cmsHANDLE, c_int, c_int]
    cmsIT8GetDataRowColDbl.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1839
if hasattr(_libs['lcms2'], 'cmsIT8SetDataRowCol'):
    cmsIT8SetDataRowCol = _libs['lcms2'].cmsIT8SetDataRowCol
    cmsIT8SetDataRowCol.argtypes = [cmsHANDLE, c_int, c_int, String]
    cmsIT8SetDataRowCol.restype = cmsBool

# /usr/include/lcms2.h: 1842
if hasattr(_libs['lcms2'], 'cmsIT8SetDataRowColDbl'):
    cmsIT8SetDataRowColDbl = _libs['lcms2'].cmsIT8SetDataRowColDbl
    cmsIT8SetDataRowColDbl.argtypes = [cmsHANDLE, c_int, c_int, cmsFloat64Number]
    cmsIT8SetDataRowColDbl.restype = cmsBool

# /usr/include/lcms2.h: 1845
if hasattr(_libs['lcms2'], 'cmsIT8GetData'):
    cmsIT8GetData = _libs['lcms2'].cmsIT8GetData
    cmsIT8GetData.argtypes = [cmsHANDLE, String, String]
    cmsIT8GetData.restype = c_char_p

# /usr/include/lcms2.h: 1848
if hasattr(_libs['lcms2'], 'cmsIT8GetDataDbl'):
    cmsIT8GetDataDbl = _libs['lcms2'].cmsIT8GetDataDbl
    cmsIT8GetDataDbl.argtypes = [cmsHANDLE, String, String]
    cmsIT8GetDataDbl.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1850
if hasattr(_libs['lcms2'], 'cmsIT8SetData'):
    cmsIT8SetData = _libs['lcms2'].cmsIT8SetData
    cmsIT8SetData.argtypes = [cmsHANDLE, String, String, String]
    cmsIT8SetData.restype = cmsBool

# /usr/include/lcms2.h: 1854
if hasattr(_libs['lcms2'], 'cmsIT8SetDataDbl'):
    cmsIT8SetDataDbl = _libs['lcms2'].cmsIT8SetDataDbl
    cmsIT8SetDataDbl.argtypes = [cmsHANDLE, String, String, cmsFloat64Number]
    cmsIT8SetDataDbl.restype = cmsBool

# /usr/include/lcms2.h: 1858
if hasattr(_libs['lcms2'], 'cmsIT8FindDataFormat'):
    cmsIT8FindDataFormat = _libs['lcms2'].cmsIT8FindDataFormat
    cmsIT8FindDataFormat.argtypes = [cmsHANDLE, String]
    cmsIT8FindDataFormat.restype = c_int

# /usr/include/lcms2.h: 1859
if hasattr(_libs['lcms2'], 'cmsIT8SetDataFormat'):
    cmsIT8SetDataFormat = _libs['lcms2'].cmsIT8SetDataFormat
    cmsIT8SetDataFormat.argtypes = [cmsHANDLE, c_int, String]
    cmsIT8SetDataFormat.restype = cmsBool

# /usr/include/lcms2.h: 1860
if hasattr(_libs['lcms2'], 'cmsIT8EnumDataFormat'):
    cmsIT8EnumDataFormat = _libs['lcms2'].cmsIT8EnumDataFormat
    cmsIT8EnumDataFormat.argtypes = [cmsHANDLE, POINTER(POINTER(POINTER(c_char)))]
    cmsIT8EnumDataFormat.restype = c_int

# /usr/include/lcms2.h: 1862
if hasattr(_libs['lcms2'], 'cmsIT8GetPatchName'):
    cmsIT8GetPatchName = _libs['lcms2'].cmsIT8GetPatchName
    cmsIT8GetPatchName.argtypes = [cmsHANDLE, c_int, String]
    cmsIT8GetPatchName.restype = c_char_p

# /usr/include/lcms2.h: 1863
if hasattr(_libs['lcms2'], 'cmsIT8GetPatchByName'):
    cmsIT8GetPatchByName = _libs['lcms2'].cmsIT8GetPatchByName
    cmsIT8GetPatchByName.argtypes = [cmsHANDLE, String]
    cmsIT8GetPatchByName.restype = c_int

# /usr/include/lcms2.h: 1866
if hasattr(_libs['lcms2'], 'cmsIT8SetTableByLabel'):
    cmsIT8SetTableByLabel = _libs['lcms2'].cmsIT8SetTableByLabel
    cmsIT8SetTableByLabel.argtypes = [cmsHANDLE, String, String, String]
    cmsIT8SetTableByLabel.restype = c_int

# /usr/include/lcms2.h: 1868
if hasattr(_libs['lcms2'], 'cmsIT8SetIndexColumn'):
    cmsIT8SetIndexColumn = _libs['lcms2'].cmsIT8SetIndexColumn
    cmsIT8SetIndexColumn.argtypes = [cmsHANDLE, String]
    cmsIT8SetIndexColumn.restype = cmsBool

# /usr/include/lcms2.h: 1871
if hasattr(_libs['lcms2'], 'cmsIT8DefineDblFormat'):
    cmsIT8DefineDblFormat = _libs['lcms2'].cmsIT8DefineDblFormat
    cmsIT8DefineDblFormat.argtypes = [cmsHANDLE, String]
    cmsIT8DefineDblFormat.restype = None

# /usr/include/lcms2.h: 1875
if hasattr(_libs['lcms2'], 'cmsGBDAlloc'):
    cmsGBDAlloc = _libs['lcms2'].cmsGBDAlloc
    cmsGBDAlloc.argtypes = [cmsContext]
    cmsGBDAlloc.restype = cmsHANDLE

# /usr/include/lcms2.h: 1876
if hasattr(_libs['lcms2'], 'cmsGBDFree'):
    cmsGBDFree = _libs['lcms2'].cmsGBDFree
    cmsGBDFree.argtypes = [cmsHANDLE]
    cmsGBDFree.restype = None

# /usr/include/lcms2.h: 1877
if hasattr(_libs['lcms2'], 'cmsGDBAddPoint'):
    cmsGDBAddPoint = _libs['lcms2'].cmsGDBAddPoint
    cmsGDBAddPoint.argtypes = [cmsHANDLE, POINTER(cmsCIELab)]
    cmsGDBAddPoint.restype = cmsBool

# /usr/include/lcms2.h: 1878
if hasattr(_libs['lcms2'], 'cmsGDBCompute'):
    cmsGDBCompute = _libs['lcms2'].cmsGDBCompute
    cmsGDBCompute.argtypes = [cmsHANDLE, cmsUInt32Number]
    cmsGDBCompute.restype = cmsBool

# /usr/include/lcms2.h: 1879
if hasattr(_libs['lcms2'], 'cmsGDBCheckPoint'):
    cmsGDBCheckPoint = _libs['lcms2'].cmsGDBCheckPoint
    cmsGDBCheckPoint.argtypes = [cmsHANDLE, POINTER(cmsCIELab)]
    cmsGDBCheckPoint.restype = cmsBool

# /usr/include/lcms2.h: 1884
if hasattr(_libs['lcms2'], 'cmsDetectBlackPoint'):
    cmsDetectBlackPoint = _libs['lcms2'].cmsDetectBlackPoint
    cmsDetectBlackPoint.argtypes = [POINTER(cmsCIEXYZ), cmsHPROFILE, cmsUInt32Number, cmsUInt32Number]
    cmsDetectBlackPoint.restype = cmsBool

# /usr/include/lcms2.h: 1885
if hasattr(_libs['lcms2'], 'cmsDetectDestinationBlackPoint'):
    cmsDetectDestinationBlackPoint = _libs['lcms2'].cmsDetectDestinationBlackPoint
    cmsDetectDestinationBlackPoint.argtypes = [POINTER(cmsCIEXYZ), cmsHPROFILE, cmsUInt32Number, cmsUInt32Number]
    cmsDetectDestinationBlackPoint.restype = cmsBool

# /usr/include/lcms2.h: 1888
if hasattr(_libs['lcms2'], 'cmsDetectTAC'):
    cmsDetectTAC = _libs['lcms2'].cmsDetectTAC
    cmsDetectTAC.argtypes = [cmsHPROFILE]
    cmsDetectTAC.restype = cmsFloat64Number

# /usr/include/lcms2.h: 1892
if hasattr(_libs['lcms2'], 'cmsDesaturateLab'):
    cmsDesaturateLab = _libs['lcms2'].cmsDesaturateLab
    cmsDesaturateLab.argtypes = [POINTER(cmsCIELab), c_double, c_double, c_double, c_double]
    cmsDesaturateLab.restype = cmsBool

# /usr/include/lcms2_plugin.h: 74
class struct_anon_63(Structure):
    pass

struct_anon_63.__slots__ = [
    'n',
]
struct_anon_63._fields_ = [
    ('n', cmsFloat64Number * 3),
]

cmsVEC3 = struct_anon_63 # /usr/include/lcms2_plugin.h: 74

# /usr/include/lcms2_plugin.h: 80
class struct_anon_64(Structure):
    pass

struct_anon_64.__slots__ = [
    'v',
]
struct_anon_64._fields_ = [
    ('v', cmsVEC3 * 3),
]

cmsMAT3 = struct_anon_64 # /usr/include/lcms2_plugin.h: 80

# /usr/include/lcms2_plugin.h: 82
if hasattr(_libs['lcms2'], '_cmsVEC3init'):
    _cmsVEC3init = _libs['lcms2']._cmsVEC3init
    _cmsVEC3init.argtypes = [POINTER(cmsVEC3), cmsFloat64Number, cmsFloat64Number, cmsFloat64Number]
    _cmsVEC3init.restype = None

# /usr/include/lcms2_plugin.h: 83
if hasattr(_libs['lcms2'], '_cmsVEC3minus'):
    _cmsVEC3minus = _libs['lcms2']._cmsVEC3minus
    _cmsVEC3minus.argtypes = [POINTER(cmsVEC3), POINTER(cmsVEC3), POINTER(cmsVEC3)]
    _cmsVEC3minus.restype = None

# /usr/include/lcms2_plugin.h: 84
if hasattr(_libs['lcms2'], '_cmsVEC3cross'):
    _cmsVEC3cross = _libs['lcms2']._cmsVEC3cross
    _cmsVEC3cross.argtypes = [POINTER(cmsVEC3), POINTER(cmsVEC3), POINTER(cmsVEC3)]
    _cmsVEC3cross.restype = None

# /usr/include/lcms2_plugin.h: 85
if hasattr(_libs['lcms2'], '_cmsVEC3dot'):
    _cmsVEC3dot = _libs['lcms2']._cmsVEC3dot
    _cmsVEC3dot.argtypes = [POINTER(cmsVEC3), POINTER(cmsVEC3)]
    _cmsVEC3dot.restype = cmsFloat64Number

# /usr/include/lcms2_plugin.h: 86
if hasattr(_libs['lcms2'], '_cmsVEC3length'):
    _cmsVEC3length = _libs['lcms2']._cmsVEC3length
    _cmsVEC3length.argtypes = [POINTER(cmsVEC3)]
    _cmsVEC3length.restype = cmsFloat64Number

# /usr/include/lcms2_plugin.h: 87
if hasattr(_libs['lcms2'], '_cmsVEC3distance'):
    _cmsVEC3distance = _libs['lcms2']._cmsVEC3distance
    _cmsVEC3distance.argtypes = [POINTER(cmsVEC3), POINTER(cmsVEC3)]
    _cmsVEC3distance.restype = cmsFloat64Number

# /usr/include/lcms2_plugin.h: 89
if hasattr(_libs['lcms2'], '_cmsMAT3identity'):
    _cmsMAT3identity = _libs['lcms2']._cmsMAT3identity
    _cmsMAT3identity.argtypes = [POINTER(cmsMAT3)]
    _cmsMAT3identity.restype = None

# /usr/include/lcms2_plugin.h: 90
if hasattr(_libs['lcms2'], '_cmsMAT3isIdentity'):
    _cmsMAT3isIdentity = _libs['lcms2']._cmsMAT3isIdentity
    _cmsMAT3isIdentity.argtypes = [POINTER(cmsMAT3)]
    _cmsMAT3isIdentity.restype = cmsBool

# /usr/include/lcms2_plugin.h: 91
if hasattr(_libs['lcms2'], '_cmsMAT3per'):
    _cmsMAT3per = _libs['lcms2']._cmsMAT3per
    _cmsMAT3per.argtypes = [POINTER(cmsMAT3), POINTER(cmsMAT3), POINTER(cmsMAT3)]
    _cmsMAT3per.restype = None

# /usr/include/lcms2_plugin.h: 92
if hasattr(_libs['lcms2'], '_cmsMAT3inverse'):
    _cmsMAT3inverse = _libs['lcms2']._cmsMAT3inverse
    _cmsMAT3inverse.argtypes = [POINTER(cmsMAT3), POINTER(cmsMAT3)]
    _cmsMAT3inverse.restype = cmsBool

# /usr/include/lcms2_plugin.h: 93
if hasattr(_libs['lcms2'], '_cmsMAT3solve'):
    _cmsMAT3solve = _libs['lcms2']._cmsMAT3solve
    _cmsMAT3solve.argtypes = [POINTER(cmsVEC3), POINTER(cmsMAT3), POINTER(cmsVEC3)]
    _cmsMAT3solve.restype = cmsBool

# /usr/include/lcms2_plugin.h: 94
if hasattr(_libs['lcms2'], '_cmsMAT3eval'):
    _cmsMAT3eval = _libs['lcms2']._cmsMAT3eval
    _cmsMAT3eval.argtypes = [POINTER(cmsVEC3), POINTER(cmsMAT3), POINTER(cmsVEC3)]
    _cmsMAT3eval.restype = None

# /usr/include/lcms2_plugin.h: 99
if hasattr(_libs['lcms2'], 'cmsSignalError'):
    _func = _libs['lcms2'].cmsSignalError
    _restype = None
    _errcheck = None
    _argtypes = [cmsContext, cmsUInt32Number, String]
    cmsSignalError = _variadic_function(_func,_restype,_argtypes,_errcheck)

# /usr/include/lcms2_plugin.h: 103
if hasattr(_libs['lcms2'], '_cmsMalloc'):
    _cmsMalloc = _libs['lcms2']._cmsMalloc
    _cmsMalloc.argtypes = [cmsContext, cmsUInt32Number]
    _cmsMalloc.restype = POINTER(c_ubyte)
    _cmsMalloc.errcheck = lambda v,*a : cast(v, c_void_p)

# /usr/include/lcms2_plugin.h: 104
if hasattr(_libs['lcms2'], '_cmsMallocZero'):
    _cmsMallocZero = _libs['lcms2']._cmsMallocZero
    _cmsMallocZero.argtypes = [cmsContext, cmsUInt32Number]
    _cmsMallocZero.restype = POINTER(c_ubyte)
    _cmsMallocZero.errcheck = lambda v,*a : cast(v, c_void_p)

# /usr/include/lcms2_plugin.h: 105
if hasattr(_libs['lcms2'], '_cmsCalloc'):
    _cmsCalloc = _libs['lcms2']._cmsCalloc
    _cmsCalloc.argtypes = [cmsContext, cmsUInt32Number, cmsUInt32Number]
    _cmsCalloc.restype = POINTER(c_ubyte)
    _cmsCalloc.errcheck = lambda v,*a : cast(v, c_void_p)

# /usr/include/lcms2_plugin.h: 106
if hasattr(_libs['lcms2'], '_cmsRealloc'):
    _cmsRealloc = _libs['lcms2']._cmsRealloc
    _cmsRealloc.argtypes = [cmsContext, POINTER(None), cmsUInt32Number]
    _cmsRealloc.restype = POINTER(c_ubyte)
    _cmsRealloc.errcheck = lambda v,*a : cast(v, c_void_p)

# /usr/include/lcms2_plugin.h: 107
if hasattr(_libs['lcms2'], '_cmsFree'):
    _cmsFree = _libs['lcms2']._cmsFree
    _cmsFree.argtypes = [cmsContext, POINTER(None)]
    _cmsFree.restype = None

# /usr/include/lcms2_plugin.h: 108
if hasattr(_libs['lcms2'], '_cmsDupMem'):
    _cmsDupMem = _libs['lcms2']._cmsDupMem
    _cmsDupMem.argtypes = [cmsContext, POINTER(None), cmsUInt32Number]
    _cmsDupMem.restype = POINTER(c_ubyte)
    _cmsDupMem.errcheck = lambda v,*a : cast(v, c_void_p)

struct__cms_io_handler.__slots__ = [
    'stream',
    'ContextID',
    'UsedSpace',
    'ReportedSize',
    'PhysicalFile',
    'Read',
    'Seek',
    'Close',
    'Tell',
    'Write',
]
struct__cms_io_handler._fields_ = [
    ('stream', POINTER(None)),
    ('ContextID', cmsContext),
    ('UsedSpace', cmsUInt32Number),
    ('ReportedSize', cmsUInt32Number),
    ('PhysicalFile', c_char * 256),
    ('Read', CFUNCTYPE(UNCHECKED(cmsUInt32Number), POINTER(struct__cms_io_handler), POINTER(None), cmsUInt32Number, cmsUInt32Number)),
    ('Seek', CFUNCTYPE(UNCHECKED(cmsBool), POINTER(struct__cms_io_handler), cmsUInt32Number)),
    ('Close', CFUNCTYPE(UNCHECKED(cmsBool), POINTER(struct__cms_io_handler))),
    ('Tell', CFUNCTYPE(UNCHECKED(cmsUInt32Number), POINTER(struct__cms_io_handler))),
    ('Write', CFUNCTYPE(UNCHECKED(cmsBool), POINTER(struct__cms_io_handler), cmsUInt32Number, POINTER(None))),
]

# /usr/include/lcms2_plugin.h: 132
if hasattr(_libs['lcms2'], '_cmsAdjustEndianess16'):
    _cmsAdjustEndianess16 = _libs['lcms2']._cmsAdjustEndianess16
    _cmsAdjustEndianess16.argtypes = [cmsUInt16Number]
    _cmsAdjustEndianess16.restype = cmsUInt16Number

# /usr/include/lcms2_plugin.h: 133
if hasattr(_libs['lcms2'], '_cmsAdjustEndianess32'):
    _cmsAdjustEndianess32 = _libs['lcms2']._cmsAdjustEndianess32
    _cmsAdjustEndianess32.argtypes = [cmsUInt32Number]
    _cmsAdjustEndianess32.restype = cmsUInt32Number

# /usr/include/lcms2_plugin.h: 134
if hasattr(_libs['lcms2'], '_cmsAdjustEndianess64'):
    _cmsAdjustEndianess64 = _libs['lcms2']._cmsAdjustEndianess64
    _cmsAdjustEndianess64.argtypes = [POINTER(cmsUInt64Number), POINTER(cmsUInt64Number)]
    _cmsAdjustEndianess64.restype = None

# /usr/include/lcms2_plugin.h: 137
if hasattr(_libs['lcms2'], '_cmsReadUInt8Number'):
    _cmsReadUInt8Number = _libs['lcms2']._cmsReadUInt8Number
    _cmsReadUInt8Number.argtypes = [POINTER(cmsIOHANDLER), POINTER(cmsUInt8Number)]
    _cmsReadUInt8Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 138
if hasattr(_libs['lcms2'], '_cmsReadUInt16Number'):
    _cmsReadUInt16Number = _libs['lcms2']._cmsReadUInt16Number
    _cmsReadUInt16Number.argtypes = [POINTER(cmsIOHANDLER), POINTER(cmsUInt16Number)]
    _cmsReadUInt16Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 139
if hasattr(_libs['lcms2'], '_cmsReadUInt32Number'):
    _cmsReadUInt32Number = _libs['lcms2']._cmsReadUInt32Number
    _cmsReadUInt32Number.argtypes = [POINTER(cmsIOHANDLER), POINTER(cmsUInt32Number)]
    _cmsReadUInt32Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 140
if hasattr(_libs['lcms2'], '_cmsReadFloat32Number'):
    _cmsReadFloat32Number = _libs['lcms2']._cmsReadFloat32Number
    _cmsReadFloat32Number.argtypes = [POINTER(cmsIOHANDLER), POINTER(cmsFloat32Number)]
    _cmsReadFloat32Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 141
if hasattr(_libs['lcms2'], '_cmsReadUInt64Number'):
    _cmsReadUInt64Number = _libs['lcms2']._cmsReadUInt64Number
    _cmsReadUInt64Number.argtypes = [POINTER(cmsIOHANDLER), POINTER(cmsUInt64Number)]
    _cmsReadUInt64Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 142
if hasattr(_libs['lcms2'], '_cmsRead15Fixed16Number'):
    _cmsRead15Fixed16Number = _libs['lcms2']._cmsRead15Fixed16Number
    _cmsRead15Fixed16Number.argtypes = [POINTER(cmsIOHANDLER), POINTER(cmsFloat64Number)]
    _cmsRead15Fixed16Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 143
if hasattr(_libs['lcms2'], '_cmsReadXYZNumber'):
    _cmsReadXYZNumber = _libs['lcms2']._cmsReadXYZNumber
    _cmsReadXYZNumber.argtypes = [POINTER(cmsIOHANDLER), POINTER(cmsCIEXYZ)]
    _cmsReadXYZNumber.restype = cmsBool

# /usr/include/lcms2_plugin.h: 144
if hasattr(_libs['lcms2'], '_cmsReadUInt16Array'):
    _cmsReadUInt16Array = _libs['lcms2']._cmsReadUInt16Array
    _cmsReadUInt16Array.argtypes = [POINTER(cmsIOHANDLER), cmsUInt32Number, POINTER(cmsUInt16Number)]
    _cmsReadUInt16Array.restype = cmsBool

# /usr/include/lcms2_plugin.h: 146
if hasattr(_libs['lcms2'], '_cmsWriteUInt8Number'):
    _cmsWriteUInt8Number = _libs['lcms2']._cmsWriteUInt8Number
    _cmsWriteUInt8Number.argtypes = [POINTER(cmsIOHANDLER), cmsUInt8Number]
    _cmsWriteUInt8Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 147
if hasattr(_libs['lcms2'], '_cmsWriteUInt16Number'):
    _cmsWriteUInt16Number = _libs['lcms2']._cmsWriteUInt16Number
    _cmsWriteUInt16Number.argtypes = [POINTER(cmsIOHANDLER), cmsUInt16Number]
    _cmsWriteUInt16Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 148
if hasattr(_libs['lcms2'], '_cmsWriteUInt32Number'):
    _cmsWriteUInt32Number = _libs['lcms2']._cmsWriteUInt32Number
    _cmsWriteUInt32Number.argtypes = [POINTER(cmsIOHANDLER), cmsUInt32Number]
    _cmsWriteUInt32Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 149
if hasattr(_libs['lcms2'], '_cmsWriteFloat32Number'):
    _cmsWriteFloat32Number = _libs['lcms2']._cmsWriteFloat32Number
    _cmsWriteFloat32Number.argtypes = [POINTER(cmsIOHANDLER), cmsFloat32Number]
    _cmsWriteFloat32Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 150
if hasattr(_libs['lcms2'], '_cmsWriteUInt64Number'):
    _cmsWriteUInt64Number = _libs['lcms2']._cmsWriteUInt64Number
    _cmsWriteUInt64Number.argtypes = [POINTER(cmsIOHANDLER), POINTER(cmsUInt64Number)]
    _cmsWriteUInt64Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 151
if hasattr(_libs['lcms2'], '_cmsWrite15Fixed16Number'):
    _cmsWrite15Fixed16Number = _libs['lcms2']._cmsWrite15Fixed16Number
    _cmsWrite15Fixed16Number.argtypes = [POINTER(cmsIOHANDLER), cmsFloat64Number]
    _cmsWrite15Fixed16Number.restype = cmsBool

# /usr/include/lcms2_plugin.h: 152
if hasattr(_libs['lcms2'], '_cmsWriteXYZNumber'):
    _cmsWriteXYZNumber = _libs['lcms2']._cmsWriteXYZNumber
    _cmsWriteXYZNumber.argtypes = [POINTER(cmsIOHANDLER), POINTER(cmsCIEXYZ)]
    _cmsWriteXYZNumber.restype = cmsBool

# /usr/include/lcms2_plugin.h: 153
if hasattr(_libs['lcms2'], '_cmsWriteUInt16Array'):
    _cmsWriteUInt16Array = _libs['lcms2']._cmsWriteUInt16Array
    _cmsWriteUInt16Array.argtypes = [POINTER(cmsIOHANDLER), cmsUInt32Number, POINTER(cmsUInt16Number)]
    _cmsWriteUInt16Array.restype = cmsBool

# /usr/include/lcms2_plugin.h: 160
class struct_anon_65(Structure):
    pass

struct_anon_65.__slots__ = [
    'sig',
    'reserved',
]
struct_anon_65._fields_ = [
    ('sig', cmsTagTypeSignature),
    ('reserved', cmsInt8Number * 4),
]

_cmsTagBase = struct_anon_65 # /usr/include/lcms2_plugin.h: 160

# /usr/include/lcms2_plugin.h: 163
if hasattr(_libs['lcms2'], '_cmsReadTypeBase'):
    _cmsReadTypeBase = _libs['lcms2']._cmsReadTypeBase
    _cmsReadTypeBase.argtypes = [POINTER(cmsIOHANDLER)]
    _cmsReadTypeBase.restype = cmsTagTypeSignature

# /usr/include/lcms2_plugin.h: 164
if hasattr(_libs['lcms2'], '_cmsWriteTypeBase'):
    _cmsWriteTypeBase = _libs['lcms2']._cmsWriteTypeBase
    _cmsWriteTypeBase.argtypes = [POINTER(cmsIOHANDLER), cmsTagTypeSignature]
    _cmsWriteTypeBase.restype = cmsBool

# /usr/include/lcms2_plugin.h: 167
if hasattr(_libs['lcms2'], '_cmsReadAlignment'):
    _cmsReadAlignment = _libs['lcms2']._cmsReadAlignment
    _cmsReadAlignment.argtypes = [POINTER(cmsIOHANDLER)]
    _cmsReadAlignment.restype = cmsBool

# /usr/include/lcms2_plugin.h: 168
if hasattr(_libs['lcms2'], '_cmsWriteAlignment'):
    _cmsWriteAlignment = _libs['lcms2']._cmsWriteAlignment
    _cmsWriteAlignment.argtypes = [POINTER(cmsIOHANDLER)]
    _cmsWriteAlignment.restype = cmsBool

# /usr/include/lcms2_plugin.h: 171
if hasattr(_libs['lcms2'], '_cmsIOPrintf'):
    _func = _libs['lcms2']._cmsIOPrintf
    _restype = cmsBool
    _errcheck = None
    _argtypes = [POINTER(cmsIOHANDLER), String]
    _cmsIOPrintf = _variadic_function(_func,_restype,_argtypes,_errcheck)

# /usr/include/lcms2_plugin.h: 174
if hasattr(_libs['lcms2'], '_cms8Fixed8toDouble'):
    _cms8Fixed8toDouble = _libs['lcms2']._cms8Fixed8toDouble
    _cms8Fixed8toDouble.argtypes = [cmsUInt16Number]
    _cms8Fixed8toDouble.restype = cmsFloat64Number

# /usr/include/lcms2_plugin.h: 175
if hasattr(_libs['lcms2'], '_cmsDoubleTo8Fixed8'):
    _cmsDoubleTo8Fixed8 = _libs['lcms2']._cmsDoubleTo8Fixed8
    _cmsDoubleTo8Fixed8.argtypes = [cmsFloat64Number]
    _cmsDoubleTo8Fixed8.restype = cmsUInt16Number

# /usr/include/lcms2_plugin.h: 177
if hasattr(_libs['lcms2'], '_cms15Fixed16toDouble'):
    _cms15Fixed16toDouble = _libs['lcms2']._cms15Fixed16toDouble
    _cms15Fixed16toDouble.argtypes = [cmsS15Fixed16Number]
    _cms15Fixed16toDouble.restype = cmsFloat64Number

# /usr/include/lcms2_plugin.h: 178
if hasattr(_libs['lcms2'], '_cmsDoubleTo15Fixed16'):
    _cmsDoubleTo15Fixed16 = _libs['lcms2']._cmsDoubleTo15Fixed16
    _cmsDoubleTo15Fixed16.argtypes = [cmsFloat64Number]
    _cmsDoubleTo15Fixed16.restype = cmsS15Fixed16Number

# /usr/include/lcms2_plugin.h: 181
if hasattr(_libs['lcms2'], '_cmsEncodeDateTimeNumber'):
    _cmsEncodeDateTimeNumber = _libs['lcms2']._cmsEncodeDateTimeNumber
    _cmsEncodeDateTimeNumber.argtypes = [POINTER(cmsDateTimeNumber), POINTER(struct_tm)]
    _cmsEncodeDateTimeNumber.restype = None

# /usr/include/lcms2_plugin.h: 182
if hasattr(_libs['lcms2'], '_cmsDecodeDateTimeNumber'):
    _cmsDecodeDateTimeNumber = _libs['lcms2']._cmsDecodeDateTimeNumber
    _cmsDecodeDateTimeNumber.argtypes = [POINTER(cmsDateTimeNumber), POINTER(struct_tm)]
    _cmsDecodeDateTimeNumber.restype = None

_cmsFreeUserDataFn = CFUNCTYPE(UNCHECKED(None), cmsContext, POINTER(None)) # /usr/include/lcms2_plugin.h: 187

_cmsDupUserDataFn = CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), cmsContext, POINTER(None)) # /usr/include/lcms2_plugin.h: 188

# /usr/include/lcms2_plugin.h: 207
class struct__cmsPluginBaseStruct(Structure):
    pass

struct__cmsPluginBaseStruct.__slots__ = [
    'Magic',
    'ExpectedVersion',
    'Type',
    'Next',
]
struct__cmsPluginBaseStruct._fields_ = [
    ('Magic', cmsUInt32Number),
    ('ExpectedVersion', cmsUInt32Number),
    ('Type', cmsUInt32Number),
    ('Next', POINTER(struct__cmsPluginBaseStruct)),
]

cmsPluginBase = struct__cmsPluginBaseStruct # /usr/include/lcms2_plugin.h: 214

_cmsMallocFnPtrType = CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), cmsContext, cmsUInt32Number) # /usr/include/lcms2_plugin.h: 223

_cmsFreeFnPtrType = CFUNCTYPE(UNCHECKED(None), cmsContext, POINTER(None)) # /usr/include/lcms2_plugin.h: 224

_cmsReallocFnPtrType = CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), cmsContext, POINTER(None), cmsUInt32Number) # /usr/include/lcms2_plugin.h: 225

_cmsMalloZerocFnPtrType = CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), cmsContext, cmsUInt32Number) # /usr/include/lcms2_plugin.h: 227

_cmsCallocFnPtrType = CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), cmsContext, cmsUInt32Number, cmsUInt32Number) # /usr/include/lcms2_plugin.h: 228

_cmsDupFnPtrType = CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), cmsContext, POINTER(None), cmsUInt32Number) # /usr/include/lcms2_plugin.h: 229

# /usr/include/lcms2_plugin.h: 245
class struct_anon_66(Structure):
    pass

struct_anon_66.__slots__ = [
    'base',
    'MallocPtr',
    'FreePtr',
    'ReallocPtr',
    'MallocZeroPtr',
    'CallocPtr',
    'DupPtr',
]
struct_anon_66._fields_ = [
    ('base', cmsPluginBase),
    ('MallocPtr', _cmsMallocFnPtrType),
    ('FreePtr', _cmsFreeFnPtrType),
    ('ReallocPtr', _cmsReallocFnPtrType),
    ('MallocZeroPtr', _cmsMalloZerocFnPtrType),
    ('CallocPtr', _cmsCallocFnPtrType),
    ('DupPtr', _cmsDupFnPtrType),
]

cmsPluginMemHandler = struct_anon_66 # /usr/include/lcms2_plugin.h: 245

# /usr/include/lcms2_plugin.h: 285
class struct__cms_interp_struc(Structure):
    pass

_cmsInterpFn16 = CFUNCTYPE(UNCHECKED(None), POINTER(cmsUInt16Number), POINTER(cmsUInt16Number), POINTER(struct__cms_interp_struc)) # /usr/include/lcms2_plugin.h: 258

_cmsInterpFnFloat = CFUNCTYPE(UNCHECKED(None), POINTER(cmsFloat32Number), POINTER(cmsFloat32Number), POINTER(struct__cms_interp_struc)) # /usr/include/lcms2_plugin.h: 265

# /usr/include/lcms2_plugin.h: 275
class union_anon_67(Union):
    pass

union_anon_67.__slots__ = [
    'Lerp16',
    'LerpFloat',
]
union_anon_67._fields_ = [
    ('Lerp16', _cmsInterpFn16),
    ('LerpFloat', _cmsInterpFnFloat),
]

cmsInterpFunction = union_anon_67 # /usr/include/lcms2_plugin.h: 275

struct__cms_interp_struc.__slots__ = [
    'ContextID',
    'dwFlags',
    'nInputs',
    'nOutputs',
    'nSamples',
    'Domain',
    'opta',
    'Table',
    'Interpolation',
]
struct__cms_interp_struc._fields_ = [
    ('ContextID', cmsContext),
    ('dwFlags', cmsUInt32Number),
    ('nInputs', cmsUInt32Number),
    ('nOutputs', cmsUInt32Number),
    ('nSamples', cmsUInt32Number * 8),
    ('Domain', cmsUInt32Number * 8),
    ('opta', cmsUInt32Number * 8),
    ('Table', POINTER(None)),
    ('Interpolation', cmsInterpFunction),
]

cmsInterpParams = struct__cms_interp_struc # /usr/include/lcms2_plugin.h: 303

cmsInterpFnFactory = CFUNCTYPE(UNCHECKED(cmsInterpFunction), cmsUInt32Number, cmsUInt32Number, cmsUInt32Number) # /usr/include/lcms2_plugin.h: 306

# /usr/include/lcms2_plugin.h: 315
class struct_anon_68(Structure):
    pass

struct_anon_68.__slots__ = [
    'base',
    'InterpolatorsFactory',
]
struct_anon_68._fields_ = [
    ('base', cmsPluginBase),
    ('InterpolatorsFactory', cmsInterpFnFactory),
]

cmsPluginInterpolation = struct_anon_68 # /usr/include/lcms2_plugin.h: 315

cmsParametricCurveEvaluator = CFUNCTYPE(UNCHECKED(cmsFloat64Number), cmsInt32Number, cmsFloat64Number * 10, cmsFloat64Number) # /usr/include/lcms2_plugin.h: 322

# /usr/include/lcms2_plugin.h: 334
class struct_anon_69(Structure):
    pass

struct_anon_69.__slots__ = [
    'base',
    'nFunctions',
    'FunctionTypes',
    'ParameterCount',
    'Evaluator',
]
struct_anon_69._fields_ = [
    ('base', cmsPluginBase),
    ('nFunctions', cmsUInt32Number),
    ('FunctionTypes', cmsUInt32Number * 20),
    ('ParameterCount', cmsUInt32Number * 20),
    ('Evaluator', cmsParametricCurveEvaluator),
]

cmsPluginParametricCurves = struct_anon_69 # /usr/include/lcms2_plugin.h: 334

# /usr/include/lcms2_plugin.h: 341
class struct__cmstransform_struct(Structure):
    pass

cmsFormatter16 = CFUNCTYPE(UNCHECKED(POINTER(cmsUInt8Number)), POINTER(struct__cmstransform_struct), POINTER(cmsUInt16Number), POINTER(cmsUInt8Number), cmsUInt32Number) # /usr/include/lcms2_plugin.h: 343

cmsFormatterFloat = CFUNCTYPE(UNCHECKED(POINTER(cmsUInt8Number)), POINTER(struct__cmstransform_struct), POINTER(cmsFloat32Number), POINTER(cmsUInt8Number), cmsUInt32Number) # /usr/include/lcms2_plugin.h: 348

# /usr/include/lcms2_plugin.h: 358
class union_anon_70(Union):
    pass

union_anon_70.__slots__ = [
    'Fmt16',
    'FmtFloat',
]
union_anon_70._fields_ = [
    ('Fmt16', cmsFormatter16),
    ('FmtFloat', cmsFormatterFloat),
]

cmsFormatter = union_anon_70 # /usr/include/lcms2_plugin.h: 358

enum_anon_71 = c_int # /usr/include/lcms2_plugin.h: 363

cmsFormatterInput = 0 # /usr/include/lcms2_plugin.h: 363

cmsFormatterOutput = 1 # /usr/include/lcms2_plugin.h: 363

cmsFormatterDirection = enum_anon_71 # /usr/include/lcms2_plugin.h: 363

cmsFormatterFactory = CFUNCTYPE(UNCHECKED(cmsFormatter), cmsUInt32Number, cmsFormatterDirection, cmsUInt32Number) # /usr/include/lcms2_plugin.h: 365

# /usr/include/lcms2_plugin.h: 374
class struct_anon_72(Structure):
    pass

struct_anon_72.__slots__ = [
    'base',
    'FormattersFactory',
]
struct_anon_72._fields_ = [
    ('base', cmsPluginBase),
    ('FormattersFactory', cmsFormatterFactory),
]

cmsPluginFormatters = struct_anon_72 # /usr/include/lcms2_plugin.h: 374

# /usr/include/lcms2_plugin.h: 380
class struct__cms_typehandler_struct(Structure):
    pass

struct__cms_typehandler_struct.__slots__ = [
    'Signature',
    'ReadPtr',
    'WritePtr',
    'DupPtr',
    'FreePtr',
    'ContextID',
    'ICCVersion',
]
struct__cms_typehandler_struct._fields_ = [
    ('Signature', cmsTagTypeSignature),
    ('ReadPtr', CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), POINTER(struct__cms_typehandler_struct), POINTER(cmsIOHANDLER), POINTER(cmsUInt32Number), cmsUInt32Number)),
    ('WritePtr', CFUNCTYPE(UNCHECKED(cmsBool), POINTER(struct__cms_typehandler_struct), POINTER(cmsIOHANDLER), POINTER(None), cmsUInt32Number)),
    ('DupPtr', CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), POINTER(struct__cms_typehandler_struct), POINTER(None), cmsUInt32Number)),
    ('FreePtr', CFUNCTYPE(UNCHECKED(None), POINTER(struct__cms_typehandler_struct), POINTER(None))),
    ('ContextID', cmsContext),
    ('ICCVersion', cmsUInt32Number),
]

cmsTagTypeHandler = struct__cms_typehandler_struct # /usr/include/lcms2_plugin.h: 409

# /usr/include/lcms2_plugin.h: 416
class struct_anon_73(Structure):
    pass

struct_anon_73.__slots__ = [
    'base',
    'Handler',
]
struct_anon_73._fields_ = [
    ('base', cmsPluginBase),
    ('Handler', cmsTagTypeHandler),
]

cmsPluginTagType = struct_anon_73 # /usr/include/lcms2_plugin.h: 416

# /usr/include/lcms2_plugin.h: 434
class struct_anon_74(Structure):
    pass

struct_anon_74.__slots__ = [
    'ElemCount',
    'nSupportedTypes',
    'SupportedTypes',
    'DecideType',
]
struct_anon_74._fields_ = [
    ('ElemCount', cmsUInt32Number),
    ('nSupportedTypes', cmsUInt32Number),
    ('SupportedTypes', cmsTagTypeSignature * 20),
    ('DecideType', CFUNCTYPE(UNCHECKED(cmsTagTypeSignature), cmsFloat64Number, POINTER(None))),
]

cmsTagDescriptor = struct_anon_74 # /usr/include/lcms2_plugin.h: 434

# /usr/include/lcms2_plugin.h: 443
class struct_anon_75(Structure):
    pass

struct_anon_75.__slots__ = [
    'base',
    'Signature',
    'Descriptor',
]
struct_anon_75._fields_ = [
    ('base', cmsPluginBase),
    ('Signature', cmsTagSignature),
    ('Descriptor', cmsTagDescriptor),
]

cmsPluginTag = struct_anon_75 # /usr/include/lcms2_plugin.h: 443

cmsIntentFn = CFUNCTYPE(UNCHECKED(POINTER(cmsPipeline)), cmsContext, cmsUInt32Number, POINTER(cmsUInt32Number), POINTER(cmsHPROFILE), POINTER(cmsBool), POINTER(cmsFloat64Number), cmsUInt32Number) # /usr/include/lcms2_plugin.h: 452

# /usr/include/lcms2_plugin.h: 468
class struct_anon_76(Structure):
    pass

struct_anon_76.__slots__ = [
    'base',
    'Intent',
    'Link',
    'Description',
]
struct_anon_76._fields_ = [
    ('base', cmsPluginBase),
    ('Intent', cmsUInt32Number),
    ('Link', cmsIntentFn),
    ('Description', c_char * 256),
]

cmsPluginRenderingIntent = struct_anon_76 # /usr/include/lcms2_plugin.h: 468

# /usr/include/lcms2_plugin.h: 472
if hasattr(_libs['lcms2'], '_cmsDefaultICCintents'):
    _cmsDefaultICCintents = _libs['lcms2']._cmsDefaultICCintents
    _cmsDefaultICCintents.argtypes = [cmsContext, cmsUInt32Number, POINTER(cmsUInt32Number), POINTER(cmsHPROFILE), POINTER(cmsBool), POINTER(cmsFloat64Number), cmsUInt32Number]
    _cmsDefaultICCintents.restype = POINTER(cmsPipeline)

_cmsStageEvalFn = CFUNCTYPE(UNCHECKED(None), POINTER(cmsFloat32Number), POINTER(cmsFloat32Number), POINTER(cmsStage)) # /usr/include/lcms2_plugin.h: 485

_cmsStageDupElemFn = CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), POINTER(cmsStage)) # /usr/include/lcms2_plugin.h: 486

_cmsStageFreeElemFn = CFUNCTYPE(UNCHECKED(None), POINTER(cmsStage)) # /usr/include/lcms2_plugin.h: 487

# /usr/include/lcms2_plugin.h: 491
if hasattr(_libs['lcms2'], '_cmsStageAllocPlaceholder'):
    _cmsStageAllocPlaceholder = _libs['lcms2']._cmsStageAllocPlaceholder
    _cmsStageAllocPlaceholder.argtypes = [cmsContext, cmsStageSignature, cmsUInt32Number, cmsUInt32Number, _cmsStageEvalFn, _cmsStageDupElemFn, _cmsStageFreeElemFn, POINTER(None)]
    _cmsStageAllocPlaceholder.restype = POINTER(cmsStage)

# /usr/include/lcms2_plugin.h: 503
class struct_anon_77(Structure):
    pass

struct_anon_77.__slots__ = [
    'base',
    'Handler',
]
struct_anon_77._fields_ = [
    ('base', cmsPluginBase),
    ('Handler', cmsTagTypeHandler),
]

cmsPluginMultiProcessElement = struct_anon_77 # /usr/include/lcms2_plugin.h: 503

# /usr/include/lcms2_plugin.h: 513
class struct_anon_78(Structure):
    pass

struct_anon_78.__slots__ = [
    'nCurves',
    'TheCurves',
]
struct_anon_78._fields_ = [
    ('nCurves', cmsUInt32Number),
    ('TheCurves', POINTER(POINTER(cmsToneCurve))),
]

_cmsStageToneCurvesData = struct_anon_78 # /usr/include/lcms2_plugin.h: 513

# /usr/include/lcms2_plugin.h: 520
class struct_anon_79(Structure):
    pass

struct_anon_79.__slots__ = [
    'Double',
    'Offset',
]
struct_anon_79._fields_ = [
    ('Double', POINTER(cmsFloat64Number)),
    ('Offset', POINTER(cmsFloat64Number)),
]

_cmsStageMatrixData = struct_anon_79 # /usr/include/lcms2_plugin.h: 520

# /usr/include/lcms2_plugin.h: 525
class union_anon_80(Union):
    pass

union_anon_80.__slots__ = [
    'T',
    'TFloat',
]
union_anon_80._fields_ = [
    ('T', POINTER(cmsUInt16Number)),
    ('TFloat', POINTER(cmsFloat32Number)),
]

# /usr/include/lcms2_plugin.h: 535
class struct_anon_81(Structure):
    pass

struct_anon_81.__slots__ = [
    'Tab',
    'Params',
    'nEntries',
    'HasFloatValues',
]
struct_anon_81._fields_ = [
    ('Tab', union_anon_80),
    ('Params', POINTER(cmsInterpParams)),
    ('nEntries', cmsUInt32Number),
    ('HasFloatValues', cmsBool),
]

_cmsStageCLutData = struct_anon_81 # /usr/include/lcms2_plugin.h: 535

_cmsOPTeval16Fn = CFUNCTYPE(UNCHECKED(None), POINTER(cmsUInt16Number), POINTER(cmsUInt16Number), POINTER(None)) # /usr/include/lcms2_plugin.h: 544

_cmsOPToptimizeFn = CFUNCTYPE(UNCHECKED(cmsBool), POINTER(POINTER(cmsPipeline)), cmsUInt32Number, POINTER(cmsUInt32Number), POINTER(cmsUInt32Number), POINTER(cmsUInt32Number)) # /usr/include/lcms2_plugin.h: 549

# /usr/include/lcms2_plugin.h: 558
if hasattr(_libs['lcms2'], '_cmsPipelineSetOptimizationParameters'):
    _cmsPipelineSetOptimizationParameters = _libs['lcms2']._cmsPipelineSetOptimizationParameters
    _cmsPipelineSetOptimizationParameters.argtypes = [POINTER(cmsPipeline), _cmsOPTeval16Fn, POINTER(None), _cmsFreeUserDataFn, _cmsDupUserDataFn]
    _cmsPipelineSetOptimizationParameters.restype = None

# /usr/include/lcms2_plugin.h: 570
class struct_anon_82(Structure):
    pass

struct_anon_82.__slots__ = [
    'base',
    'OptimizePtr',
]
struct_anon_82._fields_ = [
    ('base', cmsPluginBase),
    ('OptimizePtr', _cmsOPToptimizeFn),
]

cmsPluginOptimization = struct_anon_82 # /usr/include/lcms2_plugin.h: 570

# /usr/include/lcms2_plugin.h: 581
class struct_anon_83(Structure):
    pass

struct_anon_83.__slots__ = [
    'BytesPerLineIn',
    'BytesPerLineOut',
    'BytesPerPlaneIn',
    'BytesPerPlaneOut',
]
struct_anon_83._fields_ = [
    ('BytesPerLineIn', cmsUInt32Number),
    ('BytesPerLineOut', cmsUInt32Number),
    ('BytesPerPlaneIn', cmsUInt32Number),
    ('BytesPerPlaneOut', cmsUInt32Number),
]

cmsStride = struct_anon_83 # /usr/include/lcms2_plugin.h: 581

_cmsTransformFn = CFUNCTYPE(UNCHECKED(None), POINTER(struct__cmstransform_struct), POINTER(None), POINTER(None), cmsUInt32Number, cmsUInt32Number) # /usr/include/lcms2_plugin.h: 583

_cmsTransform2Fn = CFUNCTYPE(UNCHECKED(None), POINTER(struct__cmstransform_struct), POINTER(None), POINTER(None), cmsUInt32Number, cmsUInt32Number, POINTER(cmsStride)) # /usr/include/lcms2_plugin.h: 590

_cmsTransformFactory = CFUNCTYPE(UNCHECKED(cmsBool), POINTER(_cmsTransformFn), POINTER(POINTER(None)), POINTER(_cmsFreeUserDataFn), POINTER(POINTER(cmsPipeline)), POINTER(cmsUInt32Number), POINTER(cmsUInt32Number), POINTER(cmsUInt32Number)) # /usr/include/lcms2_plugin.h: 597

_cmsTransform2Factory = CFUNCTYPE(UNCHECKED(cmsBool), POINTER(_cmsTransform2Fn), POINTER(POINTER(None)), POINTER(_cmsFreeUserDataFn), POINTER(POINTER(cmsPipeline)), POINTER(cmsUInt32Number), POINTER(cmsUInt32Number), POINTER(cmsUInt32Number)) # /usr/include/lcms2_plugin.h: 605

# /usr/include/lcms2_plugin.h: 615
if hasattr(_libs['lcms2'], '_cmsSetTransformUserData'):
    _cmsSetTransformUserData = _libs['lcms2']._cmsSetTransformUserData
    _cmsSetTransformUserData.argtypes = [POINTER(struct__cmstransform_struct), POINTER(None), _cmsFreeUserDataFn]
    _cmsSetTransformUserData.restype = None

# /usr/include/lcms2_plugin.h: 616
if hasattr(_libs['lcms2'], '_cmsGetTransformUserData'):
    _cmsGetTransformUserData = _libs['lcms2']._cmsGetTransformUserData
    _cmsGetTransformUserData.argtypes = [POINTER(struct__cmstransform_struct)]
    _cmsGetTransformUserData.restype = POINTER(c_ubyte)
    _cmsGetTransformUserData.errcheck = lambda v,*a : cast(v, c_void_p)

# /usr/include/lcms2_plugin.h: 620
if hasattr(_libs['lcms2'], '_cmsGetTransformFormatters16'):
    _cmsGetTransformFormatters16 = _libs['lcms2']._cmsGetTransformFormatters16
    _cmsGetTransformFormatters16.argtypes = [POINTER(struct__cmstransform_struct), POINTER(cmsFormatter16), POINTER(cmsFormatter16)]
    _cmsGetTransformFormatters16.restype = None

# /usr/include/lcms2_plugin.h: 621
if hasattr(_libs['lcms2'], '_cmsGetTransformFormattersFloat'):
    _cmsGetTransformFormattersFloat = _libs['lcms2']._cmsGetTransformFormattersFloat
    _cmsGetTransformFormattersFloat.argtypes = [POINTER(struct__cmstransform_struct), POINTER(cmsFormatterFloat), POINTER(cmsFormatterFloat)]
    _cmsGetTransformFormattersFloat.restype = None

# /usr/include/lcms2_plugin.h: 627
class union_anon_84(Union):
    pass

union_anon_84.__slots__ = [
    'legacy_xform',
    'xform',
]
union_anon_84._fields_ = [
    ('legacy_xform', _cmsTransformFactory),
    ('xform', _cmsTransform2Factory),
]

# /usr/include/lcms2_plugin.h: 632
class struct_anon_85(Structure):
    pass

struct_anon_85.__slots__ = [
    'base',
    'factories',
]
struct_anon_85._fields_ = [
    ('base', cmsPluginBase),
    ('factories', union_anon_84),
]

cmsPluginTransform = struct_anon_85 # /usr/include/lcms2_plugin.h: 632

_cmsCreateMutexFnPtrType = CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), cmsContext) # /usr/include/lcms2_plugin.h: 637

_cmsDestroyMutexFnPtrType = CFUNCTYPE(UNCHECKED(None), cmsContext, POINTER(None)) # /usr/include/lcms2_plugin.h: 638

_cmsLockMutexFnPtrType = CFUNCTYPE(UNCHECKED(cmsBool), cmsContext, POINTER(None)) # /usr/include/lcms2_plugin.h: 639

_cmsUnlockMutexFnPtrType = CFUNCTYPE(UNCHECKED(None), cmsContext, POINTER(None)) # /usr/include/lcms2_plugin.h: 640

# /usr/include/lcms2_plugin.h: 650
class struct_anon_86(Structure):
    pass

struct_anon_86.__slots__ = [
    'base',
    'CreateMutexPtr',
    'DestroyMutexPtr',
    'LockMutexPtr',
    'UnlockMutexPtr',
]
struct_anon_86._fields_ = [
    ('base', cmsPluginBase),
    ('CreateMutexPtr', _cmsCreateMutexFnPtrType),
    ('DestroyMutexPtr', _cmsDestroyMutexFnPtrType),
    ('LockMutexPtr', _cmsLockMutexFnPtrType),
    ('UnlockMutexPtr', _cmsUnlockMutexFnPtrType),
]

cmsPluginMutex = struct_anon_86 # /usr/include/lcms2_plugin.h: 650

# /usr/include/lcms2_plugin.h: 652
if hasattr(_libs['lcms2'], '_cmsCreateMutex'):
    _cmsCreateMutex = _libs['lcms2']._cmsCreateMutex
    _cmsCreateMutex.argtypes = [cmsContext]
    _cmsCreateMutex.restype = POINTER(c_ubyte)
    _cmsCreateMutex.errcheck = lambda v,*a : cast(v, c_void_p)

# /usr/include/lcms2_plugin.h: 653
if hasattr(_libs['lcms2'], '_cmsDestroyMutex'):
    _cmsDestroyMutex = _libs['lcms2']._cmsDestroyMutex
    _cmsDestroyMutex.argtypes = [cmsContext, POINTER(None)]
    _cmsDestroyMutex.restype = None

# /usr/include/lcms2_plugin.h: 654
if hasattr(_libs['lcms2'], '_cmsLockMutex'):
    _cmsLockMutex = _libs['lcms2']._cmsLockMutex
    _cmsLockMutex.argtypes = [cmsContext, POINTER(None)]
    _cmsLockMutex.restype = cmsBool

# /usr/include/lcms2_plugin.h: 655
if hasattr(_libs['lcms2'], '_cmsUnlockMutex'):
    _cmsUnlockMutex = _libs['lcms2']._cmsUnlockMutex
    _cmsUnlockMutex.argtypes = [cmsContext, POINTER(None)]
    _cmsUnlockMutex.restype = None

# /usr/include/lcms2.h: 78
try:
    LCMS_VERSION = 2080
except:
    pass

# /usr/include/lcms2.h: 248
try:
    cmsMAX_PATH = 256
except:
    pass

# /usr/include/lcms2.h: 251
try:
    FALSE = 0
except:
    pass

# /usr/include/lcms2.h: 254
try:
    TRUE = 1
except:
    pass

# /usr/include/lcms2.h: 258
try:
    cmsD50X = 0.9642
except:
    pass

# /usr/include/lcms2.h: 259
try:
    cmsD50Y = 1.0
except:
    pass

# /usr/include/lcms2.h: 260
try:
    cmsD50Z = 0.8249
except:
    pass

# /usr/include/lcms2.h: 263
try:
    cmsPERCEPTUAL_BLACK_X = 0.00336
except:
    pass

# /usr/include/lcms2.h: 264
try:
    cmsPERCEPTUAL_BLACK_Y = 0.0034731
except:
    pass

# /usr/include/lcms2.h: 265
try:
    cmsPERCEPTUAL_BLACK_Z = 0.00287
except:
    pass

# /usr/include/lcms2.h: 268
try:
    cmsMagicNumber = 1633907568
except:
    pass

# /usr/include/lcms2.h: 269
try:
    lcmsSignature = 1818455411
except:
    pass

# /usr/include/lcms2.h: 495
try:
    cmsSigPerceptualReferenceMediumGamut = 1886547303
except:
    pass

# /usr/include/lcms2.h: 498
try:
    cmsSigSceneColorimetryEstimates = 1935896421
except:
    pass

# /usr/include/lcms2.h: 499
try:
    cmsSigSceneAppearanceEstimates = 1935765605
except:
    pass

# /usr/include/lcms2.h: 500
try:
    cmsSigFocalPlaneColorimetryEstimates = 1718641509
except:
    pass

# /usr/include/lcms2.h: 501
try:
    cmsSigReflectionHardcopyOriginalColorimetry = 1919446883
except:
    pass

# /usr/include/lcms2.h: 502
try:
    cmsSigReflectionPrintOutputColorimetry = 1919971171
except:
    pass

# /usr/include/lcms2.h: 542
try:
    cmsSigStatusA = 1400136001
except:
    pass

# /usr/include/lcms2.h: 543
try:
    cmsSigStatusE = 1400136005
except:
    pass

# /usr/include/lcms2.h: 544
try:
    cmsSigStatusI = 1400136009
except:
    pass

# /usr/include/lcms2.h: 545
try:
    cmsSigStatusT = 1400136020
except:
    pass

# /usr/include/lcms2.h: 546
try:
    cmsSigStatusM = 1400136013
except:
    pass

# /usr/include/lcms2.h: 547
try:
    cmsSigDN = 1145970720
except:
    pass

# /usr/include/lcms2.h: 548
try:
    cmsSigDNP = 1145970768
except:
    pass

# /usr/include/lcms2.h: 549
try:
    cmsSigDNN = 1145982496
except:
    pass

# /usr/include/lcms2.h: 550
try:
    cmsSigDNNP = 1145982544
except:
    pass

# /usr/include/lcms2.h: 554
try:
    cmsReflective = 0
except:
    pass

# /usr/include/lcms2.h: 555
try:
    cmsTransparency = 1
except:
    pass

# /usr/include/lcms2.h: 556
try:
    cmsGlossy = 0
except:
    pass

# /usr/include/lcms2.h: 557
try:
    cmsMatte = 2
except:
    pass

# /usr/include/lcms2.h: 646
try:
    cmsMAXCHANNELS = 16
except:
    pass

# /usr/include/lcms2.h: 666
def FLOAT_SH(a):
    return (a << 22)

# /usr/include/lcms2.h: 667
def OPTIMIZED_SH(s):
    return (s << 21)

# /usr/include/lcms2.h: 668
def COLORSPACE_SH(s):
    return (s << 16)

# /usr/include/lcms2.h: 669
def SWAPFIRST_SH(s):
    return (s << 14)

# /usr/include/lcms2.h: 670
def FLAVOR_SH(s):
    return (s << 13)

# /usr/include/lcms2.h: 671
def PLANAR_SH(p):
    return (p << 12)

# /usr/include/lcms2.h: 672
def ENDIAN16_SH(e):
    return (e << 11)

# /usr/include/lcms2.h: 673
def DOSWAP_SH(e):
    return (e << 10)

# /usr/include/lcms2.h: 674
def EXTRA_SH(e):
    return (e << 7)

# /usr/include/lcms2.h: 675
def CHANNELS_SH(c):
    return (c << 3)

# /usr/include/lcms2.h: 676
def BYTES_SH(b):
    return b

# /usr/include/lcms2.h: 679
def T_FLOAT(a):
    return ((a >> 22) & 1)

# /usr/include/lcms2.h: 680
def T_OPTIMIZED(o):
    return ((o >> 21) & 1)

# /usr/include/lcms2.h: 681
def T_COLORSPACE(s):
    return ((s >> 16) & 31)

# /usr/include/lcms2.h: 682
def T_SWAPFIRST(s):
    return ((s >> 14) & 1)

# /usr/include/lcms2.h: 683
def T_FLAVOR(s):
    return ((s >> 13) & 1)

# /usr/include/lcms2.h: 684
def T_PLANAR(p):
    return ((p >> 12) & 1)

# /usr/include/lcms2.h: 685
def T_ENDIAN16(e):
    return ((e >> 11) & 1)

# /usr/include/lcms2.h: 686
def T_DOSWAP(e):
    return ((e >> 10) & 1)

# /usr/include/lcms2.h: 687
def T_EXTRA(e):
    return ((e >> 7) & 7)

# /usr/include/lcms2.h: 688
def T_CHANNELS(c):
    return ((c >> 3) & 15)

# /usr/include/lcms2.h: 689
def T_BYTES(b):
    return (b & 7)

# /usr/include/lcms2.h: 693
try:
    PT_ANY = 0
except:
    pass

# /usr/include/lcms2.h: 695
try:
    PT_GRAY = 3
except:
    pass

# /usr/include/lcms2.h: 696
try:
    PT_RGB = 4
except:
    pass

# /usr/include/lcms2.h: 697
try:
    PT_CMY = 5
except:
    pass

# /usr/include/lcms2.h: 698
try:
    PT_CMYK = 6
except:
    pass

# /usr/include/lcms2.h: 699
try:
    PT_YCbCr = 7
except:
    pass

# /usr/include/lcms2.h: 700
try:
    PT_YUV = 8
except:
    pass

# /usr/include/lcms2.h: 701
try:
    PT_XYZ = 9
except:
    pass

# /usr/include/lcms2.h: 702
try:
    PT_Lab = 10
except:
    pass

# /usr/include/lcms2.h: 703
try:
    PT_YUVK = 11
except:
    pass

# /usr/include/lcms2.h: 704
try:
    PT_HSV = 12
except:
    pass

# /usr/include/lcms2.h: 705
try:
    PT_HLS = 13
except:
    pass

# /usr/include/lcms2.h: 706
try:
    PT_Yxy = 14
except:
    pass

# /usr/include/lcms2.h: 708
try:
    PT_MCH1 = 15
except:
    pass

# /usr/include/lcms2.h: 709
try:
    PT_MCH2 = 16
except:
    pass

# /usr/include/lcms2.h: 710
try:
    PT_MCH3 = 17
except:
    pass

# /usr/include/lcms2.h: 711
try:
    PT_MCH4 = 18
except:
    pass

# /usr/include/lcms2.h: 712
try:
    PT_MCH5 = 19
except:
    pass

# /usr/include/lcms2.h: 713
try:
    PT_MCH6 = 20
except:
    pass

# /usr/include/lcms2.h: 714
try:
    PT_MCH7 = 21
except:
    pass

# /usr/include/lcms2.h: 715
try:
    PT_MCH8 = 22
except:
    pass

# /usr/include/lcms2.h: 716
try:
    PT_MCH9 = 23
except:
    pass

# /usr/include/lcms2.h: 717
try:
    PT_MCH10 = 24
except:
    pass

# /usr/include/lcms2.h: 718
try:
    PT_MCH11 = 25
except:
    pass

# /usr/include/lcms2.h: 719
try:
    PT_MCH12 = 26
except:
    pass

# /usr/include/lcms2.h: 720
try:
    PT_MCH13 = 27
except:
    pass

# /usr/include/lcms2.h: 721
try:
    PT_MCH14 = 28
except:
    pass

# /usr/include/lcms2.h: 722
try:
    PT_MCH15 = 29
except:
    pass

# /usr/include/lcms2.h: 724
try:
    PT_LabV2 = 30
except:
    pass

# /usr/include/lcms2.h: 731
try:
    TYPE_GRAY_8 = (((COLORSPACE_SH (PT_GRAY)) | (CHANNELS_SH (1))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 732
try:
    TYPE_GRAY_8_REV = ((((COLORSPACE_SH (PT_GRAY)) | (CHANNELS_SH (1))) | (BYTES_SH (1))) | (FLAVOR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 733
try:
    TYPE_GRAY_16 = (((COLORSPACE_SH (PT_GRAY)) | (CHANNELS_SH (1))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 734
try:
    TYPE_GRAY_16_REV = ((((COLORSPACE_SH (PT_GRAY)) | (CHANNELS_SH (1))) | (BYTES_SH (2))) | (FLAVOR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 735
try:
    TYPE_GRAY_16_SE = ((((COLORSPACE_SH (PT_GRAY)) | (CHANNELS_SH (1))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 736
try:
    TYPE_GRAYA_8 = ((((COLORSPACE_SH (PT_GRAY)) | (EXTRA_SH (1))) | (CHANNELS_SH (1))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 737
try:
    TYPE_GRAYA_16 = ((((COLORSPACE_SH (PT_GRAY)) | (EXTRA_SH (1))) | (CHANNELS_SH (1))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 738
try:
    TYPE_GRAYA_16_SE = (((((COLORSPACE_SH (PT_GRAY)) | (EXTRA_SH (1))) | (CHANNELS_SH (1))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 739
try:
    TYPE_GRAYA_8_PLANAR = (((((COLORSPACE_SH (PT_GRAY)) | (EXTRA_SH (1))) | (CHANNELS_SH (1))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 740
try:
    TYPE_GRAYA_16_PLANAR = (((((COLORSPACE_SH (PT_GRAY)) | (EXTRA_SH (1))) | (CHANNELS_SH (1))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 742
try:
    TYPE_RGB_8 = (((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 743
try:
    TYPE_RGB_8_PLANAR = ((((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 744
try:
    TYPE_BGR_8 = ((((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 745
try:
    TYPE_BGR_8_PLANAR = (((((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (DOSWAP_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 746
try:
    TYPE_RGB_16 = (((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 747
try:
    TYPE_RGB_16_PLANAR = ((((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 748
try:
    TYPE_RGB_16_SE = ((((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 749
try:
    TYPE_BGR_16 = ((((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 750
try:
    TYPE_BGR_16_PLANAR = (((((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 751
try:
    TYPE_BGR_16_SE = (((((COLORSPACE_SH (PT_RGB)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 753
try:
    TYPE_RGBA_8 = ((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 754
try:
    TYPE_RGBA_8_PLANAR = (((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 755
try:
    TYPE_RGBA_16 = ((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 756
try:
    TYPE_RGBA_16_PLANAR = (((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 757
try:
    TYPE_RGBA_16_SE = (((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 759
try:
    TYPE_ARGB_8 = (((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 760
try:
    TYPE_ARGB_8_PLANAR = ((((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (SWAPFIRST_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 761
try:
    TYPE_ARGB_16 = (((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 763
try:
    TYPE_ABGR_8 = (((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 764
try:
    TYPE_ABGR_8_PLANAR = ((((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (DOSWAP_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 765
try:
    TYPE_ABGR_16 = (((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 766
try:
    TYPE_ABGR_16_PLANAR = ((((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 767
try:
    TYPE_ABGR_16_SE = ((((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 769
try:
    TYPE_BGRA_8 = ((((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (DOSWAP_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 770
try:
    TYPE_BGRA_8_PLANAR = (((((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (DOSWAP_SH (1))) | (SWAPFIRST_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 771
try:
    TYPE_BGRA_16 = ((((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 772
try:
    TYPE_BGRA_16_SE = (((((((COLORSPACE_SH (PT_RGB)) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (ENDIAN16_SH (1))) | (DOSWAP_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 774
try:
    TYPE_CMY_8 = (((COLORSPACE_SH (PT_CMY)) | (CHANNELS_SH (3))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 775
try:
    TYPE_CMY_8_PLANAR = ((((COLORSPACE_SH (PT_CMY)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 776
try:
    TYPE_CMY_16 = (((COLORSPACE_SH (PT_CMY)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 777
try:
    TYPE_CMY_16_PLANAR = ((((COLORSPACE_SH (PT_CMY)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 778
try:
    TYPE_CMY_16_SE = ((((COLORSPACE_SH (PT_CMY)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 780
try:
    TYPE_CMYK_8 = (((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 781
try:
    TYPE_CMYKA_8 = ((((COLORSPACE_SH (PT_CMYK)) | (EXTRA_SH (1))) | (CHANNELS_SH (4))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 782
try:
    TYPE_CMYK_8_REV = ((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (1))) | (FLAVOR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 783
try:
    TYPE_YUVK_8 = TYPE_CMYK_8_REV
except:
    pass

# /usr/include/lcms2.h: 784
try:
    TYPE_CMYK_8_PLANAR = ((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 785
try:
    TYPE_CMYK_16 = (((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 786
try:
    TYPE_CMYK_16_REV = ((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (2))) | (FLAVOR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 787
try:
    TYPE_YUVK_16 = TYPE_CMYK_16_REV
except:
    pass

# /usr/include/lcms2.h: 788
try:
    TYPE_CMYK_16_PLANAR = ((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 789
try:
    TYPE_CMYK_16_SE = ((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 791
try:
    TYPE_KYMC_8 = ((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 792
try:
    TYPE_KYMC_16 = ((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 793
try:
    TYPE_KYMC_16_SE = (((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 795
try:
    TYPE_KCMY_8 = ((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 796
try:
    TYPE_KCMY_8_REV = (((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (1))) | (FLAVOR_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 797
try:
    TYPE_KCMY_16 = ((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (2))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 798
try:
    TYPE_KCMY_16_REV = (((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (2))) | (FLAVOR_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 799
try:
    TYPE_KCMY_16_SE = (((((COLORSPACE_SH (PT_CMYK)) | (CHANNELS_SH (4))) | (BYTES_SH (2))) | (ENDIAN16_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 801
try:
    TYPE_CMYK5_8 = (((COLORSPACE_SH (PT_MCH5)) | (CHANNELS_SH (5))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 802
try:
    TYPE_CMYK5_16 = (((COLORSPACE_SH (PT_MCH5)) | (CHANNELS_SH (5))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 803
try:
    TYPE_CMYK5_16_SE = ((((COLORSPACE_SH (PT_MCH5)) | (CHANNELS_SH (5))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 804
try:
    TYPE_KYMC5_8 = ((((COLORSPACE_SH (PT_MCH5)) | (CHANNELS_SH (5))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 805
try:
    TYPE_KYMC5_16 = ((((COLORSPACE_SH (PT_MCH5)) | (CHANNELS_SH (5))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 806
try:
    TYPE_KYMC5_16_SE = (((((COLORSPACE_SH (PT_MCH5)) | (CHANNELS_SH (5))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 807
try:
    TYPE_CMYK6_8 = (((COLORSPACE_SH (PT_MCH6)) | (CHANNELS_SH (6))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 808
try:
    TYPE_CMYK6_8_PLANAR = ((((COLORSPACE_SH (PT_MCH6)) | (CHANNELS_SH (6))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 809
try:
    TYPE_CMYK6_16 = (((COLORSPACE_SH (PT_MCH6)) | (CHANNELS_SH (6))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 810
try:
    TYPE_CMYK6_16_PLANAR = ((((COLORSPACE_SH (PT_MCH6)) | (CHANNELS_SH (6))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 811
try:
    TYPE_CMYK6_16_SE = ((((COLORSPACE_SH (PT_MCH6)) | (CHANNELS_SH (6))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 812
try:
    TYPE_CMYK7_8 = (((COLORSPACE_SH (PT_MCH7)) | (CHANNELS_SH (7))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 813
try:
    TYPE_CMYK7_16 = (((COLORSPACE_SH (PT_MCH7)) | (CHANNELS_SH (7))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 814
try:
    TYPE_CMYK7_16_SE = ((((COLORSPACE_SH (PT_MCH7)) | (CHANNELS_SH (7))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 815
try:
    TYPE_KYMC7_8 = ((((COLORSPACE_SH (PT_MCH7)) | (CHANNELS_SH (7))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 816
try:
    TYPE_KYMC7_16 = ((((COLORSPACE_SH (PT_MCH7)) | (CHANNELS_SH (7))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 817
try:
    TYPE_KYMC7_16_SE = (((((COLORSPACE_SH (PT_MCH7)) | (CHANNELS_SH (7))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 818
try:
    TYPE_CMYK8_8 = (((COLORSPACE_SH (PT_MCH8)) | (CHANNELS_SH (8))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 819
try:
    TYPE_CMYK8_16 = (((COLORSPACE_SH (PT_MCH8)) | (CHANNELS_SH (8))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 820
try:
    TYPE_CMYK8_16_SE = ((((COLORSPACE_SH (PT_MCH8)) | (CHANNELS_SH (8))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 821
try:
    TYPE_KYMC8_8 = ((((COLORSPACE_SH (PT_MCH8)) | (CHANNELS_SH (8))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 822
try:
    TYPE_KYMC8_16 = ((((COLORSPACE_SH (PT_MCH8)) | (CHANNELS_SH (8))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 823
try:
    TYPE_KYMC8_16_SE = (((((COLORSPACE_SH (PT_MCH8)) | (CHANNELS_SH (8))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 824
try:
    TYPE_CMYK9_8 = (((COLORSPACE_SH (PT_MCH9)) | (CHANNELS_SH (9))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 825
try:
    TYPE_CMYK9_16 = (((COLORSPACE_SH (PT_MCH9)) | (CHANNELS_SH (9))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 826
try:
    TYPE_CMYK9_16_SE = ((((COLORSPACE_SH (PT_MCH9)) | (CHANNELS_SH (9))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 827
try:
    TYPE_KYMC9_8 = ((((COLORSPACE_SH (PT_MCH9)) | (CHANNELS_SH (9))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 828
try:
    TYPE_KYMC9_16 = ((((COLORSPACE_SH (PT_MCH9)) | (CHANNELS_SH (9))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 829
try:
    TYPE_KYMC9_16_SE = (((((COLORSPACE_SH (PT_MCH9)) | (CHANNELS_SH (9))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 830
try:
    TYPE_CMYK10_8 = (((COLORSPACE_SH (PT_MCH10)) | (CHANNELS_SH (10))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 831
try:
    TYPE_CMYK10_16 = (((COLORSPACE_SH (PT_MCH10)) | (CHANNELS_SH (10))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 832
try:
    TYPE_CMYK10_16_SE = ((((COLORSPACE_SH (PT_MCH10)) | (CHANNELS_SH (10))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 833
try:
    TYPE_KYMC10_8 = ((((COLORSPACE_SH (PT_MCH10)) | (CHANNELS_SH (10))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 834
try:
    TYPE_KYMC10_16 = ((((COLORSPACE_SH (PT_MCH10)) | (CHANNELS_SH (10))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 835
try:
    TYPE_KYMC10_16_SE = (((((COLORSPACE_SH (PT_MCH10)) | (CHANNELS_SH (10))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 836
try:
    TYPE_CMYK11_8 = (((COLORSPACE_SH (PT_MCH11)) | (CHANNELS_SH (11))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 837
try:
    TYPE_CMYK11_16 = (((COLORSPACE_SH (PT_MCH11)) | (CHANNELS_SH (11))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 838
try:
    TYPE_CMYK11_16_SE = ((((COLORSPACE_SH (PT_MCH11)) | (CHANNELS_SH (11))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 839
try:
    TYPE_KYMC11_8 = ((((COLORSPACE_SH (PT_MCH11)) | (CHANNELS_SH (11))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 840
try:
    TYPE_KYMC11_16 = ((((COLORSPACE_SH (PT_MCH11)) | (CHANNELS_SH (11))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 841
try:
    TYPE_KYMC11_16_SE = (((((COLORSPACE_SH (PT_MCH11)) | (CHANNELS_SH (11))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 842
try:
    TYPE_CMYK12_8 = (((COLORSPACE_SH (PT_MCH12)) | (CHANNELS_SH (12))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 843
try:
    TYPE_CMYK12_16 = (((COLORSPACE_SH (PT_MCH12)) | (CHANNELS_SH (12))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 844
try:
    TYPE_CMYK12_16_SE = ((((COLORSPACE_SH (PT_MCH12)) | (CHANNELS_SH (12))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 845
try:
    TYPE_KYMC12_8 = ((((COLORSPACE_SH (PT_MCH12)) | (CHANNELS_SH (12))) | (BYTES_SH (1))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 846
try:
    TYPE_KYMC12_16 = ((((COLORSPACE_SH (PT_MCH12)) | (CHANNELS_SH (12))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 847
try:
    TYPE_KYMC12_16_SE = (((((COLORSPACE_SH (PT_MCH12)) | (CHANNELS_SH (12))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 850
try:
    TYPE_XYZ_16 = (((COLORSPACE_SH (PT_XYZ)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 851
try:
    TYPE_Lab_8 = (((COLORSPACE_SH (PT_Lab)) | (CHANNELS_SH (3))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 852
try:
    TYPE_LabV2_8 = (((COLORSPACE_SH (PT_LabV2)) | (CHANNELS_SH (3))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 854
try:
    TYPE_ALab_8 = (((((COLORSPACE_SH (PT_Lab)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (EXTRA_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 855
try:
    TYPE_ALabV2_8 = (((((COLORSPACE_SH (PT_LabV2)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (EXTRA_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 856
try:
    TYPE_Lab_16 = (((COLORSPACE_SH (PT_Lab)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 857
try:
    TYPE_LabV2_16 = (((COLORSPACE_SH (PT_LabV2)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 858
try:
    TYPE_Yxy_16 = (((COLORSPACE_SH (PT_Yxy)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 861
try:
    TYPE_YCbCr_8 = (((COLORSPACE_SH (PT_YCbCr)) | (CHANNELS_SH (3))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 862
try:
    TYPE_YCbCr_8_PLANAR = ((((COLORSPACE_SH (PT_YCbCr)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 863
try:
    TYPE_YCbCr_16 = (((COLORSPACE_SH (PT_YCbCr)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 864
try:
    TYPE_YCbCr_16_PLANAR = ((((COLORSPACE_SH (PT_YCbCr)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 865
try:
    TYPE_YCbCr_16_SE = ((((COLORSPACE_SH (PT_YCbCr)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 868
try:
    TYPE_YUV_8 = (((COLORSPACE_SH (PT_YUV)) | (CHANNELS_SH (3))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 869
try:
    TYPE_YUV_8_PLANAR = ((((COLORSPACE_SH (PT_YUV)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 870
try:
    TYPE_YUV_16 = (((COLORSPACE_SH (PT_YUV)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 871
try:
    TYPE_YUV_16_PLANAR = ((((COLORSPACE_SH (PT_YUV)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 872
try:
    TYPE_YUV_16_SE = ((((COLORSPACE_SH (PT_YUV)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 875
try:
    TYPE_HLS_8 = (((COLORSPACE_SH (PT_HLS)) | (CHANNELS_SH (3))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 876
try:
    TYPE_HLS_8_PLANAR = ((((COLORSPACE_SH (PT_HLS)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 877
try:
    TYPE_HLS_16 = (((COLORSPACE_SH (PT_HLS)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 878
try:
    TYPE_HLS_16_PLANAR = ((((COLORSPACE_SH (PT_HLS)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 879
try:
    TYPE_HLS_16_SE = ((((COLORSPACE_SH (PT_HLS)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 882
try:
    TYPE_HSV_8 = (((COLORSPACE_SH (PT_HSV)) | (CHANNELS_SH (3))) | (BYTES_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 883
try:
    TYPE_HSV_8_PLANAR = ((((COLORSPACE_SH (PT_HSV)) | (CHANNELS_SH (3))) | (BYTES_SH (1))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 884
try:
    TYPE_HSV_16 = (((COLORSPACE_SH (PT_HSV)) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 885
try:
    TYPE_HSV_16_PLANAR = ((((COLORSPACE_SH (PT_HSV)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (PLANAR_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 886
try:
    TYPE_HSV_16_SE = ((((COLORSPACE_SH (PT_HSV)) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (ENDIAN16_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 889
try:
    TYPE_NAMED_COLOR_INDEX = ((CHANNELS_SH (1)) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 892
try:
    TYPE_XYZ_FLT = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_XYZ))) | (CHANNELS_SH (3))) | (BYTES_SH (4)))
except:
    pass

# /usr/include/lcms2.h: 893
try:
    TYPE_Lab_FLT = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_Lab))) | (CHANNELS_SH (3))) | (BYTES_SH (4)))
except:
    pass

# /usr/include/lcms2.h: 894
try:
    TYPE_LabA_FLT = (((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_Lab))) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (4)))
except:
    pass

# /usr/include/lcms2.h: 895
try:
    TYPE_GRAY_FLT = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_GRAY))) | (CHANNELS_SH (1))) | (BYTES_SH (4)))
except:
    pass

# /usr/include/lcms2.h: 896
try:
    TYPE_RGB_FLT = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (CHANNELS_SH (3))) | (BYTES_SH (4)))
except:
    pass

# /usr/include/lcms2.h: 898
try:
    TYPE_RGBA_FLT = (((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (4)))
except:
    pass

# /usr/include/lcms2.h: 899
try:
    TYPE_ARGB_FLT = ((((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (4))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 900
try:
    TYPE_BGR_FLT = (((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (CHANNELS_SH (3))) | (BYTES_SH (4))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 901
try:
    TYPE_BGRA_FLT = (((((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (4))) | (DOSWAP_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 902
try:
    TYPE_ABGR_FLT = ((((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (4))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 904
try:
    TYPE_CMYK_FLT = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_CMYK))) | (CHANNELS_SH (4))) | (BYTES_SH (4)))
except:
    pass

# /usr/include/lcms2.h: 908
try:
    TYPE_XYZ_DBL = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_XYZ))) | (CHANNELS_SH (3))) | (BYTES_SH (0)))
except:
    pass

# /usr/include/lcms2.h: 909
try:
    TYPE_Lab_DBL = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_Lab))) | (CHANNELS_SH (3))) | (BYTES_SH (0)))
except:
    pass

# /usr/include/lcms2.h: 910
try:
    TYPE_GRAY_DBL = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_GRAY))) | (CHANNELS_SH (1))) | (BYTES_SH (0)))
except:
    pass

# /usr/include/lcms2.h: 911
try:
    TYPE_RGB_DBL = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (CHANNELS_SH (3))) | (BYTES_SH (0)))
except:
    pass

# /usr/include/lcms2.h: 912
try:
    TYPE_BGR_DBL = (((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (CHANNELS_SH (3))) | (BYTES_SH (0))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 913
try:
    TYPE_CMYK_DBL = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_CMYK))) | (CHANNELS_SH (4))) | (BYTES_SH (0)))
except:
    pass

# /usr/include/lcms2.h: 916
try:
    TYPE_GRAY_HALF_FLT = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_GRAY))) | (CHANNELS_SH (1))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 917
try:
    TYPE_RGB_HALF_FLT = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 918
try:
    TYPE_RGBA_HALF_FLT = (((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 919
try:
    TYPE_CMYK_HALF_FLT = ((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_CMYK))) | (CHANNELS_SH (4))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 921
try:
    TYPE_RGBA_HALF_FLT = (((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2)))
except:
    pass

# /usr/include/lcms2.h: 922
try:
    TYPE_ARGB_HALF_FLT = ((((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 923
try:
    TYPE_BGR_HALF_FLT = (((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 924
try:
    TYPE_BGRA_HALF_FLT = (((((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (EXTRA_SH (1))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1))) | (SWAPFIRST_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 925
try:
    TYPE_ABGR_HALF_FLT = (((((FLOAT_SH (1)) | (COLORSPACE_SH (PT_RGB))) | (CHANNELS_SH (3))) | (BYTES_SH (2))) | (DOSWAP_SH (1)))
except:
    pass

# /usr/include/lcms2.h: 980
try:
    cmsILLUMINANT_TYPE_UNKNOWN = 0
except:
    pass

# /usr/include/lcms2.h: 981
try:
    cmsILLUMINANT_TYPE_D50 = 1
except:
    pass

# /usr/include/lcms2.h: 982
try:
    cmsILLUMINANT_TYPE_D65 = 2
except:
    pass

# /usr/include/lcms2.h: 983
try:
    cmsILLUMINANT_TYPE_D93 = 3
except:
    pass

# /usr/include/lcms2.h: 984
try:
    cmsILLUMINANT_TYPE_F2 = 4
except:
    pass

# /usr/include/lcms2.h: 985
try:
    cmsILLUMINANT_TYPE_D55 = 5
except:
    pass

# /usr/include/lcms2.h: 986
try:
    cmsILLUMINANT_TYPE_A = 6
except:
    pass

# /usr/include/lcms2.h: 987
try:
    cmsILLUMINANT_TYPE_E = 7
except:
    pass

# /usr/include/lcms2.h: 988
try:
    cmsILLUMINANT_TYPE_F8 = 8
except:
    pass

# /usr/include/lcms2.h: 1047
try:
    cmsERROR_UNDEFINED = 0
except:
    pass

# /usr/include/lcms2.h: 1048
try:
    cmsERROR_FILE = 1
except:
    pass

# /usr/include/lcms2.h: 1049
try:
    cmsERROR_RANGE = 2
except:
    pass

# /usr/include/lcms2.h: 1050
try:
    cmsERROR_INTERNAL = 3
except:
    pass

# /usr/include/lcms2.h: 1051
try:
    cmsERROR_NULL = 4
except:
    pass

# /usr/include/lcms2.h: 1052
try:
    cmsERROR_READ = 5
except:
    pass

# /usr/include/lcms2.h: 1053
try:
    cmsERROR_SEEK = 6
except:
    pass

# /usr/include/lcms2.h: 1054
try:
    cmsERROR_WRITE = 7
except:
    pass

# /usr/include/lcms2.h: 1055
try:
    cmsERROR_UNKNOWN_EXTENSION = 8
except:
    pass

# /usr/include/lcms2.h: 1056
try:
    cmsERROR_COLORSPACE_CHECK = 9
except:
    pass

# /usr/include/lcms2.h: 1057
try:
    cmsERROR_ALREADY_DEFINED = 10
except:
    pass

# /usr/include/lcms2.h: 1058
try:
    cmsERROR_BAD_SIGNATURE = 11
except:
    pass

# /usr/include/lcms2.h: 1059
try:
    cmsERROR_CORRUPTION_DETECTED = 12
except:
    pass

# /usr/include/lcms2.h: 1060
try:
    cmsERROR_NOT_SUITABLE = 13
except:
    pass

# /usr/include/lcms2.h: 1117
try:
    AVG_SURROUND = 1
except:
    pass

# /usr/include/lcms2.h: 1118
try:
    DIM_SURROUND = 2
except:
    pass

# /usr/include/lcms2.h: 1119
try:
    DARK_SURROUND = 3
except:
    pass

# /usr/include/lcms2.h: 1120
try:
    CUTSHEET_SURROUND = 4
except:
    pass

# /usr/include/lcms2.h: 1122
try:
    D_CALCULATE = (-1)
except:
    pass

# /usr/include/lcms2.h: 1251
try:
    SAMPLER_INSPECT = 16777216
except:
    pass

# /usr/include/lcms2.h: 1268
try:
    cmsNoLanguage = '\x00\x00'
except:
    pass

# /usr/include/lcms2.h: 1269
try:
    cmsNoCountry = '\x00\x00'
except:
    pass

# /usr/include/lcms2.h: 1312
try:
    cmsPRINTER_DEFAULT_SCREENS = 1
except:
    pass

# /usr/include/lcms2.h: 1313
try:
    cmsFREQUENCE_UNITS_LINES_CM = 0
except:
    pass

# /usr/include/lcms2.h: 1314
try:
    cmsFREQUENCE_UNITS_LINES_INCH = 2
except:
    pass

# /usr/include/lcms2.h: 1316
try:
    cmsSPOT_UNKNOWN = 0
except:
    pass

# /usr/include/lcms2.h: 1317
try:
    cmsSPOT_PRINTER_DEFAULT = 1
except:
    pass

# /usr/include/lcms2.h: 1318
try:
    cmsSPOT_ROUND = 2
except:
    pass

# /usr/include/lcms2.h: 1319
try:
    cmsSPOT_DIAMOND = 3
except:
    pass

# /usr/include/lcms2.h: 1320
try:
    cmsSPOT_ELLIPSE = 4
except:
    pass

# /usr/include/lcms2.h: 1321
try:
    cmsSPOT_LINE = 5
except:
    pass

# /usr/include/lcms2.h: 1322
try:
    cmsSPOT_SQUARE = 6
except:
    pass

# /usr/include/lcms2.h: 1323
try:
    cmsSPOT_CROSS = 7
except:
    pass

# /usr/include/lcms2.h: 1437
try:
    cmsEmbeddedProfileFalse = 0
except:
    pass

# /usr/include/lcms2.h: 1438
try:
    cmsEmbeddedProfileTrue = 1
except:
    pass

# /usr/include/lcms2.h: 1439
try:
    cmsUseAnywhere = 0
except:
    pass

# /usr/include/lcms2.h: 1440
try:
    cmsUseWithEmbeddedDataOnly = 2
except:
    pass

# /usr/include/lcms2.h: 1474
try:
    LCMS_USED_AS_INPUT = 0
except:
    pass

# /usr/include/lcms2.h: 1475
try:
    LCMS_USED_AS_OUTPUT = 1
except:
    pass

# /usr/include/lcms2.h: 1476
try:
    LCMS_USED_AS_PROOF = 2
except:
    pass

# /usr/include/lcms2.h: 1609
try:
    INTENT_PERCEPTUAL = 0
except:
    pass

# /usr/include/lcms2.h: 1610
try:
    INTENT_RELATIVE_COLORIMETRIC = 1
except:
    pass

# /usr/include/lcms2.h: 1611
try:
    INTENT_SATURATION = 2
except:
    pass

# /usr/include/lcms2.h: 1612
try:
    INTENT_ABSOLUTE_COLORIMETRIC = 3
except:
    pass

# /usr/include/lcms2.h: 1615
try:
    INTENT_PRESERVE_K_ONLY_PERCEPTUAL = 10
except:
    pass

# /usr/include/lcms2.h: 1616
try:
    INTENT_PRESERVE_K_ONLY_RELATIVE_COLORIMETRIC = 11
except:
    pass

# /usr/include/lcms2.h: 1617
try:
    INTENT_PRESERVE_K_ONLY_SATURATION = 12
except:
    pass

# /usr/include/lcms2.h: 1618
try:
    INTENT_PRESERVE_K_PLANE_PERCEPTUAL = 13
except:
    pass

# /usr/include/lcms2.h: 1619
try:
    INTENT_PRESERVE_K_PLANE_RELATIVE_COLORIMETRIC = 14
except:
    pass

# /usr/include/lcms2.h: 1620
try:
    INTENT_PRESERVE_K_PLANE_SATURATION = 15
except:
    pass

# /usr/include/lcms2.h: 1628
try:
    cmsFLAGS_NOCACHE = 64
except:
    pass

# /usr/include/lcms2.h: 1629
try:
    cmsFLAGS_NOOPTIMIZE = 256
except:
    pass

# /usr/include/lcms2.h: 1630
try:
    cmsFLAGS_NULLTRANSFORM = 512
except:
    pass

# /usr/include/lcms2.h: 1633
try:
    cmsFLAGS_GAMUTCHECK = 4096
except:
    pass

# /usr/include/lcms2.h: 1634
try:
    cmsFLAGS_SOFTPROOFING = 16384
except:
    pass

# /usr/include/lcms2.h: 1637
try:
    cmsFLAGS_BLACKPOINTCOMPENSATION = 8192
except:
    pass

# /usr/include/lcms2.h: 1638
try:
    cmsFLAGS_NOWHITEONWHITEFIXUP = 4
except:
    pass

# /usr/include/lcms2.h: 1639
try:
    cmsFLAGS_HIGHRESPRECALC = 1024
except:
    pass

# /usr/include/lcms2.h: 1640
try:
    cmsFLAGS_LOWRESPRECALC = 2048
except:
    pass

# /usr/include/lcms2.h: 1643
try:
    cmsFLAGS_8BITS_DEVICELINK = 8
except:
    pass

# /usr/include/lcms2.h: 1644
try:
    cmsFLAGS_GUESSDEVICECLASS = 32
except:
    pass

# /usr/include/lcms2.h: 1645
try:
    cmsFLAGS_KEEP_SEQUENCE = 128
except:
    pass

# /usr/include/lcms2.h: 1648
try:
    cmsFLAGS_FORCE_CLUT = 2
except:
    pass

# /usr/include/lcms2.h: 1649
try:
    cmsFLAGS_CLUT_POST_LINEARIZATION = 1
except:
    pass

# /usr/include/lcms2.h: 1650
try:
    cmsFLAGS_CLUT_PRE_LINEARIZATION = 16
except:
    pass

# /usr/include/lcms2.h: 1653
try:
    cmsFLAGS_NONEGATIVES = 32768
except:
    pass

# /usr/include/lcms2.h: 1656
try:
    cmsFLAGS_COPY_ALPHA = 67108864
except:
    pass

# /usr/include/lcms2.h: 1659
def cmsFLAGS_GRIDPOINTS(n):
    return ((n & 255) << 16)

# /usr/include/lcms2.h: 1662
try:
    cmsFLAGS_NODEFAULTRESOURCEDEF = 16777216
except:
    pass

# /usr/include/lcms2_plugin.h: 66
try:
    VX = 0
except:
    pass

# /usr/include/lcms2_plugin.h: 67
try:
    VY = 1
except:
    pass

# /usr/include/lcms2_plugin.h: 68
try:
    VZ = 2
except:
    pass

# /usr/include/lcms2_plugin.h: 193
try:
    cmsPluginMagicNumber = 1633906800
except:
    pass

# /usr/include/lcms2_plugin.h: 195
try:
    cmsPluginMemHandlerSig = 1835363656
except:
    pass

# /usr/include/lcms2_plugin.h: 196
try:
    cmsPluginInterpolationSig = 1768845384
except:
    pass

# /usr/include/lcms2_plugin.h: 197
try:
    cmsPluginParametricCurveSig = 1885434440
except:
    pass

# /usr/include/lcms2_plugin.h: 198
try:
    cmsPluginFormattersSig = 1718775112
except:
    pass

# /usr/include/lcms2_plugin.h: 199
try:
    cmsPluginTagTypeSig = 1954115656
except:
    pass

# /usr/include/lcms2_plugin.h: 200
try:
    cmsPluginTagSig = 1952540488
except:
    pass

# /usr/include/lcms2_plugin.h: 201
try:
    cmsPluginRenderingIntentSig = 1768846408
except:
    pass

# /usr/include/lcms2_plugin.h: 202
try:
    cmsPluginMultiProcessElementSig = 1836082504
except:
    pass

# /usr/include/lcms2_plugin.h: 203
try:
    cmsPluginOptimizationSig = 1869640776
except:
    pass

# /usr/include/lcms2_plugin.h: 204
try:
    cmsPluginTransformSig = 2053533000
except:
    pass

# /usr/include/lcms2_plugin.h: 205
try:
    cmsPluginMutexSig = 1836350024
except:
    pass

# /usr/include/lcms2_plugin.h: 217
try:
    MAX_TYPES_IN_LCMS_PLUGIN = 20
except:
    pass

# /usr/include/lcms2_plugin.h: 278
try:
    CMS_LERP_FLAGS_16BITS = 0
except:
    pass

# /usr/include/lcms2_plugin.h: 279
try:
    CMS_LERP_FLAGS_FLOAT = 1
except:
    pass

# /usr/include/lcms2_plugin.h: 280
try:
    CMS_LERP_FLAGS_TRILINEAR = 256
except:
    pass

# /usr/include/lcms2_plugin.h: 283
try:
    MAX_INPUT_DIMENSIONS = 8
except:
    pass

# /usr/include/lcms2_plugin.h: 360
try:
    CMS_PACK_FLAGS_16BITS = 0
except:
    pass

# /usr/include/lcms2_plugin.h: 361
try:
    CMS_PACK_FLAGS_FLOAT = 1
except:
    pass

_cmsContext_struct = struct__cmsContext_struct # /usr/include/lcms2.h: 1021

_cms_curve_struct = struct__cms_curve_struct # /usr/include/lcms2.h: 1154

_cmsPipeline_struct = struct__cmsPipeline_struct # /usr/include/lcms2.h: 1185

_cmsStage_struct = struct__cmsStage_struct # /usr/include/lcms2.h: 1186

_cms_MLU_struct = struct__cms_MLU_struct # /usr/include/lcms2.h: 1266

_cms_NAMEDCOLORLIST_struct = struct__cms_NAMEDCOLORLIST_struct # /usr/include/lcms2.h: 1342

_cmsDICTentry_struct = struct__cmsDICTentry_struct # /usr/include/lcms2.h: 1399

_cms_io_handler = struct__cms_io_handler # /usr/include/lcms2_plugin.h: 112

_cmsPluginBaseStruct = struct__cmsPluginBaseStruct # /usr/include/lcms2_plugin.h: 207

_cms_interp_struc = struct__cms_interp_struc # /usr/include/lcms2_plugin.h: 285

_cmstransform_struct = struct__cmstransform_struct # /usr/include/lcms2_plugin.h: 341

_cms_typehandler_struct = struct__cms_typehandler_struct # /usr/include/lcms2_plugin.h: 380

# No inserted files

