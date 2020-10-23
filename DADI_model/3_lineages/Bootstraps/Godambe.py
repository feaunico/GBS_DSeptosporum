"""
Parameter uncertainties and likelihood ratio tests using Godambe information.
"""
import numpy

from dadi import Inference
from dadi.Spectrum_mod import Spectrum

print("""If you use the Godambe methods in your published research, please cite Coffman et al. (2016) in addition to the main dadi paper Gutenkunst et al. (2009).
AJ Coffman, P Hsieh, S Gravel, RN Gutenkunst "Computationally efficient composite likelihood statistics for demographic inference" Molecular Biology and Evolution 33:591-593 (2016)""")

def hessian_elem(func, f0, p0, ii, jj, eps, args=(), one_sided=None):
    """
    Calculate element [ii][jj] of the Hessian matrix, a matrix
    of partial second derivatives w.r.t. to parameters ii and jj
        
    func: Model function
    f0: Evaluation of func at p0
    p0: Parameters for func
    eps: List of absolute step sizes to use for each parameter when taking
         finite differences.
    args: Additional arguments to func
    one_sided: Optionally, pass in a sequence of length p0 that determines
               whether a one-sided derivative will be used for each parameter.
    """
    # Note that we need to specify dtype=float, to avoid this being an integer
    # array which will silently fail when adding fractional eps.
    if one_sided is None:
        one_sided = [False]*len(p0)

    pwork = numpy.array(p0, copy=True, dtype=float)
    if ii == jj:
        if pwork[ii] != 0 and not one_sided[ii]:
            pwork[ii] = p0[ii] + eps[ii]
            fp = func(pwork, *args)
            
            pwork[ii] = p0[ii] - eps[ii]
            fm = func(pwork, *args)
            
            element = (fp - 2*f0 + fm)/eps[ii]**2
        else:
            pwork[ii] = p0[ii] + 2*eps[ii]
            fpp = func(pwork, *args)
            
            pwork[ii] = p0[ii] + eps[ii]
            fp = func(pwork, *args)

            element = (fpp - 2*fp + f0)/eps[ii]**2
    else:
        if pwork[ii] != 0 and pwork[jj] != 0 and not one_sided[ii] and not one_sided[jj]:
            # f(xi + hi, xj + h)
            pwork[ii] = p0[ii] + eps[ii]
            pwork[jj] = p0[jj] + eps[jj]
            fpp = func(pwork, *args)
            
            # f(xi + hi, xj - hj)
            pwork[ii] = p0[ii] + eps[ii]
            pwork[jj] = p0[jj] - eps[jj]
            fpm = func(pwork, *args)
            
            # f(xi - hi, xj + hj)
            pwork[ii] = p0[ii] - eps[ii]
            pwork[jj] = p0[jj] + eps[jj]
            fmp = func(pwork, *args)
            
            # f(xi - hi, xj - hj)
            pwork[ii] = p0[ii] - eps[ii]
            pwork[jj] = p0[jj] - eps[jj]
            fmm = func(pwork, *args)

            element = (fpp - fpm - fmp + fmm)/(4 * eps[ii]*eps[jj])
        else:
            # f(xi + hi, xj + h)
            pwork[ii] = p0[ii] + eps[ii]
            pwork[jj] = p0[jj] + eps[jj]
            fpp = func(pwork, *args)
            
            # f(xi + hi, xj)
            pwork[ii] = p0[ii] + eps[ii]
            pwork[jj] = p0[jj]
            fpm = func(pwork, *args)
            
            # f(xi, xj + hj)
            pwork[ii] = p0[ii]
            pwork[jj] = p0[jj] + eps[jj]
            fmp = func(pwork, *args)
            
            element = (fpp - fpm - fmp + f0)/(eps[ii]*eps[jj])
    return element

def get_hess(func, p0, eps, args=()):
    """
    Calculate Hessian matrix of partial second derivatives. 
    Hij = dfunc/(dp_i dp_j)
    
    func: Model function
    p0: Parameter values to take derivative around
    eps: Fractional stepsize to use when taking finite-difference derivatives
         Note that if eps*param is < 1e-6, then the step size for that parameter
         will simply be eps, to avoid numerical issues with small parameter
         perturbations.
    args: Additional arguments to func
    """
    # Calculate step sizes for finite-differences.
    eps_in = eps
    eps = numpy.empty([len(p0)])
    one_sided = [False]*len(p0)
    for i, pval in enumerate(p0):
        if pval != 0:
            # Account for floating point arithmetic issues
            if pval*eps_in < 1e-6:
                eps[i] = eps_in
                one_sided[i] = True
            else:
                eps[i] = eps_in*pval
        else:
            # Account for parameters equal to zero
            eps[i] = eps_in

    f0 = func(p0, *args)
    hess = numpy.empty((len(p0), len(p0)))
    for ii in range(len(p0)):
        for jj in range(ii, len(p0)):
            hess[ii][jj] = hessian_elem(func, f0, p0, ii, jj, eps, args=args, one_sided=one_sided)
            hess[jj][ii] = hess[ii][jj]
    return hess

