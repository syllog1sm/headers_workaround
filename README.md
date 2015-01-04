headers_workaround
==================

Workaround for setuptools Issue #209: packages listed in both setup\_requires and install_requires aren't installed. For PyPy-in-a-virtualenv, this is currently broken due to issue #510 in virtualenv: https://github.com/pypa/virtualenv/issues/510 . I should have a workaround for this soon.

Currently supported headers:

* numpy
* murmurhash

Pull requests for whatever headers you need are welcome.

Let's say you've developed a C extension that depends on the numpy headers at compile time. This is very common for Cython projects, because numpy is often used as a native array type.

numpy exports a function numpy.get_include_dir(). To call this function, numpy must be imported during the setup.py script. The documented way to achieve this is to supply the string "numpy" to the setup_requires keyword argument of the call to setuptools.setup in your setup.py file.

Bug #209 prevents this from working as expected.  Setuptools uses easy_install to fetch a numpy egg, which is left in your package directory --- but doesn't install it. This allows "import numpy" to work in your setup.py script.  But, when it comes time to install the dependencies in install_requires, setuptools notes that "import numpy" succeeds, and doesn't then install numpy! So, at runtime, "import numpy" fails.

Here is an example setup.py script, employing my workaround. The headers installed are for my wrapper of murmurhash.

```python
  setup(
      ext_modules=exts,
      name="preshed",
      packages=["preshed"],
      version="0.33",
      author="Matthew Honnibal",
      author_email="honnibal@gmail.com",
      url="http://github.com/syllog1sm/preshed",
      package_data={"preshed": ["*.pxd", "*.pyx", "*.c"]},
      description="""Cython hash table that trusts the keys are pre-hashed""",
      classifiers=[
                  'Environment :: Console',
                  'Operating System :: OS Independent',
                  'Intended Audience :: Science/Research',
                  'Programming Language :: Cython',
                  'Topic :: Scientific/Engineering'],
      install_requires=["murmurhash", "cymem"],
      setup_requires=["headers_workaround"]
  )

  import headers_workaround
  import sys


  include_dir = path.join(sys.prefix, 'include', 'site')
  if not path.exists(include_dir):
      os.mkdir(include_dir)
  headers_workaround.install_headers(include_dir, 'murmurhash')
```
  
The package required at setup is "murmurhash". But, I also want that package at run-time (because of course). So, I don't write setup_requires=["murmurhash"], because of Bug 209.  Instead, I write setup_requires=["headers_workaround"]

Below the call to setup, I import the headers_workaround package. This only works *below* the call, due to whatever witchcraft setuptools uses to make setup_requires work. I then fetch the location of the relevant Python install, which under a virtualenv will be the virtualenv directory.  I then construct a path to the include dir, and tell headers_workaround to install the murmurhash headers.

# Gotchas

Note that setuptools.setup_requires leaves the .egg directories sitting in your package directory.  This can make your build stateful.  For instance, if you've been trying to require numpy at setup time, you may have a numpy .egg file in your package dir, which is causing "import numpy" to succeed. Delete this directory to make the headers_workaround succeed.
