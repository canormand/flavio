r"""Functions for exclusive $\Lambda_b\to \Lambda\ell^+\ell^-$ decays."""

import flavio
from math import sqrt,pi
from flavio.physics.bdecays.common import lambda_K, beta_l, meson_quark, meson_ff
from flavio.classes import Observable, Prediction, AuxiliaryQuantity
import warnings


def helicity_amps(q2, mLb, mL, ff):
    """$\Lambda_b\to \Lambda\ell^+\ell^-$ helicity amplitudes.

    See (3.12)-(3.15) of arXiv:1410.2115."""
    sp = (mLb + mL)**2 - q2
    sm = (mLb - mL)**2 - q2
    H = {}
    H['0V++'] = ff['fV0'] * (mLb + mL)/sqrt(q2) * sqrt(sm)
    H['+V-+'] = -ff['fVperp'] * sqrt(2*sm)
    H['0A++'] = ff['fA0'] * (mLb - mL)/sqrt(q2) * sqrt(sp)
    H['+A-+'] = -ff['fAperp'] * sqrt(2*sp)
    H['0T++'] = -ff['fT0'] * sqrt(q2) * sqrt(sm)
    H['+T-+'] = ff['fTperp'] * (mLb + mL) * sqrt(2*sm)
    H['0T5++'] = ff['fT50'] * sqrt(q2) * sqrt(sp)
    H['+T5-+'] = -ff['fT5perp'] * (mLb - mL) * sqrt(2*sp)
    H['0V--'] = H['0V++']
    H['+V+-'] = H['+V-+']
    H['0A--'] = -H['0A++']
    H['+A+-'] = -H['+A-+']
    H['0T--'] = H['0T++']
    H['+T+-'] = H['+T-+']
    H['0T5--'] = -H['0T5++']
    H['+T5+-'] = -H['+T5-+']
    return H

def transverity_amps(ha, q2, mLb, mL, mqh, mql, wc, prefactor):
    r"""Transversity amplitudes for $\Lambda_b\to \Lambda\ell^+\ell^-$.

    See (3.16) of arXiv:1410.2115."""
    C910Lpl = (wc['v'] - wc['a']) + (wc['vp'] - wc['ap'])
    C910Rpl = (wc['v'] + wc['a']) + (wc['vp'] + wc['ap'])
    C910Lmi = (wc['v'] - wc['a']) - (wc['vp'] - wc['ap'])
    C910Rmi = (wc['v'] + wc['a']) - (wc['vp'] + wc['ap'])
    A = {}
    A['perp1', 'L'] = +sqrt(2)*( C910Lpl *ha['+V-+']
                                 - 2*mqh*(wc['7']+wc['7p'])/q2 * ha['+T-+'] )
    A['perp1', 'R'] = +sqrt(2)*( C910Rpl *ha['+V-+']
                                 - 2*mqh*(wc['7']+wc['7p'])/q2 * ha['+T-+'] )
    A['para1', 'L'] = -sqrt(2)*( C910Lmi *ha['+A-+']
                                 + 2*mqh*(wc['7']-wc['7p'])/q2 * ha['+T5-+'] )
    A['para1', 'R'] = -sqrt(2)*( C910Rmi *ha['+A-+']
                                 + 2*mqh*(wc['7']-wc['7p'])/q2 * ha['+T5-+'] )
    A['perp0', 'L'] = +sqrt(2)*( C910Lpl *ha['0V++']
                                 - 2*mqh*(wc['7']+wc['7p'])/q2 * ha['0T++'] )
    A['perp0', 'R'] = +sqrt(2)*( C910Rpl *ha['0V++']
                                 - 2*mqh*(wc['7']+wc['7p'])/q2 * ha['0T++'] )
    A['para0', 'L'] = -sqrt(2)*( C910Lmi *ha['0A++']
                                 + 2*mqh*(wc['7']-wc['7p'])/q2 * ha['0T5++'] )
    A['para0', 'R'] = -sqrt(2)*( C910Rmi *ha['0A++']
                                 + 2*mqh*(wc['7']-wc['7p'])/q2 * ha['0T5++'] )
    return {k: prefactor*v for k, v in A.items()}