def get_grad(func, p0, eps, args=()):
    """
    Calculate gradient vector
    
    func: Model function
    p0: Parameters for func
    eps: Fractional stepsize to use when taking finite-difference derivatives
         Note that if eps*param is < 1e-6, then the step size for that parameter
         will simply be eps, to avoid numerical issues with small parameter
         perturbations.
    args: Additional arguments to func
    """
    # Calculate step sizes for finite-differences.
    eps_in = eps
    eps = numpy.empty([len(p0)])
    one_sided = [False]*len(p0)
    for i, pval in enumerate(p0):
        if pval != 0:
            # Account for floating point arithmetic issues
            if pval*eps_in < 1e-6:
                eps[i] = eps_in
                one_sided[i] = True
            else:
                eps[i] = eps_in*pval
        else:
            # Account for parameters equal to zero
            eps[i] = eps_in

    grad = numpy.empty([len(p0), 1])
    for ii in range(len(p0)):
        pwork = numpy.array(p0, copy=True, dtype=float)

        if p0[ii] != 0 and not one_sided[ii]:
            pwork[ii] = p0[ii] + eps[ii]
            fp = func(pwork, *args)

            pwork[ii] = p0[ii] - eps[ii]
            fm = func(pwork, *args)

            grad[ii] = (fp - fm)/(2*eps[ii])
        else:
            # Do one-sided finite-difference 
            pwork[ii] = p0[ii] + eps[ii]
            fp = func(pwork, *args)

            pwork[ii] = p0[ii]
            fm = func(pwork, *args)

            grad[ii] = (fp - fm)/eps[ii]
    return grad

cache = {}
def get_godambe(func_ex, grid_pts, all_boot, p0, data, eps, log=False,
                just_hess=False, boot_theta_adjusts=[]):
    """
    Godambe information and Hessian matrices

    func_ex: Model function
    grid_pts: Number of grid points to evaluate the model function
    all_boot: List of bootstrap frequency spectra
    p0: Best-fit parameters for func_ex.
    data: Original data frequency spectrum
    eps: Fractional stepsize to use when taking finite-difference derivatives
         Note that if eps*param is < 1e-6, then the step size for that parameter
         will simply be eps, to avoid numerical issues with small parameter
         perturbations.
    log: If True, calculate derivatives in terms of log-parameters
    just_hess: If True, only evaluate and return the Hessian matrix
    boot_theta_adjusts: Factors by which to adjust theta for each bootstrap
                        sample, relative to full data theta.
    """
    ns = data.sample_sizes
    if not boot_theta_adjusts:
        boot_theta_adjusts = numpy.ones(len(all_boot))

    # Cache evaluations of the frequency spectrum inside our hessian/J 
    # evaluation function
    def func(params, data, theta_adjust=1):
        key = (tuple(params), tuple(ns), tuple(grid_pts))
        if key not in cache:
            cache[key] = func_ex(params, ns, grid_pts)
        # theta_adjust deals with bootstraps that need  different thetas
        fs = theta_adjust*cache[key]
        return Inference.ll(fs, data)
    def log_func(logparams, data, theta_adjust=1):
        return func(numpy.exp(logparams), data, theta_adjust)

    # First calculate the observed hessian.
    # theta_adjust defaults to 1.
    if not log:
        hess = -get_hess(func, p0, eps, args=[data])
    else:
        hess = -get_hess(log_func, numpy.log(p0), eps, args=[data])

    if just_hess:
        return hess

    # Now the expectation of J over the bootstrap data
    J = numpy.zeros((len(p0), len(p0)))
    # cU is a column vector
    cU = numpy.zeros((len(p0),1))
    for ii, (boot,theta_adjust) in enumerate(zip(all_boot, boot_theta_adjusts)):
        boot = Spectrum(boot)
        if not log:
            grad_temp = get_grad(func, p0, eps, args=[boot, theta_adjust])
        else:
            grad_temp = get_grad(log_func, numpy.log(p0), eps,
                                 args=[boot, theta_adjust])
        J_temp = numpy.outer(grad_temp, grad_temp)
        J = J + J_temp
        cU = cU + grad_temp
    J = J/len(all_boot)
    cU = cU/len(all_boot)

    # G = H*J^-1*H
    J_inv = numpy.linalg.inv(J)
    godambe = numpy.dot(numpy.dot(hess, J_inv), hess)
    return godambe, hess, J, cU

