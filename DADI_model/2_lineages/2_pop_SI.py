import numpy
#site.addsitedir('/scratch/NICO/dadi-1.6.3_modif')  # Seems to be the important line!
import dadi
from dadi import Numerics, PhiManip, Integration, Inference
#import Inference
from dadi.Spectrum_mod import Spectrum


def SI(params, (n1,n2), pts):
    nu1, nu2, Ts = params
    """
    Model of standard isolation.
    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    Ts: Time of divergence in continuous migration.
    n1,n2: Size of fs to generate.
    pts: Number of points to use in grid for evaluation.
    """
    xx = dadi.Numerics.default_grid(pts)
    phi = dadi.PhiManip.phi_1D(xx)
    phi = dadi.PhiManip.phi_1D_to_2D(xx, phi)
    phi = dadi.Integration.two_pops(phi, xx, Ts, nu1, nu2, m12=0, m21=0)
    fs = dadi.Spectrum.from_phi(phi, (n1,n2), (xx,xx), pop_ids=['SM', 'OT'])

    return fs
best, opt = '', -100000.0
for jj in range(0,10):

    func = SI
    dd = dadi.Misc.make_data_dict('sfs.xls')
    data = dadi.Spectrum.from_data_dict(dd, ['SM', 'OT'], [50, 50], polarized=True)
    ns = data.sample_sizes
    print ns
    pts_l = [ns[0] + 5, ns[0] + 10, ns[0] + 15]

    params =      [1, 1, 1]
    upper_bound = [10, 10, 10]
    lower_bound = [ 0.01, 0.01, 0.01]

    func_ex = dadi.Numerics.make_extrap_log_func(func)  # Makde the extrapolating version of our demographic model function.

    model = func_ex(params, ns, pts_l)  # Calculate the model AFS.

    ll_model = dadi.Inference.ll_multinom(model, data)  # Likelihood of the data given the model AFS.

    theta = dadi.Inference.optimal_sfs_scaling(model, data)  # The optimal value of theta given the model.

    print 'Model log-likelihood:', ll_model, 'and theta', theta
    p0 = dadi.Misc.perturb_params(params, fold=1, lower_bound=lower_bound, upper_bound=upper_bound)


    popt = dadi.Inference.optimize_log(p0, data, func_ex, pts_l, lower_bound=lower_bound, upper_bound=upper_bound, maxiter=10000, verbose=1)


    model = func_ex(popt, ns, pts_l)
    ll_opt = dadi.Inference.ll_multinom(model, data)
    theta = dadi.Inference.optimal_sfs_scaling(model, data)
    AIC= 2*len(params)-2*ll_opt
    print 'Optimized log-likelihood:', ll_opt, 'AIC:', AIC, 'Theta:', theta
    print 'Parameters:', popt


    if float(ll_opt) > opt:
        opt = ll_opt
        best = str(popt).replace('\n','')



    fout = open('2pops_SI.xls','a')
    fout.write('1st_anneal_optimization\t2pops_SI\t' + str(ll_opt) + '\t' + str(theta) + '\t' + str(popt).replace('\n','') + '\t' + str(AIC) + '\n')

    fout.close()

print opt, best
newparm = []
print best.split(' ')
for x in best.split(' '):

    newparm.append(float(x.replace('[','').replace(' ','').replace(']','').replace(',','')))
    up, lw = [], []
    for x,y,z in zip(newparm,upper_bound,lower_bound):
        if x == y:            up.append(x * 10)
        else:            up.append(y)
        if x == z:            lw.append(x / 10 )
        else:            lw.append(z)

print 'second optimization'
print 'new parameters', newparm
print 'new upper bounds', up
print 'new lower bounds', lw

for jj in range(0, 5):
    func = SI
    dd = dadi.Misc.make_data_dict('sfs.xls')
    data = dadi.Spectrum.from_data_dict(dd, ['SM', 'OT'], [50, 50], polarized=True)
    ns = data.sample_sizes
    print ns
    pts_l = [ns[0] + 5, ns[0] + 10, ns[0] + 15]

    func_ex = dadi.Numerics.make_extrap_log_func(func)  # Makde the extrapolating version of our demographic model function.
    model = func_ex(newparm, ns, pts_l)  # Calculate the model AFS.
    ll_model = dadi.Inference.ll_multinom(model, data)  # Likelihood of the data given the model AFS.
    theta = dadi.Inference.optimal_sfs_scaling(model, data)  # The optimal value of theta given the model.
    print 'Model log-likelihood:', ll_model, 'and theta', theta
    p0 = dadi.Misc.perturb_params(newparm, fold=1, lower_bound=lw,upper_bound=up)
    popt = dadi.Inference.optimize_log(p0,  data, func_ex, pts_l, lower_bound=lw,upper_bound=up, maxiter=1000, verbose=1)
    model = func_ex(popt, ns, pts_l)
    ll_opt = dadi.Inference.ll_multinom(model, data)
    theta = dadi.Inference.optimal_sfs_scaling(model, data)

    AIC= 2*len(params)-2*ll_opt
    print 'Optimized log-likelihood:', ll_opt, 'AIC:', AIC, 'Theta:', theta
    print 'Parameters:', popt


    fout = open('2pops_SI.xls','a')
    fout.write('2nd_otimization\t2pops_SI\t' + str(ll_opt) + '\t' + str(theta) + '\t' + str(popt).replace('\n','') + '\t' + str(AIC) + '\n')
    fout.close()