def angular_coefficients(ta, alpha):
    r"""Angular coefficients of $\Lambda_b\to \Lambda\ell^+\ell^-$ in terms of
    transversity amplitudes and decay parameter $\alpha$.

    See (3.29)-(3.32) of arXiv:1410.2115."""
    K = {}
    K['1ss'] = 1/4.*(   abs(ta['perp1', 'R'])**2 + abs(ta['perp1', 'L'])**2
                      + abs(ta['para1', 'R'])**2 + abs(ta['para1', 'L'])**2
                      + 2*abs(ta['perp0', 'R'])**2 + 2*abs(ta['perp0', 'L'])**2
                      + 2*abs(ta['para0', 'R'])**2 + 2*abs(ta['para0', 'L'])**2 )
    K['1cc'] = 1/2.*(   abs(ta['perp1', 'R'])**2 + abs(ta['perp1', 'L'])**2
                      + abs(ta['para1', 'R'])**2 + abs(ta['para1', 'L'])**2 )
    K['1c'] = -(  ta['perp1', 'R'] * ta['para1', 'R'].conj()
                - ta['perp1', 'L'] * ta['para1', 'L'].conj() ).real
    K['2ss'] = alpha/2. * (  ta['perp1', 'R'] * ta['para1', 'R'].conj()
                       + 2 * ta['perp0', 'R'] * ta['para0', 'R'].conj()
                           + ta['perp1', 'L'] * ta['para1', 'L'].conj()
                       + 2 * ta['perp0', 'L'] * ta['para0', 'L'].conj() ).real
    K['2cc'] = alpha * (  ta['perp1', 'R'] * ta['para1', 'R'].conj()
                        + ta['perp1', 'L'] * ta['para1', 'L'].conj() ).real
    K['2c'] = -alpha/2.*(   abs(ta['perp1', 'R'])**2 - abs(ta['perp1', 'L'])**2
                          + abs(ta['para1', 'R'])**2 - abs(ta['para1', 'L'])**2 )
    K['3sc'] = alpha/sqrt(2) * ( ta['perp1', 'R'] * ta['perp0', 'R'].conj()
                               - ta['para1', 'R'] * ta['para0', 'R'].conj()
                               + ta['perp1', 'L'] * ta['perp0', 'L'].conj()
                               - ta['para1', 'L'] * ta['para0', 'L'].conj() ).imag
    K['3s'] = alpha/sqrt(2) * ( ta['perp1', 'R'] * ta['para0', 'R'].conj()
                              - ta['para1', 'R'] * ta['perp0', 'R'].conj()
                              - ta['perp1', 'L'] * ta['para0', 'L'].conj()
                              + ta['para1', 'L'] * ta['perp0', 'L'].conj() ).imag
    K['4sc'] = alpha/sqrt(2) * ( ta['perp1', 'R'] * ta['para0', 'R'].conj()
                               - ta['para1', 'R'] * ta['perp0', 'R'].conj()
                               + ta['perp1', 'L'] * ta['para0', 'L'].conj()
                               - ta['para1', 'L'] * ta['perp0', 'L'].conj() ).imag
    K['4s'] = alpha/sqrt(2) * ( ta['perp1', 'R'] * ta['perp0', 'R'].conj()
                              - ta['para1', 'R'] * ta['para0', 'R'].conj()
                              - ta['perp1', 'L'] * ta['perp0', 'L'].conj()
                              + ta['para1', 'L'] * ta['para0', 'L'].conj() ).imag
    return K


