## notes:

`talon` is not compatible with Python 3

`pyml` is required for `talon` to install properly:

    $ curl -L http://sourceforge.net/projects/pyml/files/latest/download?source=typ_redirect > PyML.tar.gz;
    $ tar -xzf PyML.tar.gz && cd PyML-* && python setup.py build && python setup.py install && rm -rf PyML.tar.gz;

## to do:

- add as part of elasticsearch indexing pipeline?
- check clustering results
- integrate email viz into beerbelly
- how to integrate clustering? as "documents like this"?
- try keyword clustering and build cluster descriptors like in geiger?