#  input file location for conversion from fasta (.fas) to phylip (.txt or .phy)

# file = input("enter file location and name: ")
file = ''

if len(file) == 0:
    file = '/home/chaddaniel18/Desktop/Phylip-data/bioinfomethods1_labs_Lab3,4_sequences_DNA_aligned.fas'
    # file = '/home/chaddaniel18/Desktop/Phylip-data/copy-paste-from-class.fas'

fasta = []

try:
    with open(file) as f:
        for line in f:
            fasta.append(line)
        print('file location and name valid')
except:
    print('invalid file location and name')
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
with open('/home/chaddaniel18/Desktop/Phylip-data/converted-with-py.phy', 'w') as writer:
    writer.write(str(num_samples) + ' ' + str(len(dna) - 1) + '\n')
    writer.write(phylip)

# test = 'ATGCAGAGATTCATGTTTAGCCGCGTCGTGGAACATCAACGTCAGATAAGCCGAGGATTTCTCAGTCTTGTACCATCTCTATCTCCCACTGCTGTTCCTGCTATGTCTCGTTTCTTTCCGAAGATTACTGCTTCTGATTCCACTTCCTCGATTCCCTTTTTTACTCCAGACTTCATCAATCCCAAGAAGACTCTTGAAGAGTCCCTTAACAACTTAGAAGGCCTAACATGTAACCAAGCCGAAAGAGAGATGTATCTCTTTCCACAGATTAATCAACAACGCCTTCTCAACACCACTGGTTCTCGCTTCGGACAGGTTCTTGGAACTTGGCAGTTCAGATGCACAATTCTTCCGGCGAGAGTGAATCGTGTGAGAGAGGTCCACGAGACTTCCAACAACGAAAAGAAACAACAAAAACAAAAAAGTTCCGTCAACGAAAAGAAACCAAAAAAAAAAAAAAAGAGTTCCATCAGCGATATCCCAAGAAGAACAAAGT--TTCAGAAACATCATCGAGGAAGAATTAAT------AAAGGAGTATCTTCTCAGGGGTATATT------TGTAGTAGATATGCTCTTCAAACACTT---GAACCAGCTTGGATCACTTCTAGACAAATAGAAGCAGGACGACGAGCAATGACACGAAATATAGGAC------GTGGTTTAACTGTTCGAGTTCATATATTTGCAGACAAACCAGTTACAGTAAGACCTCCTGAAACGCGTATGGGTCGTGGGAAAGGAGCTCCAGCGTTTTGGGTAGCTGTGGTTAAACCAGGTAAAATCATTTATGAAATGGGTGGTG------TTTCCGAAAAAGTAGCTAGAGAAGCTATTTCTATAGCCGCATCAAAGTTGCCTGCAAAAACCAAATTCATCATTTCTAAATAA------------------------------------------------------------------------------------------------------------------------------------------------------'
# print('test')
# print(len(test))