def get_transverity_amps(q2, wc_obj, par_dict, lep, cp_conjugate):
    par = par_dict.copy()
    if cp_conjugate:
        par = conjugate_par(par)
    scale = flavio.config['renormalization scale']['lambdab']
    mLb = par['m_Lambdab']
    mL = par['m_Lambda']
    mb = flavio.physics.running.running.get_mb(par, scale)
    ff_aux = AuxiliaryQuantity.get_instance('Lambdab->Lambda form factor')
    ff = ff_aux.prediction(par_dict=par, wc_obj=None, q2=q2)
    wc = flavio.physics.bdecays.wilsoncoefficients.wctot_dict(wc_obj, 'bs' + lep + lep, scale, par)
    wc_eff = flavio.physics.bdecays.wilsoncoefficients.get_wceff(q2, wc, par, 'Lambdab', 'Lambda', lep, scale)
    ha = helicity_amps(q2, mLb, mL, ff)
    xi_t = flavio.physics.ckm.xi('t','bs')(par)
    alphaem = flavio.physics.running.running.get_alpha(par, scale)['alpha_e']
    la_K = flavio.physics.bdecays.common.lambda_K(mLb**2, mL**2, q2)
    N = par['GF'] * xi_t * alphaem * sqrt(q2) * la_K**(1/4.) / sqrt(3 * 2 * mLb**3 * pi**5) / 32.
    ta_ff = transverity_amps(ha, q2, mLb, mL, mb, 0, wc_eff, N)
    return ta_ff

def get_obs(function, q2, wc_obj, par, lep):
    ml = par['m_'+lep]
    mLb = par['m_Lambdab']
    mL = par['m_Lambda']
    if q2 < 4*ml**2 or q2 > (mLb-mL)**2:
        return 0
    ta = get_transverity_amps(q2, wc_obj, par, lep, cp_conjugate=False)
    alpha = par['Lambda->ppi alpha_-']
    K = angular_coefficients(ta, alpha)
    return function(K)

def dGdq2(K):
    return 2*K['1ss'] + K['1cc']

def dbrdq2(q2, wc_obj, par, lep):
    tauLb = par['tau_Lambdab']
    return tauLb * get_obs(dGdq2, q2, wc_obj, par, lep)

def dbrdq2_int(q2min, q2max, wc_obj, par, lep):
    def obs(q2):
        return dbrdq2(q2, wc_obj, par, lep)
    return flavio.math.integrate.nintegrate(obs, q2min, q2max)/(q2max-q2min)

# Functions returning functions needed for Prediction instances

def dbrdq2_int_func(lep):
    def fct(wc_obj, par, q2min, q2max):
        return dbrdq2_int(q2min, q2max, wc_obj, par, lep)
    return fct

def dbrdq2_func(lep):
    def fct(wc_obj, par, q2):
        return dbrdq2(q2, wc_obj, par, lep)
    return fct


_tex = {'e': 'e', 'mu': '\mu', 'tau': r'\tau'}

for l in ['e', 'mu', ]: # tau requires lepton mass dependence!

        # binned branching ratio
        _obs_name = "<dBR/dq2>(Lambdab->Lambda"+l+l+")"
        _obs = Observable(name=_obs_name, arguments=['q2min', 'q2max'])
        _obs.set_description(r"Binned differential branching ratio of $\Lambda_b\to\Lambda " +_tex[l]+r"^+"+_tex[l]+"^-$")
        _obs.tex = r"$\langle \frac{d\text{BR}}{dq^2} \rangle(\Lambda_b\to\Lambda " +_tex[l]+r"^+"+_tex[l]+"^-)$"
        Prediction(_obs_name, dbrdq2_int_func(l))

        # differential branching ratio
        _obs_name = "dBR/dq2(Lambdab->Lambda"+l+l+")"
        _obs = Observable(name=_obs_name, arguments=['q2'])
        _obs.set_description(r"Differential branching ratio of $\Lambda_b\to\Lambda " +_tex[l]+r"^+"+_tex[l]+"^-$")
        _obs.tex = r"$\frac{d\text{BR}}{dq^2}(\Lambda_b\to\Lambda " +_tex[l]+r"^+"+_tex[l]+"^-)$"
        Prediction(_obs_name, dbrdq2_func(l))
