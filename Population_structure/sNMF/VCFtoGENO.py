
# convert VCF file Second_vcf.recode.vcf into geno format (input for sNMF)


fx = open('Dothi_1491.vcf')
ct = fx.readlines()
fx.close()

n = 0
fout = open('Dothi.geno','w')
for x in ct:
    if x[0] != '#':
        n = n + 1
        line = ''
        genop = x.split('\t')[9:]
        for y in genop:
            if y.split(':')[0] == '.':
                line = line + '9'
            elif y.split(':')[0] == '0':
                line = line + '1'
            else:
                line = line +'0'
        print n, len(line)
        fout.write(line + '\n')
fout.close()