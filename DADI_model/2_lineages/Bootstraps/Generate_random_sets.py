import random
import numpy, random, os
from numpy import array
import dadi
from dadi import Numerics, PhiManip, Integration
from dadi.Spectrum_mod import Spectrum
import matplotlib
import pylab
import numpy


fx = open('sfs.xls')
cont = fx.readlines()
fx.close()

head = cont[0]
body = cont[1:]
print len(body)
sca = []
for x in body:
    if x.split('\t')[8].split(':')[0] not in sca:
        sca.append(x.split('\t')[8].split(':')[0])


for j in range(1,101):
    print j
    i = 0
    fout = open('boot.xls','w')
    fout.write(head)
    while i < len(body):
        nb = random.choice(sca)
        deb = random.randrange(0,4000000)
        fin = random.randrange(deb,deb+1000000)
        for x in body:
            if x.split('\t')[8].split(':')[0] == nb:
                if int(x.split('\t')[9].replace('\n','')) >= deb and int(x.split('\t')[9].replace('\n','')) <= fin:
                    if i < len(body):
                        fout.write(x)
                        i = i + 1
    fout.close()
    dd = dadi.Misc.make_data_dict('boot.xls')
    data = dadi.Spectrum.from_data_dict(dd, ['SM', 'OT'], [50, 50], polarized=True)
    data.to_file('boot_.' + str(j) + '.fs')

