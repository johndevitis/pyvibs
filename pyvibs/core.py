import numpy as np
from scipy import linalg, interpolate
import matplotlib.pyplot as plt
from scipy import spatial



class FRF():
    pass

class DataLogger():
    pass

class DataTrigger():
    pass



class MAC():

    def __init__(self,u1,u2,**kwargs):
        self.u1 = u1
        self.u2 = u2
        self.m = get_mac(u1,u2)

    def __repr__(self):
        return 'Modal Assurance Criterion:\n{}'.format(self.m)

    def plot(self):
        plt.figure()
        plt.imshow(self.m, aspect='auto', interpolation='none')
        plt.show()



def get_mac(U1,U2):
    """
    returns modal assurance criterion (MAC). U1 and U2 numpy arrays should
    be in the form of [ndof x nmodes].
    modal arrays can have a different number of modes (columns) but must retain the same
    number of DOF (rows).
    suitable for the general case of real normal modes and complex modes. that is, the hermitian operations are performed.
    """
    nm1, nm2 = np.shape(U1)[1], np.shape(U2)[1]
    m = np.empty((nm1,nm2))
    for ii in range(nm1):
        for jj in range(nm2):
            m[ii,jj] = _mac_single(U1[:,ii],U2[:,jj])
    return m


def _mac_single(u1,u2):
    """ macro for get_mac function. returns mac value for 1d arrays"""
    return (np.inner(u1.conj(),u2)*np.inner(u2.conj(),u1)) / (np.inner(u1.conj(),u1)*np.inner(u2.conj(),u2))



def pair_modes(u1,u2):
    """pairs to shape arrays. returns a list of pairids"""
    
    # get modal assurance criterion
    m = get_mac(u1,u2)
    # sort from 0->1 in terms of shape 'likeness'
    ms = np.argsort(m)

    # return indices of best shape pairs (pairing u2 [slave] to u1 [master])
    pairid = ms[:,-1]

    # remove pairs retaining order
    # WORKS ONLY IN PYTHON VERSIONS >= 3.6
    # TODO: check python version
    #import sys
    #if sys.version_info >= (3,6):
    #    pairid = list(dict.fromkeys(pairid)))
    #else:
    #    pairid = unique(pairid)
    return list(dict.fromkeys(pairid))


def snap2(array,value):
    """finds and returns the nearest value in array"""
    idx = (np.abs(array-value)).argmin()
    return array[idx]


def search(array,value):
    """
    uses search to find nearest neighbor in array and returns value.
    works for n dimensional data
    """
    return spatial.KDTree(array).query(value)[1]


def snap(array,value):
    """
    snaps value to nearest neighbor in array. uses scipy's spatial.KDTree for nearest-neighbor lookup.
    works for n dimensional data
    """
    idx = spatial.KDTree(array).query(value)[1]
    return array[idx]


def unique(seq):
    """
    return array of unique values with the original order preserved
    (i.e. only returns first values found in order)
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def mag2db(x):
    """ converts magnitude to decibles """
    return 20*np.log10(x)


def hermit(x):
    """
    return Hermitian of numpy array, x. this is equivalent to taking the complex
    conjugate transpose
    """
    return x.conj().T


def freq_residual(f1,f2):
    pass