def GIM_uncert(func_ex, grid_pts, all_boot, p0, data, log=False,
               multinom=True, eps=0.01, return_GIM=False,
               boot_theta_adjusts=None):
    """
    Parameter uncertainties from Godambe Information Matrix (GIM)

    Returns standard deviations of parameter values.

    func_ex: Model function
    all_boot: List of bootstrap frequency spectra
    p0: Best-fit parameters for func_ex
    data: Original data frequency spectrum
    eps: Fractional stepsize to use when taking finite-difference derivatives.
         Note that if eps*param is < 1e-6, then the step size for that parameter
         will simply be eps, to avoid numerical issues with small parameter
         perturbations.
    log: If True, assume log-normal distribution of parameters. Returned values
         are then the standard deviations of the *logs* of the parameter values,
         which can be interpreted as relative parameter uncertainties.
    multinom: If True, assume model is defined without an explicit parameter for
              theta. Because uncertainty in theta must be accounted for to get
              correct uncertainties for other parameters, this function will
              automatically consider theta if multinom=True. In that case, the
              final entry of the returned uncertainties will correspond to
              theta.
    return_GIM: If true, also return the full GIM.
    boot_theta_adjusts: Optionally, a sequence of *relative* values of theta
                        (compared to original data) to assume for bootstrap
                        data sets. Only valid when multinom=False.
    """
    if multinom:
        if boot_theta_adjusts:
            raise ValueError('boot_thetas option can only be used with '
                             'multinom=False')
        func_multi = func_ex
        model = func_multi(p0, data.sample_sizes, grid_pts)
        theta_opt = Inference.optimal_sfs_scaling(model, data)
        p0 = list(p0) + [theta_opt]
        func_ex = lambda p, ns, pts: p[-1]*func_multi(p[:-1], ns, pts)
    GIM, H, J, cU = get_godambe(func_ex, grid_pts, all_boot, p0, data, eps, log,
                                boot_theta_adjusts=boot_theta_adjusts)
    uncerts = numpy.sqrt(numpy.diag(numpy.linalg.inv(GIM)))
    if not return_GIM:
        return uncerts
    else:
        return uncerts, GIM

def FIM_uncert(func_ex, grid_pts, p0, data, log=False, multinom=True, eps=0.01):
    """
    Parameter uncertainties from Fisher Information Matrix

    Returns standard deviations of parameter values.

    func_ex: Model function
    all_boot: List of bootstrap frequency spectra
    p0: Best-fit parameters for func_ex
    data: Original data frequency spectrum
    eps: Fractional stepsize to use when taking finite-difference derivatives.
         Note that if eps*param is < 1e-6, then the step size for that parameter
         will simply be eps, to avoid numerical issues with small parameter
         perturbations.
    log: If True, assume log-normal distribution of parameters. Returned values
         are then the standard deviations of the *logs* of the parameter values,
         which can be interpreted as relative parameter uncertainties.
    multinom: If True, assume model is defined without an explicit parameter for
              theta. Because uncertainty in theta must be accounted for to get
              correct uncertainties for other parameters, this function will
              automatically consider theta if multinom=True. In that case, the
              final entry of the returned uncertainties will correspond to
              theta.
    """
    if multinom:
        func_multi = func_ex
        model = func_multi(p0, data.sample_sizes, grid_pts)
        theta_opt = Inference.optimal_sfs_scaling(model, data)
        p0 = list(p0) + [theta_opt]
        func_ex = lambda p, ns, pts: p[-1]*func_multi(p[:-1], ns, pts)
    H = get_godambe(func_ex, grid_pts, [], p0, data, eps, log, just_hess=True)
    return numpy.sqrt(numpy.diag(numpy.linalg.inv(H)))

