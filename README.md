## notes:

`talon` is not compatible with Python 3

`pyml` is required for `talon` to install properly:

    $ curl -L http://sourceforge.net/projects/pyml/files/latest/download?source=typ_redirect > PyML.tar.gz;
    $ tar -xzf PyML.tar.gz && cd PyML-* && python setup.py build && python setup.py install && rm -rf PyML.tar.gz;