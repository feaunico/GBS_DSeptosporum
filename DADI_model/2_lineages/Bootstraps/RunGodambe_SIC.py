import Godambe
import sys
print(sys.version)
import glob
import pylab

#site.addsitedir('/scratch/NICO/dadi-1.6.3_modif')  # Seems to be the important line!
import dadi
from dadi import Numerics, PhiManip, Integration, Inference
from dadi.Spectrum_mod import Spectrum
import numpy as np


def SI(params, (n1, n2), pts):
    nu1, nu2, Ts = params
    xx = dadi.Numerics.default_grid(pts)
    phi = dadi.PhiManip.phi_1D(xx)
    phi = dadi.PhiManip.phi_1D_to_2D(xx, phi)
    phi = dadi.Integration.two_pops(phi, xx, Ts, nu1, nu2, m12=0, m21=01)
    fs = dadi.Spectrum.from_phi(phi, (n1, n2), (xx, xx))
    #fsO = dadi.Numerics.reverse_array(fsM)
    ### Sum the two spectra in proportion O
    #fs = O*fsM+(1-O)*fsO
    return fs


func_ex = SI

dd = dadi.Misc.make_data_dict('sfs.xls')

data = dadi.Spectrum.from_data_dict(dd, ['SM', 'OT'], [50, 50], polarized=True)

ns = data.sample_sizes
grid_pts = np.array([ns[0] + 5])
p0 = np.array([ 0.20730225, 0.13038928, 0.16262654 ])
all_boot = glob.glob('boot_.*.fs')
for x in glob.glob('boot_.*.fs'):
    all_boot.append(dadi.Spectrum.from_file(x))

