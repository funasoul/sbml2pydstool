#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sun, 10 Sep 2017 01:23:44 +0900
# 
# (ex.) ./sbml2pydstool.py sbml.xml
#
import argparse
from libsbml import *

__version__ = "0.0.1"

def generatePars(model):
    pars = {}
    # global parameters
    for p in model.getListOfParameters():
        pars[p.getId()] = p.getValue()

    # local parameters
    for r in m.getListOfReactions():
        k = r.getKineticLaw()
        for p in r.getKineticLaw().getListOfParameters():
            assert p.getId() not in pars, "Please rename your parameter id so that there is no conflict between local and global parameters." # we assume there is no conflict on parameter id
            pars[p.getId()] = p.getValue()

    return pars

def generateIcdict(model):
    icdict = {}
    for s in model.getListOfSpecies():
        if s.isSetInitialConcentration:
            icdict[s.getId()] = s.getInitialConcentration()
        elif s.isSetIntialAmount():
            icdict[s.getId()] = s.getInitialAmount()

    return icdict

def isSpeciesReactantOf(species, reaction):
    for sr in reaction.getListOfReactants():
        if sr.getSpecies() == species.getId():
            return True

    return False

def isSpeciesProductOf(species, reaction):
    for sr in reaction.getListOfProducts():
        if sr.getSpecies() == species.getId():
            return True

    return False

def addASTasReactant(ast, r):
    if ast is None: # if there is no parent, return -1 * v1.
        root = ASTNode(AST_TIMES)
        l = ASTNode()
        l.setValue(-1.0)
        root.addChild(l)
        root.addChild(r.getKineticLaw().getMath().deepCopy())
    else:
        root = ASTNode(AST_MINUS)
        root.addChild(ast)
        root.addChild(r.getKineticLaw().getMath().deepCopy())

    return root

def addASTasProduct(ast, r):
    if ast is None: # if there is no parent, return v1.
        root = r.getKineticLaw().getMath().deepCopy()
    else:
        root = ASTNode(AST_PLUS)
        root.addChild(ast)
        root.addChild(r.getKineticLaw().getMath().deepCopy())

    return root

def generateVarspecs(model):
    # Generate Rate equation for all variable Species (ex. dx/dt = v1 - v2 + v3).
    varspecs = {}
    for s in model.getListOfSpecies():
        #if s.isSetBoundaryCondition() or s.isSetConstant:
        #    continue
        root = None
        for r in model.getListOfReactions():
            if isSpeciesReactantOf(s, r):
                root = addASTasReactant(root, r)
            if isSpeciesProductOf(s, r):
                root = addASTasProduct(root, r)

        if root is not None:
            varspecs[s.getId()] = formulaToString(root)


    return varspecs

#def main():
parser = argparse.ArgumentParser(description="Convert SBML to a python code for bifurcation analysis using pyDSTool")
parser.add_argument('-v', '--version', action='version',
        version=('sbml2pydstool.py v%s' % __version__))
parser.add_argument("sbml_file", metavar='sbml_file', help="SBML file")
args = parser.parse_args()

d = readSBMLFromFile(args.sbml_file)
m = d.getModel()
# generate pars from global/local parameters
pars = generatePars(m)
# generate icdict from species
icdict = generateIcdict(m)
# generate varspecs (rate equations) from model
varspecs = generateVarspecs(m)

#if __name__ == "__main__":
#    main()
