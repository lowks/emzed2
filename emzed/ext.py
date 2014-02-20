import sys

# rescan moudles and packages on sys.path:

import pkg_resources
reload(pkg_resources)  # migh be loaded already and is not up to date

_loaded = []

for ep in pkg_resources.iter_entry_points("emzed_package", name="extension"):
    pkg = ep.load()
    _loaded.append(ep.module_name)
    exec "%s=pkg" % ep.module_name
    sys.modules["emzed.ext.%s" % ep.module_name] = pkg
    del ep
    del pkg

if _loaded:
    print
    print "LOADED EMZED EXTENSIONS: ".ljust(80, "-")
    print
    for l in _loaded:
        print "loaded", l
    print
    print "-" * 80

del pkg_resources
del sys
