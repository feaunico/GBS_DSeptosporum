import matplotlib
matplotlib.use('Agg')

import mpl_toolkits
mpl_toolkits.__path__.append('C:/Python27/Lib/site-packages/mpl_toolkits/')
import matplotlib.pyplot as plt
import numpy as np
import os

entropy = {"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"7":[],"8":[],"9":[],"10":[]}
for  i in range(0,100):
    print 'run', i

    for j in range(1,11):
        os.system('./bin/sNMF -x Dothi.geno -K ' + str(j) +' -m 1 -c 0.05 > Dothi.' + str(j) +'.log')
        fx = open("Dothi." + str(j) + ".log")
        ct = fx.readlines()
        fx.close()
        val = float(ct[-4].split('\t')[1].replace('\n','').replace(' ',''))
        entropy[str(j)].append(val)
        os.system('rm Dothi_I.geno')
        os.system('rm Dothi.' + str(j) + '.log')
        os.system('rm Dothi.' + str(j) + '.G')

        fn = open('Dothi.' + str(j) + '.popfile','a')
        fx = open('Dothi.' + str(j) + '.Q')
        qf = fx.readlines()
        fx.close()
        a = 1
        for l in qf:
            fn.write(str(a)+': '+ l.replace('\n','') + ' 1\n')
            a = a + 1
        fn.write('\n')
        fn.close()


        os.system('rm Dothi.' + str(j) + '.Q')

values = []
for x in entropy:
    values.append((float(x), np.mean(entropy[x]),np.std(entropy[x])))

	
values.sort(key=lambda x: x[0])
print values


fig = plt.figure(figsize=(9, 9))

ax0 = plt.subplot2grid((1, 1), (0, 0))
ax0.errorbar([x[0] for x in values], [x[1] for x in values], yerr=[x[2] for x in values], fmt='-o')
ax0.set_ylabel('Cross-entropy')
ax0.set_xlabel('K, # of ancestral populations')
plt.savefig('Cross_entropy.pdf',dpi=600,  format='pdf')