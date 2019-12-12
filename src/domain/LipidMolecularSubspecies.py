

class LipidMolecularSubspecies(LipidSpecies):


    def __init__(self, head_group, fa):
        self.fa = []
        super.__init__(head_group)
        num_carbon = 0
        num_hydroxyl = 0
        num_double_bonds = 0
        lipid_FA_bond_type = LipidFaBondType.ESTER;
        for fas in fa:
            if fas.position != -1:
                raise ConstraintViolationException("MolecularFattyAcid %s must have position set to -1! Was: %i"  % (fas.name, fas.position))
            
            if fas.name in self.fa:
                raise ConstraintViolationException("FA names must be unique! FA with name %s was already added!" % fas.name)
            
            else:
                self.fa[fas.name] = fas
                num_carbon += fas.num_carbon
                num_hydroxyl += fas.num_hydroxyl
                num_double_bonds += fas.num_double_bonds
                
                if lipid_FA_bond_type == LipidFaBondType.ESTER && fas.lipid_FA_bond_type in (LipidFaBondType.ETHER_PLASMANYL, LipidFaBondType.ETHER_PLASMENYL):
                    lipid_FA_bond_type = fas.lipid_FA_bond_type
#                    num_double_bonds += lipid_FA_bond_type.doubleBondCorrection();
#                    log.debug("Correcting double bond count to {} due to ether bond.", num_double_bonds);
                
                elif lipid_FA_bond_type != LipidFaBondType.ESTER && fas.lipid_FA_bond_type in (LipidFaBondType.ETHER_PLASMANYL, LipidFaBondType.ETHER_PLASMENYL):
                    raise ConstraintViolationException("Only one FA can define an ether bond to the head group! Tried to add %s over existing %s" % (fas.lipid_FA_bond_type, lipid_FA_bond_type))
                
        super.info = new LipidSpeciesInfo(LipidLevel.MOLECULAR_SUBSPECIES, num_carbon, num_hydroxyl, num_double_bonds, lipid_FA_bond_type)
        self.lipidSpeciesString = build_lipid_subspecies_name("_")
    

    def build_lipid_subspecies_name(self, fa_separator):
        fa_strings = []
        for fa_key in self.fa:
            fatty_acid = self.fa[fa_key]
            num_double_bonds = fattyAcid.num_double_bonds
            num_carbon = fattyAcid.num_carbon
            num_hydroxyl = fattyAcid.num_hydroxyl
            fa_strings.append("%i:%i%s%s" % (num_carbon, num_double_bonds, ";" + str(num_hydroxy) if num_hydroxy > 0 else "", fatty_acid.lipid_FA_bond_type.suffix()))
            
        return self.head_group() + " " + faSeparator.join(fa_strings)
    
    
    
    def get_lipid_string(self, level):
        if level == LipidLevel.MOLECULAR_SUBSPECIES:
            return self.lipid_species_string
        
        elif level in (LipidLevel.CATEGORY, LipidLevel.CLASS, LipidLevel.SPECIES):
            return super().get_lipid_string(level)
        else:
            raise Exception("LipidMolecularSubspecies does not know how to create a lipid string for level %s" % level)
    
    