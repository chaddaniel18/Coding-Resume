# Multiple Longest Common Subsequence Problem
# This code is adapted from GlobalAlignmentProblem and LocalAlignmentProblem_V2
# It adds a third string to the alignment problem i.e. a third dimension
# It is also shifted to funciton with a scoring matrix but this matrix assumes all mismatch/indel == 0
# The multiple result option from the original code has been removed to have practical run times
# Functionality for amino acid alignment added

 # In the Multiple Longest Common Subsequence Problem, the score of a column of the alignment 
    # matrix is equal to 1 if all of the column's symbols are identical, and 0 if even one symbol 
    # disagrees.

# Code Challenge: Solve the Multiple Longest Common Subsequence Problem.
    # Input: Three DNA strings of length at most 10.
    # Output: The length of a longest common subsequence of these three strings, followed by a 
        # multiple alignment of the three strings corresponding to such an alignment.

class MultipleLCS(object):
    def __init__(self):
        print('μ_σ')
        print('main_aas(score_matrix_dict, v, w, u)')
        print('main_atcg(v, w, u)')
        
    def main_aas(self, score_matrix_dict, v, w, u):
         # seting variables
        self.v = v
        self.w = w
        self.u = u
        self.matrix = score_matrix_dict
        # runing subroutines
        self.node_backtrack_3D()
        self.backtracking_3D()
        print('Hazah!!!')
        
    def main_atcg(self, v, w, u):
        # seting variables
        self.v = v
        self.w = w
        self.u = u
        # generate scoring matrix
        self.matrix = {}
        for char in 'ATCG-':
            self.matrix[char] = {}
        for char_1 in 'ATCG-':
            for char_2 in 'ATCG-':
                self.matrix[char_1][char_2] = {}
                for char_3 in 'ATCG-':
                    if char_1 == char_2 == char_3 and char_1 != '-':
                        self.matrix[char_1][char_2][char_3] = 1
                    else:
                        self.matrix[char_1][char_2][char_3] = 0
        # runing subroutines
        self.node_backtrack_3D()
        self.backtracking_3D()
        print('Hazah!!!')
        
    def node_backtrack_3D(self):
        nodes = {}
        nodes[(0, 0, 0)] = 0
        backtrack = {}
        backtrack[(0, 0, 0)] = "*"
        # generate simple 1D nodes
        for i in range(1, len(v) + 1):
            nodes[(i, 0, 0)] = 0
            backtrack[(i, 0, 0)] = "s"                
        for j in range(1, len(w) + 1):
            nodes[(0, j, 0)] = 0
            backtrack[(0, j, 0)] = "e"
        for k in range(1, len(u) + 1):
            nodes[(0, 0, k)] = 0
            backtrack[(0, 0, k)] = "b"
        # cube simple surface generation
        k = 0
        for i in range(1, len(v) + 1):
            for j in range(1, len(w) + 1):
                nodes[(i, j, k)] = 0
                backtrack[(i, j, k)] = "se" # default return to sink once at surface
        j = 0
        for i in range(1, len(v) + 1):
            for k in range(1, len(u) + 1):
                nodes[(i, j, k)] = 0
                backtrack[(i, j, k)] = "sb" # default return to sink once at surface
        i = 0
        for j in range(1, len(w) + 1):
            for k in range(1, len(u) + 1):
                nodes[(i, j, k)] = 0
                backtrack[(i, j, k)] = "eb" # default return to sink once at surface
        # generate interior nodes an record backtrack
        for i in range(1, len(v) + 1):
            for j in range(1, len(w) + 1):
                for k in range(1, len(u) + 1):
                    # one dimensional change
                    #south_sum = nodes[(i - 1, j, k)] + self.matrix[v[i-1]]['-']['-']
                    #east_sum = nodes[(i, j - 1, k)] + self.matrix['-'][w[j-1]]['-']
                    #back_sum = nodes[(i, j, k - 1)] + self.matrix['-']['-'][u[k-1]]
                    # shorthand for simple matrix atcg, score increased by 0 for indel
                    south_sum = nodes[(i - 1, j, k)] + 0
                    east_sum = nodes[(i, j - 1, k)] + 0
                    back_sum = nodes[(i, j, k - 1)] + 0
                    # two dimensional change
                    #south_east_sum = nodes[i - 1, j - 1, k] + self.matrix[v[i-1]][w[j-1]]['-']
                    #south_back_sum = nodes[i - 1, j, k - 1] + self.matrix[v[i-1]]['-'][u[k-1]]
                    #east_back_sum = nodes[i, j - 1, k - 1] + self.matrix['-'][w[j-1]][u[k-1]]
                    # shorthand for simple matrix atcg, score increased by 0 for indel
                    south_east_sum = nodes[i - 1, j - 1, k] + 0
                    south_back_sum = nodes[i - 1, j, k - 1] + 0
                    east_back_sum = nodes[i, j - 1, k - 1] + 0
                    # three dimensional change
                    south_east_back_sum = nodes[i - 1, j - 1, k - 1] + \
                                                self.matrix[v[i-1]][w[j-1]][u[k-1]]
                    nodes[(i, j, k)] = max([south_sum, east_sum, back_sum, south_east_sum, south_back_sum,\
                                        east_back_sum, south_east_back_sum])
                    backtrack[(i, j, k)] = []
                    bias = 'seb,se,sb,eb,s,e,b'
                    if bias == 's,e,b,se,sb,eb,seb':
                        if nodes[(i, j, k)] == south_sum:
                            backtrack[(i, j, k)] = "s"
                        elif nodes[(i, j, k)] == east_sum:
                            backtrack[(i, j, k)] = "e"
                        elif nodes[(i, j, k)] == back_sum:
                            backtrack[(i, j, k)] = "b"
                        elif nodes[(i, j, k)] == south_east_sum:
                            backtrack[(i, j, k)] = "se"
                        elif nodes[(i, j, k)] == south_back_sum:
                            backtrack[(i, j, k)] = "sb"
                        elif nodes[(i, j, k)] == east_back_sum:
                            backtrack[(i, j, k)] = "eb"
                        elif nodes[(i, j, k)] == south_east_back_sum:
                            backtrack[(i, j, k)] = "seb"
                    if bias == 'seb,s,e,b,se,sb,eb':
                        if nodes[(i, j, k)] == south_east_back_sum:
                            backtrack[(i, j, k)] = "seb"
                        elif nodes[(i, j, k)] == south_sum:
                            backtrack[(i, j, k)] = "s"
                        elif nodes[(i, j, k)] == east_sum:
                            backtrack[(i, j, k)] = "e"
                        elif nodes[(i, j, k)] == back_sum:
                            backtrack[(i, j, k)] = "b"
                        elif nodes[(i, j, k)] == south_east_sum:
                            backtrack[(i, j, k)] = "se"
                        elif nodes[(i, j, k)] == south_back_sum:
                            backtrack[(i, j, k)] = "sb"
                        elif nodes[(i, j, k)] == east_back_sum:
                            backtrack[(i, j, k)] = "eb"
                    if bias == 'seb,se,sb,eb,s,e,b':
                        if nodes[(i, j, k)] == south_east_back_sum:
                            backtrack[(i, j, k)] = "seb"
                        elif nodes[(i, j, k)] == south_east_sum:
                            backtrack[(i, j, k)] = "se"
                        elif nodes[(i, j, k)] == south_back_sum:
                            backtrack[(i, j, k)] = "sb"
                        elif nodes[(i, j, k)] == east_back_sum:
                            backtrack[(i, j, k)] = "eb"
                        elif nodes[(i, j, k)] == south_sum:
                            backtrack[(i, j, k)] = "s"
                        elif nodes[(i, j, k)] == east_sum:
                            backtrack[(i, j, k)] = "e"
                        elif nodes[(i, j, k)] == back_sum:
                            backtrack[(i, j, k)] = "b"
        self.score = nodes[(len(v), len(w), len(u))]
        self.nodes = nodes
        self.backtrack = backtrack
        print(self.score)
    
    def backtracking_3D(self):
        node = (len(self.v), len(self.w), len(self.u))
        lcs_vwu = ['', '', '']
        while node != (0, 0, 0):
            if self.backtrack[node] == "s":
                lcs_vwu = [v[node[0] - 1] + lcs_vwu[0], '-' + lcs_vwu[1], '-' + lcs_vwu[2]]
                node = (node[0] - 1, node[1], node[2])
            elif self.backtrack[node] == "e":
                lcs_vwu = ['-' + lcs_vwu[0], w[node[1] - 1] + lcs_vwu[1], '-' + lcs_vwu[2]]
                node = (node[0], node[1] - 1, node[2])
            elif self.backtrack[node] == "b":
                lcs_vwu = ['-' + lcs_vwu[0], '-' + lcs_vwu[1], u[node[2] - 1] + lcs_vwu[2]]
                node = (node[0], node[1], node[2] - 1)
            elif self.backtrack[node] == "se":
                lcs_vwu = [v[node[0] - 1] + lcs_vwu[0], w[node[1] - 1] + lcs_vwu[1], '-' + lcs_vwu[2]]
                node = (node[0] - 1, node[1] - 1, node[2])
            elif self.backtrack[node] == 'sb':
                lcs_vwu = [v[node[0] - 1] + lcs_vwu[0], '-' + lcs_vwu[1], u[node[2] - 1] + lcs_vwu[2]]
                node = (node[0] - 1, node[1], node[2] - 1)
            elif self.backtrack[node] == 'eb':
                lcs_vwu = ['-' + lcs_vwu[0], w[node[1] - 1] + lcs_vwu[1], u[node[2] - 1] + lcs_vwu[2]]
                node = (node[0], node[1] - 1, node[2] - 1)
            elif self.backtrack[node] == 'seb':
                lcs_vwu = [v[node[0] - 1] + lcs_vwu[0], w[node[1] - 1] + lcs_vwu[1], u[node[2] - 1] + \
                                                                                      lcs_vwu[2]]
                node = (node[0] - 1, node[1] - 1, node[2] - 1)
        self.alignments = lcs_vwu
        return self.alignments          
