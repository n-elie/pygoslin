from pygoslin.domain.LipidExceptions import *

class FattyAcid:

    def __init__(self, name, num_carbon, num_double_bonds, num_hydroxyl, lipid_FA_bond_type, lcb, position):
        self.name = name
        self.position = position
        self.num_carbon = num_carbon
        self.num_double_bonds = num_double_bonds
        self.num_hydroxyl = num_hydroxyl
        self.lipid_FA_bond_type = lipid_FA_bond_type
        self.lcb = lcb
        
        if num_carbon < 2:
            raise ConstraintViolationException("FattyAcid must have at least 2 carbons!")
        
        if position < -1:
            raise ConstraintViolationException("FattyAcid position must be greater or equal to -1 (undefined) or greater or equal to 0 (0 = first position)!")
        
        if num_hydroxyl < 0:
            raise ConstraintViolationException("FattyAcid must have at least 0 hydroxy groups!")
        
    def clone(self, fa):
        self.name = fa.name
        self.position = fa.position
        self.num_carbon = fa.num_carbon
        self.num_double_bonds = fa.num_double_bonds
        self.num_hydroxyl = fa.num_hydroxyl
        self.lipid_FA_bond_type = fa.lipid_FA_bond_type
        self.lcb = fa.lcb
        
    def to_string(self, special_case = False):
        suffix = self.lipid_FA_bond_type.suffix()
        return "%s%i:%i%s%s" % ("O-" if special_case and len(suffix) > 0 else "", self.num_carbon, self.num_double_bonds, ";" + str(self.num_hydroxyl) if self.num_hydroxyl > 0 else "", suffix)