def LRT_adjust(func_ex, grid_pts, all_boot, p0, data, nested_indices,
               multinom=True, eps=0.01):
    # XXX: Need to implement boot_theta_adjusts
    """
    First-order moment matching adjustment factor for likelihood ratio test

    func_ex: Model function for complex model
    grid_pts: Grid points at which to evaluate func_ex
    all_boot: List of bootstrap frequency spectra
    p0: Best-fit parameters for the simple model, with nested parameter
        explicity defined.  Although equal to values for simple model, should
        be in a list form that can be taken in by the complex model you'd like
        to evaluate.
    data: Original data frequency spectrum
    nested_indices: List of positions of nested parameters in complex model
                    parameter list
    multinom: If True, assume model is defined without an explicit parameter for
              theta. Because uncertainty in theta must be accounted for to get
              correct uncertainties for other parameters, this function will
              automatically consider theta if multinom=True.
    eps: Fractional stepsize to use when taking finite-difference derivatives
         Note that if eps*param is < 1e-6, then the step size for that parameter
         will simply be eps, to avoid numerical issues with small parameter
         perturbations.
    """
    if multinom:
        func_multi = func_ex
        model = func_multi(p0, data.sample_sizes, grid_pts)
        theta_opt = Inference.optimal_sfs_scaling(model, data)
        p0 = list(p0) + [theta_opt]
        func_ex = lambda p, ns, pts: p[-1]*func_multi(p[:-1], ns, pts)

    # We only need to take derivatives with respect to the parameters in the
    # complex model that have been set to specified values in the simple model
    def diff_func(diff_params, ns, grid_pts):
        # diff_params argument is only the nested parameters. All the rest
        # should come from p0
        full_params = numpy.array(p0, copy=True, dtype=float)
        # Use numpy indexing to set relevant parameters
        full_params[nested_indices] = diff_params
        return func_ex(full_params, ns, grid_pts)

    p_nested = numpy.asarray(p0)[nested_indices]
    GIM, H, J, cU = get_godambe(diff_func, grid_pts, all_boot, p_nested, data, 
                                eps, log=False)

    adjust = len(nested_indices)/numpy.trace(numpy.dot(J, numpy.linalg.inv(H)))
    return adjust

def sum_chi2_ppf(x, weights=(0,1)):
    """
    Percent point function (inverse of cdf) of weighted sum of chi^2
    distributions.

    x: Value(s) at which to evaluate ppf
    weights: Weights of chi^2 distributions, beginning with zero d.o.f.
             For example, weights=(0,1) is the normal chi^2 distribution with 1
             d.o.f. For single parameters on the boundary, the correct
             distribution for the LRT is 0.5*chi^2_0 + 0.5*chi^2_1, which would
             be weights=(0.5,0.5).
    """
    import scipy.stats.distributions as ssd
    # Ensure that weights are valid
    if abs(numpy.sum(weights) - 1) > 1e-6:
        raise ValueError('Weights must sum to 1.')
    # A little clunky, but we want to handle x = 0.5, and x = [2, 3, 4]
    # correctly. So if x is a scalar, we record that fact so we can return a
    # scalar on output.
    if numpy.isscalar(x):
        scalar_input = True
    # Convert x into an array, so we can index it easily.
    x = numpy.atleast_1d(x)
    # Calculate total cdf of all chi^2 dists with dof > 1.
    # (ssd.chi2.cdf(x,0) is always nan, so we avoid that.)
    cdf = numpy.sum([w*ssd.chi2.cdf(x, d+1) for (d, w)
                     in enumerate(weights[1:])], axis=0)
    # Add in contribution from 0 d.o.f.
    cdf[x > 0] += weights[0]
    # Convert to ppf
    ppf = 1-cdf

    if scalar_input:
        return ppf[0]
    else:
        return ppf

