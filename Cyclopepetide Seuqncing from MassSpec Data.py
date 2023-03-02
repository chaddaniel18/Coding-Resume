# This version introduces the option for output as first with highest score, all with highest score,
### or cyclicaly unique with highest score

# This program combines code from this subsection of the course and the previos section to solve 
### the problem of finding a peptide or peptides that are the most likely source of mass spec results 
### that have potential false values and/or missing values
############ functional but slow for large inputs unless n is reduced with each iteration

# Abbreviations
    # pep = peptide # e_spec = experimental spectra # aa = amino acid
    # t_spec = theoretical spectra # spec = spectrum

# Psudocode from the course that was used to make the main function
    #LeaderboardCyclopeptideSequencing(Spectrum, N)
    #    Leaderboard ← set containing only the empty peptide
    #    LeaderPeptide ← empty peptide
    #    while Leaderboard is non-empty
    #        Leaderboard ← Expand(Leaderboard)
    #        for each Peptide in Leaderboard
    #            if Mass(Peptide) = ParentMass(Spectrum)
    #                if Score(Peptide, Spectrum) > Score(LeaderPeptide, Spectrum)
    #                    LeaderPeptide ← Peptide
    #            else if Mass(Peptide) > ParentMass(Spectrum)
    #                remove Peptide from Leaderboard
    #        Leaderboard ← Trim(Leaderboard, Spectrum, N)
    #    output LeaderPeptide

