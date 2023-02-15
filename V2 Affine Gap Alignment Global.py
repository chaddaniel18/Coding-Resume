# Code Challenge: Solve the Global Alignment Problem.
# Find the highest scoring alignment of two strings
# Input for nucleaotide alignment: Match reward, mismatch penalty, gap open penalty, gap extend penalty, and two nucleotide strings.
# Input for amino acid alignment: Scoring matrix, gap open penalty, gap extend penalty, and two nucleotide strings.
# Output: The maximum alignment score of these strings followed by an alignment achieving this maximum score.
# Output: Results stored in object.score and object.alignments

# Scoring matrix must be a dictionary of dictionaries
# example "{'A': {'A': 4,  'C': 0,  'D': -2}, 'C': {'A': 0,  'C': 9,  'D': -3}}"

# this version expands the original in a subtle way to fuction with traditional and matrix based problems
class AffineGapAlignmentGlobalV2(object):
    def __init__(self):
        print('μ_σ_ε')
        print('main_aas(score_matrix, gap_open_penalty, gap_extend_penalty, v, w)')
        print('main_atcg(match_score, mismatch_penalty, gap_open_penalty, gap_extend_penalty, v, w)')
        
    def main_aas(self, score_matrix, gap_open_penalty, gap_extend_penalty, v, w):
        self.matrix = score_matrix
        self.open = gap_open_penalty
        self.extend = gap_extend_penalty
        self.v = v
        self.w = w
        # running subroutines
        self.node_backtrack_gen_affine()
        self.backtracking_affine()
        print('Hazah!!!')
        print(self.score)
        print(self.alignments)
        
    def main_atcg(self, match_score, mismatch_penalty, gap_open_penalty, gap_extend_penalty, v, w):
        self.match = match_score
        self.mis = mismatch_penalty
        self.open = gap_open_penalty
        self.extend = gap_extend_penalty
        self.v = v
        self.w = w
        # generate scoreing matrix
        self.matrix = {}
        for char in 'ATCG':
            self.matrix[char] = {}
        for char_1 in 'ATCG':
            for char_2 in 'ATCG':
                if char_1 == char_2:
                    self.matrix[char_1][char_2] = self.match
                else:
                    self.matrix[char_1][char_2] = -self.mis
        # running subroutines
        self.node_backtrack_gen_affine()
        self.backtracking_affine()
        print('Hazah!!!')
        print(self.score)
        print(self.alignments)
        
    def node_backtrack_gen_affine(self):
        cancel_node_val = max([len(v), len(w)]) * self.open + 1 # false source prevention value
        # create backtrack dicts
        bt_middle = {(0, 0): '*'}
        bt_upper = {(0, 0): '*'}
        bt_lower = {(0, 0): '*'}
        # initialize seed nodes
        middle = {(0, 0): 0}
        # false start nodes itteration with value set to max([len(v), len(w)]) * gap_open_penalty + 1
        upper = {(0, 0): -cancel_node_val}
        lower = {(0, 0): -cancel_node_val}
        for i in range(1,len(v) + 1):
            upper[(i, 0)] = -cancel_node_val
            bt_upper[(i, 0)] = '*'
        
        for j in range(1,len(w) + 1):
            lower[(0, j)] = -cancel_node_val
            bt_lower[(0, j)] = '*'

        # generate simple exterior nodes
        for j in range(1,len(w) + 1):
            upper[(0, j)] = max([upper[(0, j-1)] - self.extend, middle[(0, j-1)] - self.open])
            middle[(0, j)] = upper[(0, j)]
            if upper[(0, j)] == upper[(0, j-1)] - self.extend:
                bt_upper[(0, j)] = "→"
            else:
                bt_upper[(0, j)] = "out →"
            bt_middle[(0, j)] = 'in up'

        for i in range(1,len(v) + 1):
            lower[(i, 0)] = max([lower[(i-1, 0)] - self.extend, middle[(i-1, 0)] - self.open])
            middle[(i, 0)] = lower[(i, 0)]
            if lower[(i, 0)] == lower[(i-1, 0)] - self.extend:
                bt_lower[(i, 0)] = "↓"
            else:
                bt_lower[(i, 0)] = "out ↓"
            bt_middle[(i, 0)] = 'in low'
                                 
        # iteration of interior nodes
        for i in range(1, len(v) + 1):
            for j in range(1, len(w) + 1):
                # upper level node value and backtrack
                right_sum = upper[(i, j-1)] - self.extend
                middle_sum = middle[(i, j-1)] - self.open
                upper[(i, j)] = max([right_sum, middle_sum])
                if upper[(i, j)] == right_sum:
                    bt_upper[(i, j)] = "→"
                elif upper[(i, j)] == middle_sum:
                    bt_upper[(i, j)] = "out →"
                # lower level node value and backtrack
                down_sum = lower[(i-1, j)] - self.extend
                middle_sum = middle[(i-1, j)] - self.open
                lower[(i, j)] = max([down_sum, middle_sum])
                if lower[(i, j)] == down_sum:
                    bt_lower[(i, j)] = "↓"
                elif lower[(i, j)] == middle_sum:
                    bt_lower[(i, j)] = "out ↓"
                # middle level node value and backtrack
                diag_sum = middle[(i-1, j-1)] + self.matrix[v[i-1]][w[j-1]]
                middle[(i, j)] = max([upper[(i, j)], lower[(i, j)], diag_sum])
                if middle[(i, j)] == lower[(i, j)]:
                    bt_middle[(i, j)] = 'in low'
                elif middle[(i, j)] == upper[(i, j)]:
                    bt_middle[(i, j)] = 'in up'
                elif middle[(i, j)] == diag_sum:
                    bt_middle[(i, j)] = "↘"
        self.bt_middle = bt_middle
        self.bt_upper = bt_upper
        self.bt_lower = bt_lower
        self.upper = upper
        self.lower = lower
        self.middle = middle
        
######## rework for 3D backtrack ##############
    def backtracking_affine(self):
        node = (len(self.v), len(self.w))
        backtrack = self.bt_middle
        level = 'middle'
        lcs_vw = ['', '']
        self.score = self.middle[node]
        while node != (0, 0):
            if level == 'middle':
                if backtrack[node] == "↘":
                    lcs_vw = [v[node[0] - 1] + lcs_vw[0], w[node[1] - 1] + lcs_vw[1]]
                    node = (node[0] - 1, node[1] - 1)
                elif backtrack[node] == 'in up':
                    backtrack = self.bt_upper
                    level = 'upper'
                elif backtrack[node] == 'in low':
                    backtrack = self.bt_lower
                    level = 'lower'
            if level == 'upper':
                if backtrack[node] == "→":
                    lcs_vw = ['-' + lcs_vw[0], w[node[1] - 1] + lcs_vw[1]]
                    node = (node[0], node[1] - 1)
                elif backtrack[node] == "out →":
                    lcs_vw = ['-' + lcs_vw[0], w[node[1] - 1] + lcs_vw[1]]
                    node = (node[0], node[1] - 1)
                    backtrack = self.bt_middle
                    level = 'middle'
            if level == 'lower':
                if backtrack[node] == "↓":
                    lcs_vw = [v[node[0] - 1] + lcs_vw[0], '-' + lcs_vw[1]]
                    node = (node[0] - 1, node[1])
                elif backtrack[node] == "out ↓":
                    lcs_vw = [v[node[0] - 1] + lcs_vw[0], '-' + lcs_vw[1]]
                    node = (node[0] - 1, node[1])
                    backtrack = self.bt_middle
                    level = 'middle'
        self.alignments = lcs_vw
        return self.alignments    
