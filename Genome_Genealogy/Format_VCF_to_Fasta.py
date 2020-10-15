
import numpy as np

fx = open('Dothi_1348.vcf')
ct = fx.readlines()
fx.close()


lsn = []
vcf= []
for x in ct:
    if x.split('\t')[0] == '#CHROM':
        head = x.split('\t')[9:]
        for y in head:
            name = y.replace('/aegir/arnaud/Dothis/bradshaw_sequences/','').replace('/aegir/arnaud/Dothis/Round4/','').replace('_sorted.bam','')
            lsn.append(name)
    elif x[0] != '#':
        locus = []
        allele1, allele2 = x.split('\t')[3],  x.split('\t')[4]

        if len(allele1) == 1 and len(allele2) == 1:

            print allele1, allele2
            line = x.split('\t')[9:]
            for y in line:

                if y.split(':')[0] == '0':
                    locus.append(allele1)
                elif y.split(':')[0] == '1':
                    locus.append(allele2)
                else:
                    locus.append('N')
            vcf.append(locus)

vcf = np.array(vcf)
print '*', vcf
nvcf = vcf.transpose()
print '**', nvcf

fout = open('Dothi_1348.fas','w')
for y,t in zip(nvcf,lsn):
    loc = ''
    for z in y:
        loc = loc + z
    fout.write('>' + t + '\n' + loc + '\n')
fout.close()
