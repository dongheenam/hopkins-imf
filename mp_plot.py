# dependencies
import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import mpltools
from constants import G

def plot_imf(filename, ax, norm_x=1, norm_y=1, binned=True, **kwargs) :
    # read the IMF
    h5 = h5py.File(filename, 'r')

    IMF = np.array(h5['IMF'])
    M = np.array(h5['M'])

    # truncate the distribution
    if binned :
        bin_width = 4
        IMF_binned = np.zeros(IMF.size//bin_width)
        for i in range(IMF_binned.size) :
            IMF_binned[i] = np.average(IMF[i*bin_width:(i+1)*bin_width])
        M_binned = M[bin_width//2::bin_width]
    else :
        IMF_binned = IMF
        M_binned = M

    # remove zero entries
    IMF_nonzero = IMF_binned[IMF_binned!=0]
    M_nonzero = M_binned[IMF_binned!=0]

    # normalise
    x = M_nonzero/norm_x
    y = M_nonzero**2*IMF_nonzero/norm_y

    # plot the IMF
    ax.plot(x, y, **kwargs)

if __name__ == "__main__" :
    # initialise mpl
    mpltools.mpl_init()
    fig = plt.figure()
    ax = fig.add_subplot()

    # set up the axes
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(left=1e-8, right=1e2)
    ax.set_ylim(bottom=1e-3, top=1)

    ax.set_xlabel(r"$M[\rho_0 h^3]$")
    ax.set_ylabel(r"$M \dfrac{dn}{d\log M}[\rho_0]$")

    # Salpeter slope
    #x_Sal = np.linspace(1e-4,1e0,10)
    #ax.plot(x_Sal, x_Sal**(-1.35), color='orange', linewidth=3, ls='--', label='Salpeter')

    # plot the IMFs
    # M_gas = 1.171e39, rho_0 = 3.985e-23
    #plot_imf("M10p2B0.0n1000_dir.hdf5", ax, norm_x=1.171e39, norm_y=3.985e-23/2.4, binned=False, color='black', label=r'$p=2, \mathcal{M}_h=10, b=1 \quad (\times 2)$')
    plot_imf("M5p2B0.0n1000_dir.hdf5", ax, norm_x=9.370187E+33, norm_y=3.985e-23/2.4, binned=False, color='dodgerblue', label=r'$p=2, \mathcal{M}_h=5, b=1 \quad (\times 2)$')
    #plot_imf("M5p2B0.0n5000_dir.hdf5", ax, norm_x=9.370187E+33, norm_y=3.985e-23/2.4, binned=False, color='aquamarine', label=r'$p=2, \mathcal{M}_h=5, b=0.4 \quad (\times 2)$')
    #plot_imf("M5p1.001B0.0n5000_dir.hdf5", ax, norm_x=9.370187E+33, norm_y=3.985e-23/2.4, binned=False, color='aquamarine', label=r'$p=1, \mathcal{M}_h=5 \quad (\times 2)$')

    # save the plot
    plt.legend(prop={'size':12}, loc='upper left')
    plt.savefig("IMF.pdf")
