SpecprParser.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[wheel](https://gitlab.com/KOLANICH/SpecprParser/-/jobs/artifacts/master/raw/wheels/SpecprParser-0.CI-py3-none-any.whl?job=build)
[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH/SpecprParser.py/workflows/CI/master/SpecprParser-0.CI-py3-none-any.whl)
[![PyPi Status](https://img.shields.io/pypi/v/SpecprParser.svg)](https://pypi.python.org/pypi/SpecprParser.py)
![GitLab Build Status](https://gitlab.com/KOLANICH/SpecprParser.py/badges/master/pipeline.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/SpecprParser.py.svg)](https://coveralls.io/r/KOLANICH/SpecprParser.py)
![GitLab Coverage](https://gitlab.com/KOLANICH/SpecprParser.py/badges/master/coverage.svg)
[![GitHub Actions](https://github.com/KOLANICH/SpecprParser.py/workflows/CI/badge.svg)](https://github.com/KOLANICH/SpecprParser.py/actions/)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/SpecprParser.py.svg)](https://libraries.io/github/KOLANICH/SpecprParser.py)

This is a parser for [SPECtrum Processing Routines Data Format 3/4/88](https://speclab.cr.usgs.gov/specpr-format.html) for python. It relies on KaitaiStruct. Export and editing is not supported for now, though it may be supported in future, though there are better file formats for this. Don't use it on large files: for now parsing is not lazy.

Tutorial
--------
```python
import SpecprParser
p = SpecprParser.SpecprParser("./test")
p.records # the records from file
```

Requirements
------------
* [`Python 3`](https://www.python.org/downloads/). [`Python 2` is officially dead](https://devguide.python.org/devcycle/#end-of-life-branches), stop raping its corpse. Use `2to3` with manual postprocessing to migrate incompatible code to `3`.

* [`kaitaistruct`](https://github.com/kaitai-io/kaitai_struct_python_runtime)
  [![PyPi Status](https://img.shields.io/pypi/v/kaitaistruct.svg)](https://pypi.python.org/pypi/kaitaistruct)
  ![License](https://img.shields.io/github/license/kaitai-io/kaitai_struct_python_runtime.svg)
