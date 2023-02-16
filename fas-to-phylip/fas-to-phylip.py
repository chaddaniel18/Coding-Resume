#  Place input file in same folder as .py file to convert from fasta (.fas) to phylip (.txt or .phy)
#  File type must be sequential, not interleaved
file = input("enter file name: ")

if len(file) == 0:
    file = 'bioinfomethods1_labs_Lab3,4_sequences_DNA_aligned.fas'

fasta = []

try:
    with open(file) as f:
        for line in f:
            fasta.append(line)
        print('file name valid')
except:
    print('invalid file name')
    exit()

phylip = ''
switch = 'on'
num_samples = 0

for line in fasta:
    if line[0] == '>':
        num_samples += 1
        phylip = phylip  # + '\n'
        switch = 'on'
        seq_len = 0
    else:
        switch = 'off'
    if switch == 'on':
        phylip = phylip + line[1:11].strip()
    elif switch == 'off':
        temp_dna = []
        for char in line:
            seq_len += 1
            temp_dna.append(char)
        dna = ''.join(temp_dna)
        phylip = phylip + dna


print(seq_len)
save_file_name = input("save file as: ")
if len(save_file_name) == 0:
    save_file_name = 'converted-with-py.phy'

with open(save_file_name, 'w') as writer:
    writer.write(str(num_samples) + ' ' + str(len(dna) - 1) + '\n')
    writer.write(phylip)

# test = 'ATGCAGAGATTCATGTTTAGCCGCGTCGTGGAACATCAACGTCAGATAAGCCGAGGATTTCTCAGTCTTGTACCATCTCTATCTCCCACTGCTGTTCCTGCTATGTCTCGTTTCTTTCCGAAGATTACTGCTTCTGATTCCACTTCCTCGATTCCCTTTTTTACTCCAGACTTCATCAATCCCAAGAAGACTCTTGAAGAGTCCCTTAACAACTTAGAAGGCCTAACATGTAACCAAGCCGAAAGAGAGATGTATCTCTTTCCACAGATTAATCAACAACGCCTTCTCAACACCACTGGTTCTCGCTTCGGACAGGTTCTTGGAACTTGGCAGTTCAGATGCACAATTCTTCCGGCGAGAGTGAATCGTGTGAGAGAGGTCCACGAGACTTCCAACAACGAAAAGAAACAACAAAAACAAAAAAGTTCCGTCAACGAAAAGAAACCAAAAAAAAAAAAAAAGAGTTCCATCAGCGATATCCCAAGAAGAACAAAGT--TTCAGAAACATCATCGAGGAAGAATTAAT------AAAGGAGTATCTTCTCAGGGGTATATT------TGTAGTAGATATGCTCTTCAAACACTT---GAACCAGCTTGGATCACTTCTAGACAAATAGAAGCAGGACGACGAGCAATGACACGAAATATAGGAC------GTGGTTTAACTGTTCGAGTTCATATATTTGCAGACAAACCAGTTACAGTAAGACCTCCTGAAACGCGTATGGGTCGTGGGAAAGGAGCTCCAGCGTTTTGGGTAGCTGTGGTTAAACCAGGTAAAATCATTTATGAAATGGGTGGTG------TTTCCGAAAAAGTAGCTAGAGAAGCTATTTCTATAGCCGCATCAAAGTTGCCTGCAAAAACCAAATTCATCATTTCTAAATAA------------------------------------------------------------------------------------------------------------------------------------------------------'
# print('test')
# print(len(test))