class LeaderboardCyclopeptideSequencing_V2(object):
    def __init__(self):
        print('main(spectrum, n, slim_n, output_type)')
        print('ouput_type options: 1st, all, unique')
        # in the aa list and dictionary below L and Q are ommited because they have the same masses
        ### as I and K respectively a choice between the two is not possible given the available info
        ### within the scope of this assignment. This removal provides more efficiency to the program.
        self.aas = ['H', 'P', 'R', 'D', 'E', 'A', 'G', 'V',
                    'Y', 'S', 'C', 'W', 'F', 'N', 'K', 'T', 'I', 'M']
        self.aa_to_mass = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103,
         'I': 113, 'N': 114, 'D': 115, 'K': 128, 'E': 129, 'M': 131,
         'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186}
        
    def main(self, spec, n, slim_n, output_type):
        top_peps = []
        leaderboard = ['']
        top_score = 0
        parent_mass = max(spec)
        rep = 1
        while len(leaderboard) > 0:
            print(f'rep: {rep}')
            rep += 1
            leaderboard = self.expand(leaderboard)
            #if n < len(leaderboard): #### moved to the end of the loop per lecture comment section
            #    leaderboard = self.trim(leaderboard, spec, n)
            for pep in leaderboard.copy():
                pep_mass = self.mass(pep)
                if pep_mass == parent_mass:
                    pep_score = self.peptide_score(pep, spec, 'cyclic')
                    #leaderboard.remove(pep) # hashed out per lecture comment section
                    if pep_score > top_score:
                        top_peps = [pep]
                        top_score = pep_score
                    elif pep_score == top_score and pep not in top_peps:
                        top_peps.append(pep)
                elif pep_mass > parent_mass:
                    leaderboard.remove(pep)
            if n < len(leaderboard):
                leaderboard = self.trim(leaderboard, spec, n)
            if slim_n == 'y':
                n = round(n/2) + 1
        if output_type == '1st':
            self.top_pep = top_peps[0]
            self.top_pep_mass_type = self.peptide_to_mass_peptide(self.top_pep)
            return self.top_pep
        elif output_type == 'all':
            self.top_peps = top_peps
            self.top_peps_mass_type = []
            for pep in top_peps:
                self.top_peps_mass_type.append(self.peptide_to_mass_peptide(pep))
            return self.top_peps
        elif output_type == 'unique':
            # add to list if t_spec of pep not in top_specs
            top_specs = []
            self.uni_peps = []
            self.uni_peps_mass_type = []
            for pep in top_peps:
                t_spec = self.pep_spec(pep, 'cyclic')
                if t_spec not in top_specs:
                    self.uni_peps.append(pep)
                    self.uni_peps_mass_type.append(self.peptide_to_mass_peptide(pep))
                    top_specs.append(t_spec)
            return self.uni_peps
        
        #return self.top_peps_mass_type
        #leader_pep_mass_type = self.peptide_to_mass_peptide(leader_pep)
        #self.leader_pep = leader_pep
        #self.leader_pep_mass_type = leader_pep_mass_type
        #return leader_pep_mass_type
                            
            
    # conversion of a character based peptide to a mass-mass-mass peptide format
    def peptide_to_mass_peptide(self, peptide):
        mass_string = []
        for aa in peptide:
            mass_string.append(str(self.aa_to_mass[aa]))
        mass_string = '-'.join(mass_string)
        return mass_string
        
    # converts a peptide made of aa characters into the sum of the masses of each aa
    def mass(self, peptide):
        mass = 0
        for aa in peptide:
            mass += self.aa_to_mass[aa]
        return mass
    
    # input, candidate peptides (or empty list)
    # output, candidate peptides extended by one aa
    def expand(self, peptides):
        new_peptides = []
        for option in peptides:
            for aa in self.aas:
                new_peptides.append(option + aa)
        return new_peptides
    
    #  Given a list of peptides Leaderboard, a spectrum Spectrum, and an integer N, 
        # define Trim(Leaderboard, Spectrum, N) as the collection of the top N highest-scoring 
        # linear peptides in Leaderboard (including ties) with respect to Spectrum.
    def trim(self, leaderboard, spec, n):
        linear_scores = []
        for peptide in leaderboard:
            linear_scores.append(self.peptide_score(peptide, spec, 'linear'))
        leaderboard = [peptide for score, peptide 
                       in sorted(zip(linear_scores, leaderboard), reverse=True)]
        linear_scores.sort(reverse=True)
        i = int()
        for i in range(n - 1, len(leaderboard)):
            if linear_scores[i] < linear_scores[n - 1]:
                #end = i
                break
        leaderboard = leaderboard[:i]
        self.leaderboard = leaderboard
        return leaderboard
    
    #Peptide Scoring Problem: Compute the score of a cyclic or linear peptide against a spectrum.
    # the score is a count of the number of overlapping values between experimental and 
    ### theoretical spectrums.
    def peptide_score(self, pep, e_spec, pep_type):
        if pep_type not in ['cyclic', 'linear']:
            print('incorect input: cyclic or linear required')
        else:
            t_spec = self.pep_spec(pep, pep_type)
            score = 0
            t_count = self.spec_to_count_dict(t_spec)
            e_count = self.spec_to_count_dict(e_spec)
            for key in t_count:
                if key in e_count.keys():
                    if t_count[key] != 0 and e_count[key] != 0:
                        score += min([t_count[key], e_count[key]])
            return score
    
    # conversion of a list of numbers to a dictionary with these numbers as keys and the number of 
        # occurances as dict values
    def spec_to_count_dict(self, spec):
        count_dict = {}
        keys = set(spec)
        for key in keys:
            count_dict[key] = spec.count(key)
        return count_dict
    
    # creation of a list of the masses of all of the substrings of a peptide, linear or cyclic
    def pep_spec(self, peptide, pep_type):
        aa_to_mass = self.aa_to_mass
        prefix_mass = {}
        prefix_mass[0] = 0
        for i in range(len(peptide)):
            prefix_mass[i + 1] = prefix_mass[i] + aa_to_mass[peptide[i]]
        pep_spec = [0]
        peptide_mass = prefix_mass[len(peptide)]
        if pep_type == 'linear':
            for i in range(len(prefix_mass)):
                for j in range((i + 1), len(prefix_mass)):
                    pep_spec.append(prefix_mass[j] - prefix_mass[i])
        elif pep_type == 'cyclic':
            for i in range(len(peptide)):
                for j in range((i + 1), len(peptide) + 1):
                    pep_spec.append(prefix_mass[j] - prefix_mass[i])
                    if i > 0 and j < len(peptide):
                        pep_spec.append(peptide_mass - (prefix_mass[j] - prefix_mass[i]))
        pep_spec.sort()
        return pep_spec
