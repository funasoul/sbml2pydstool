# sbml2pydstool
Convert SBML to a python code for [PyDSTool](https://github.com/robclewley/pydstool).

Still under development.

## Requirements
- Python (<= 3.9. [PyDSTool is not compatible with Python 3.10](https://getdocs.org/Python/docs/3.10/whatsnew/3.10#Removed))
- libSBML
- numpy
- scipy
- matplotlib
- PyDSTool
- ipython

- If you want to use AUTO and Fortran-based integrator (Radau), please install `gfortran`.
  ```sh
  ## (ex.) Install gcc12 from MacPorts
  % sudo port install gcc12
  ## and select the installed gcc port as your default gcc
  % sudo port select gcc mp-gcc12
  ## or just create a link to ${prefix}/bin/gfortran-mp-12 as 'gfortran'.
  % sudo ln -s /opt/local/bin/gfortran-mp-12 /opt/local/bin/gfortran
  ```

## How to use
Clone the repository and install dependent python modules.
```sh
% git clone https://github.com/funasoul/sbml2pydstool.git
% cd sbml2pydstool
% python3.9 -m venv venv
% source ./venv/bin/activate
(venv)% pip install --upgrade pip
(venv)% pip install python-libsbml numpy scipy matplotlib
(venv)% pip install pydstool
(venv)% pip install gnureadline ipython
```

Run the test script, which will import SBML (`ca.xml`) and run a simple bifurcation analysis with PyDSTool.
```sh
(venv)% python test.py
```

## References
- [PyDSTool Tutorial](https://pydstool.github.io/PyDSTool/Tutorial.html)
- [PyDSTool PyCont](https://pydstool.github.io/PyDSTool/PyCont.html)
- [auto-07p](https://github.com/auto-07p/auto-07p)
- [Advances in numerical bifurcation software: MatCont](https://biblio.ugent.be/publication/8615817)
- [Numerical Continuation of Fold Bifurcations of Limit Cycles in MATCONT](https://dl.acm.org/doi/10.5555/1764172.1764253)
- [The classification of the dynamic behavior of continuous stirred tank reactors—influence of reactor residence time](https://www.sciencedirect.com/science/article/pii/0009250976850580)
- [sys-bio/rrplugins auto2000](https://github.com/sys-bio/rrplugins/tree/master/plugins/released/auto2000)
- [Bifurcation using AUTO2000 and the Auto2000 Tellurium Plugin](https://sys-bio.github.io/rrplugins/docs/plugins/auto2000/index.html)
- [libRoadRunner Bifurcation Analysis](https://sys-bio.github.io/roadrunner/docs-build/bifurcation.html)
- [Bifurcation diagram How-To](https://groups.google.com/g/copasi-user-forum/c/T-he9VwGaPw)
