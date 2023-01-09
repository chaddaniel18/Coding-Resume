def pseudo_replicate(pr_bin):
    seqA = 'AGGCTCCAAA'
    seqB = 'AGGTTCGAAA'
    seqC = 'AGCCCCGAAA'
    seqD = 'ATTTCCGAAC'

    seqs = [seqA, seqB, seqC, seqD]

    prs = []
    for seq in seqs:
        new_seq = ''
        for i in range(len(seq)):
            new_seq += seq[i] * int(pr_bin[i])
        prs.append(new_seq)
    return prs

pr_bin = '010'
while True:
    pr_bin = input('pr_bin: ')
    if len(pr_bin) == 0:
        break
    if len(pr_bin) != 10:
        print('pr_bin is too short, try again')
        continue
    seqs = pseudo_replicate(pr_bin)
    print(pr_bin)
    print(*seqs, sep='\n')