#print all_boot
uncert = Godambe.GIM_uncert(SI ,grid_pts,  [dadi.Spectrum.from_file("boot_.1.fs"),
dadi.Spectrum.from_file("boot_.2.fs"),
dadi.Spectrum.from_file("boot_.3.fs"),
dadi.Spectrum.from_file("boot_.4.fs"),
dadi.Spectrum.from_file("boot_.5.fs"),
dadi.Spectrum.from_file("boot_.6.fs"),
dadi.Spectrum.from_file("boot_.7.fs"),
dadi.Spectrum.from_file("boot_.8.fs"),
dadi.Spectrum.from_file("boot_.9.fs"),
dadi.Spectrum.from_file("boot_.10.fs"),
dadi.Spectrum.from_file("boot_.11.fs"),
dadi.Spectrum.from_file("boot_.12.fs"),
dadi.Spectrum.from_file("boot_.13.fs"),
dadi.Spectrum.from_file("boot_.14.fs"),
dadi.Spectrum.from_file("boot_.15.fs"),
dadi.Spectrum.from_file("boot_.16.fs"),
dadi.Spectrum.from_file("boot_.17.fs"),
dadi.Spectrum.from_file("boot_.18.fs"),
dadi.Spectrum.from_file("boot_.19.fs"),
dadi.Spectrum.from_file("boot_.20.fs"),
dadi.Spectrum.from_file("boot_.21.fs"),
dadi.Spectrum.from_file("boot_.22.fs"),
dadi.Spectrum.from_file("boot_.23.fs"),
dadi.Spectrum.from_file("boot_.24.fs"),
dadi.Spectrum.from_file("boot_.25.fs"),
dadi.Spectrum.from_file("boot_.26.fs"),
dadi.Spectrum.from_file("boot_.27.fs"),
dadi.Spectrum.from_file("boot_.28.fs"),
dadi.Spectrum.from_file("boot_.29.fs"),
dadi.Spectrum.from_file("boot_.30.fs"),
dadi.Spectrum.from_file("boot_.31.fs"),
dadi.Spectrum.from_file("boot_.32.fs"),
dadi.Spectrum.from_file("boot_.33.fs"),
dadi.Spectrum.from_file("boot_.34.fs"),
dadi.Spectrum.from_file("boot_.35.fs"),
dadi.Spectrum.from_file("boot_.36.fs"),
dadi.Spectrum.from_file("boot_.37.fs"),
dadi.Spectrum.from_file("boot_.38.fs"),
dadi.Spectrum.from_file("boot_.39.fs"),
dadi.Spectrum.from_file("boot_.40.fs"),
dadi.Spectrum.from_file("boot_.41.fs"),
dadi.Spectrum.from_file("boot_.42.fs"),
dadi.Spectrum.from_file("boot_.43.fs"),
dadi.Spectrum.from_file("boot_.44.fs"),
dadi.Spectrum.from_file("boot_.45.fs"),
dadi.Spectrum.from_file("boot_.46.fs"),
dadi.Spectrum.from_file("boot_.47.fs"),
dadi.Spectrum.from_file("boot_.48.fs"),
dadi.Spectrum.from_file("boot_.49.fs"),
dadi.Spectrum.from_file("boot_.50.fs"),
dadi.Spectrum.from_file("boot_.51.fs"),
dadi.Spectrum.from_file("boot_.52.fs"),
dadi.Spectrum.from_file("boot_.53.fs"),
dadi.Spectrum.from_file("boot_.54.fs"),
dadi.Spectrum.from_file("boot_.55.fs"),
dadi.Spectrum.from_file("boot_.56.fs"),
dadi.Spectrum.from_file("boot_.57.fs"),
dadi.Spectrum.from_file("boot_.58.fs"),
dadi.Spectrum.from_file("boot_.59.fs"),
dadi.Spectrum.from_file("boot_.60.fs"),
dadi.Spectrum.from_file("boot_.61.fs"),
dadi.Spectrum.from_file("boot_.62.fs"),
dadi.Spectrum.from_file("boot_.63.fs"),
dadi.Spectrum.from_file("boot_.64.fs"),
dadi.Spectrum.from_file("boot_.65.fs"),
dadi.Spectrum.from_file("boot_.66.fs"),
dadi.Spectrum.from_file("boot_.67.fs"),
dadi.Spectrum.from_file("boot_.68.fs"),
dadi.Spectrum.from_file("boot_.69.fs"),
dadi.Spectrum.from_file("boot_.70.fs"),
dadi.Spectrum.from_file("boot_.71.fs"),
dadi.Spectrum.from_file("boot_.72.fs"),
dadi.Spectrum.from_file("boot_.73.fs"),
dadi.Spectrum.from_file("boot_.74.fs"),
dadi.Spectrum.from_file("boot_.75.fs"),
dadi.Spectrum.from_file("boot_.76.fs"),
dadi.Spectrum.from_file("boot_.77.fs"),
dadi.Spectrum.from_file("boot_.78.fs"),
dadi.Spectrum.from_file("boot_.79.fs"),
dadi.Spectrum.from_file("boot_.80.fs"),
dadi.Spectrum.from_file("boot_.81.fs"),
dadi.Spectrum.from_file("boot_.82.fs"),
dadi.Spectrum.from_file("boot_.83.fs"),
dadi.Spectrum.from_file("boot_.84.fs"),
dadi.Spectrum.from_file("boot_.85.fs"),
dadi.Spectrum.from_file("boot_.86.fs"),
dadi.Spectrum.from_file("boot_.87.fs"),
dadi.Spectrum.from_file("boot_.88.fs"),
dadi.Spectrum.from_file("boot_.89.fs"),
dadi.Spectrum.from_file("boot_.90.fs"),
dadi.Spectrum.from_file("boot_.91.fs"),
dadi.Spectrum.from_file("boot_.92.fs"),
dadi.Spectrum.from_file("boot_.93.fs"),
dadi.Spectrum.from_file("boot_.94.fs"),
dadi.Spectrum.from_file("boot_.95.fs"),
dadi.Spectrum.from_file("boot_.96.fs"),
dadi.Spectrum.from_file("boot_.97.fs"),
dadi.Spectrum.from_file("boot_.98.fs"),
dadi.Spectrum.from_file("boot_.99.fs"),
dadi.Spectrum.from_file("boot_.100.fs")]
 , p0 , data )
print '**', uncert

#returned [9.93020662e-03 1.28772273e-02 5.12706016e-01 1.61652625e+00 4.30781803e-02 4.88166071e+04] last value is estimated SD of theta

