import unittest
import numpy as np
from .bpll import *
from flavio.physics.eft import WilsonCoefficients
from flavio.physics.bdecays.wilsoncoefficients import wctot_dict

s = 1.519267515435317e+24

par = {
    'm_e': 0.510998928e-3,
    'm_mu': 105.6583715e-3,
    'm_tau': 1.77686,
    'm_B+': 5.27929,
    'm_B0': 5.27961,
    'm_K0': 0.497611,
    'm_K+': 0.493677,
    'tau_B+': 1638.e-15*s,
    'Gmu': 1.1663787e-5,
    'alpha_e': 1/127.940,
    'alpha_s': 0.1185,
    'm_Z': 91.1876,
    'm_b': 4.17,
    'm_t': 173.21,
    'm_c': 1.275,
    'Vus': 0.22,
    'Vub': 3.7e-3,
    'Vcb': 4.1e-2,
    'gamma': 1.22,
# table XII of 1509.06235v1
    ('formfactor','B->K','a0_f+'): 0.466,
    ('formfactor','B->K','a1_f+'): -0.885,
    ('formfactor','B->K','a2_f+'): -0.213,
    ('formfactor','B->K','a0_f0'): 0.292,
    ('formfactor','B->K','a1_f0'): 0.281,
    ('formfactor','B->K','a2_f0'): 0.150,
    ('formfactor','B->K','a0_fT'): 0.460,
    ('formfactor','B->K','a1_fT'): -1.089,
    ('formfactor','B->K','a2_fT'): -1.114,
}

wc_obj = WilsonCoefficients()
wc = wctot_dict(wc_obj, 'bsmumu', 4.2, par)

class TestBPll(unittest.TestCase):
    def test_bkll(self):
        # rough numerical test for branching ratio at high q^2 comparing to 1510.02349
        self.assertAlmostEqual(bpll_dbrdq2(16., wc_obj, par, 'B+', 'K+', 'mu')*1e8/(4.615/2.), 1, places=1)
