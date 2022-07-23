#!/usr/bin/env python
import argparse
import os
import sys

import libsbml
import sbml2pydstool

from pprint import pprint

parser = argparse.ArgumentParser("Reads SBML files and converts them into objects for PyDSTool")
parser.add_argument('sbml', help="SBML file to be converted to PyDSTool")

args = parser.parse_args()

if not os.path.isfile(args.sbml):
    print(args.sbml, "not found.")
    sys.exit()

# validate SBML
print("Validating", args.sbml)
d = libsbml.readSBML(args.sbml)
if d.getNumErrors() > 0:
    print(d.getErrorLog().toString())
    sys.exit()

d.setConsistencyChecks(libsbml.LIBSBML_CAT_UNITS_CONSISTENCY, False) # skip unit check
if d.checkConsistency() > 0:
    print(d.getErrorLog().toString())
    sys.exit()

# convert SBML to PyDSTool object
c = sbml2pydstool.Converter(args.sbml)

print()
print("Initial Conditions:")
print("-------------------")
pprint(c.icdict, width=8)
print()

print("Parameters:")
print("-------------------")
pprint(c.pars, width=8)
print()

print("ODEs:")
print("-------------------")
pprint(c.varspecs)
print()

print("Functions:")
print("-------------------")
pprint(c.fnspecs)
