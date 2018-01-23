#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Tue, 23 Jan 2018 19:36:48 +0900
#
# try import libsbml
try:
    from libsbml import ASTNode
    from libsbml import AST_PLUS
    from libsbml import AST_MINUS
    from libsbml import AST_TIMES
    from libsbml import formulaToString
    from libsbml import readSBMLFromFile
except ImportError:
    from libsbml import ASTNode
    from libsbml import AST_PLUS
    from libsbml import AST_MINUS
    from libsbml import AST_TIMES
    from libsbml import formulaToString
    from libsbml import readSBMLFromFile

class Converter():

    def __init__(self, filepath="", sbmldocument=None):
        self.filepath = filepath
        self.clear_objects()
        # try SBMLDocument at first, and then SBML file
        if sbmldocument is not None:
            self.sbmldocument = sbmldocument
        elif filepath is not "":
            self.sbmldocument = readSBMLFromFile(filepath)

        self.update_sbmldocument(self.sbmldocument)

    def clear_objects(self):
        self.pars = {}
        self.icdict = {}
        self.varspecs = {}

    def update_sbmlfile(self, filepath=""):
        if filepath is not "":
            self.filepath = filepath
            self.sbmldocument = readSBMLFromFile(filepath)
            self.update_sbmldocument(self.sbmldocument)

    def update_sbmldocument(self, sbmldocument):
        if sbmldocument is not None:
            self.sbmlmodel = sbmldocument.getModel()
            self.filepath = ""
            self.clear_objects()
            self.generate_pars(self.sbmlmodel)
            self.generate_icdict(self.sbmlmodel)
            self.generate_varspecs(self.sbmlmodel)

    def generate_pars(self, model):
        # global parameters
        for p in model.getListOfParameters():
            self.pars[p.getId()] = p.getValue()

        # local parameters
        for r in model.getListOfReactions():
            k = r.getKineticLaw()
            for p in r.getKineticLaw().getListOfParameters():
                # we assume there is no conflict on parameter id
                assert p.getId() not in self.pars, "Please rename your parameter id so that there is no conflict between local and global parameters."
                self.pars[p.getId()] = p.getValue()

    def generate_icdict(self, model):
        for s in model.getListOfSpecies():
            if s.isSetInitialConcentration():
                self.icdict[s.getId()] = s.getInitialConcentration()
            elif s.isSetInitialAmount():
                self.icdict[s.getId()] = s.getInitialAmount()

    def is_species_reactant_of(self, species, reaction):
        for sr in reaction.getListOfReactants():
            if sr.getSpecies() == species.getId():
                return True

        return False

    def is_species_product_of(self, species, reaction):
        for sr in reaction.getListOfProducts():
            if sr.getSpecies() == species.getId():
                return True

        return False

    def add_ast_as_reactant(self, ast, r):
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

    def add_ast_as_product(self, ast, r):
        if ast is None: # if there is no parent, return v1.
            root = r.getKineticLaw().getMath().deepCopy()
        else:
            root = ASTNode(AST_PLUS)
            root.addChild(ast)
            root.addChild(r.getKineticLaw().getMath().deepCopy())

        return root

    def generate_varspecs(self, model):
        # Generate Rate equation for all variable Species (ex. dx/dt = v1 - v2 + v3).
        for s in model.getListOfSpecies():
            #if s.isSetBoundaryCondition() or s.isSetConstant:
            #    continue
            root = None
            for r in model.getListOfReactions():
                if self.is_species_reactant_of(s, r):
                    root = self.add_ast_as_reactant(root, r)
                if self.is_species_product_of(s, r):
                    root = self.add_ast_as_product(root, r)
    
            if root is not None:
                self.varspecs[s.getId()] = formulaToString(root)

