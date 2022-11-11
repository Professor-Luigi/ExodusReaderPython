# ExodusReaderPython
Read exodus files into a more usable form using python. This package is meant to be used within a python script as it stands. There will be development into an executable file as well for use outside of python.

This package can read netCDF type files (the filetype that exodus files are based on), but mainly focuses on exodus files. Specifically those output by the ZAPDOS software.

For more information on exodus files, click [here](https://mooseframework.inl.gov/source/outputs/Exodus.html).
For more information on ZAPDOS, click [here](https://github.com/shannon-lab/zapdos).
For documentation on the netCDF4 library for python, click [here](https://unidata.github.io/netcdf4-python).

## Installation
Right now, the package can be installed in the usual way. Download the zip or open a terminal and clone into the desired directory:


`git clone https://github.com/Professor-Luigi/ExodusReaderPython.git`

Most likely you will also need to install the netCDF4 library. This is how the exodus files are made readable to python.

`python -m pip install netCDF4`

Or some variant of that depending on your setup.

In the interest of being thorough, numpy must also be installed (matplotlib is optional but the plotting in the examples won't work.

## Use
Next, (for now) copy the ExodusReader.py and AuxFunctions.py files into the directory where you're reading. All you need to import into your script is ExodusReader.py. AuxFunctions.py is only meant to be used by the ExodusReader.py file.

`import ExodusReader as er`
or
`import .ExodusReader as er`

From there the example files will guide you through the basics of how to use this package.