def Wald_stat(func_ex, grid_pts, all_boot, p0, data, nested_indices,
              full_params, multinom=True, eps=0.01, adj_and_org=False):
    # XXX: Implement boot_theta_adjusts
    """
    Calculate test stastic from wald test
             
    func_ex: Model function for complex model
    all_boot: List of bootstrap frequency spectra
    p0: Best-fit parameters for the simple model, with nested parameter
        explicity defined.  Although equal to values for simple model, should
        be in a list form that can be taken in by the complex model you'd like
        to evaluate.
    data: Original data frequency spectrum
    nested_indices: List of positions of nested parameters in complex model
    parameter list
    full_params: Parameter values for parameters found only in complex model,
                 Can either be array with just values found only in the compelx
                 model, or entire list of parameters from complex model.
    multinom: If True, assume model is defined without an explicit parameter for
              theta. Because uncertainty in theta must be accounted for to get
              correct uncertainties for other parameters, this function will
              automatically consider theta if multinom=True. In that case, the
              final entry of the returned uncertainties will correspond to
              theta.
    eps: Fractional stepsize to use when taking finite-difference derivatives
         Note that if eps*param is < 1e-6, then the step size for that parameter
         will simply be eps, to avoid numerical issues with small parameter
         perturbations.
    adj_and_org: If False, return only adjusted Wald statistic. If True, also
                 return unadjusted statistic as second return value.
    """
    if multinom:
         func_multi = func_ex
         model = func_multi(p0, data.sample_sizes, grid_pts)
         theta_opt = Inference.optimal_sfs_scaling(model, data)
         # Also need to extend full_params
         if len(full_params) == len(p0):
             full_params = numpy.concatenate((full_params, [theta_opt]))
         p0 = list(p0) + [theta_opt]
         func_ex = lambda p, ns, pts: p[-1]*func_multi(p[:-1], ns, pts)
         
    # We only need to take derivatives with respect to the parameters in the
    # complex model that have been set to specified values in the simple model
    def diff_func(diff_params, ns, grid_pts):
         # diff_params argument is only the nested parameters. All the rest
         # should come from p0
         full_params = numpy.array(p0, copy=True, dtype=float)
         # Use numpy indexing to set relevant parameters
         full_params[nested_indices] = diff_params
         return func_ex(full_params, ns, grid_pts)
    
    # Reduce full params list to be same length as nested indices
    if len(full_params) == len(p0):
        full_params = numpy.asarray(full_params)[nested_indices]
    if len(full_params) != len(nested_indices):
        raise KeyError('Full parameters not equal in length to p0 or nested '
                       'indices')

    p_nested = numpy.asarray(p0)[nested_indices]
    GIM, H, J, cU = get_godambe(diff_func, grid_pts, all_boot, p_nested, data, 
                                eps, log=False)
    param_diff = full_params-p_nested

    wald_adj = numpy.dot(numpy.dot(numpy.transpose(param_diff),GIM), param_diff)
    wald_org = numpy.dot(numpy.dot(numpy.transpose(param_diff),H),param_diff)

    if adj_and_org:
        return wald_adj, wald_org
    return wald_adj

def score_stat(func_ex, grid_pts, all_boot, p0, data, nested_indices,
               multinom=True, eps=0.01, adj_and_org=False):
    # XXX: Implement boot_theta_adjusts
    """
    Calculate test stastic from score test
        
    func_ex: Model function for complex model
    grid_pts: Grid points to evaluate model function
    all_boot: List of bootstrap frequency spectra
    p0: Best-fit parameters for the simple model, with nested parameter
        explicity defined.  Although equal to values for simple model, should
        be in a list form that can be taken in by the complex model you'd like
        to evaluate.
    data: Original data frequency spectrum
    nested_indices: List of positions of nested parameters in complex model
                    parameter list
    eps: Fractional stepsize to use when taking finite-difference derivatives
         Note that if eps*param is < 1e-6, then the step size for that parameter
         will simply be eps, to avoid numerical issues with small parameter
         perturbations.
    multinom: If True, assume model is defined without an explicit parameter for
              theta. Because uncertainty in theta must be accounted for to get
              correct uncertainties for other parameters, this function will
              automatically consider theta if multinom=True.
    adj_and_org: If False, return only adjusted score statistic. If True, also
                 return unadjusted statistic as second return value.
    """
    if multinom:
        func_multi = func_ex
        model = func_multi(p0, data.sample_sizes, grid_pts)
        theta_opt = Inference.optimal_sfs_scaling(model, data)
        p0 = list(p0) + [theta_opt]
        func_ex = lambda p, ns, pts: p[-1]*func_multi(p[:-1], ns, pts)

    # We only need to take derivatives with respect to the parameters in the
    # complex model that have been set to specified values in the simple model
    def diff_func(diff_params, ns, grid_pts):
        # diff_params argument is only the nested parameters. All the rest
        # should come from p0
        full_params = numpy.array(p0, copy=True, dtype=float)
        # Use numpy indexing to set relevant parameters
        full_params[nested_indices] = diff_params
        return func_ex(full_params, ns, grid_pts)

    p_nested = numpy.asarray(p0)[nested_indices]
    GIM, H, J, cU = get_godambe(diff_func, grid_pts, all_boot, p_nested, data, 
                                eps, log=False)
    
    score_org = numpy.dot(numpy.dot(numpy.transpose(cU),
                                    numpy.linalg.inv(H)),cU)[0,0]
    score_adj = numpy.dot(numpy.dot(numpy.transpose(cU),
                                    numpy.linalg.inv(J)),cU)[0,0]

    if adj_and_org:
        return score_adj, score_org
    return score_adj

