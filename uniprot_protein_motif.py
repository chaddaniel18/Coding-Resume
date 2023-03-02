# Given: At most 15 UniProt Protein Database access IDs.

# Return: For each protein possessing the N-glycosylation motif, output its given access ID followed 
    # by a list of locations in the protein string where the motif can be found.

def uniprot_protein_motif(uni_ids):
    from urllib.request import urlopen
    from re import search
    samples = {}
    results = []
    for uni_id in uni_ids:
        indexes = []
        fasta = []
        url = f'http://www.uniprot.org/uniprot/{uni_id[:6]}.fasta'
        fhand = urlopen(url)
        for line in fhand:
            fasta.append(line.decode().strip())
        seq = ''.join(fasta[1:])
        samples[uni_id] = [seq]
        for i in range(len(seq)):
            if seq[i] == 'N':
                if search('N[^P][ST][^P]', seq[i:i+4]) != None:
                    indexes.append(i+1)
        if len(indexes) > 0:
            results.append(uni_id)
            results.append(' '.join([str(x) for x in indexes]))
    return results
