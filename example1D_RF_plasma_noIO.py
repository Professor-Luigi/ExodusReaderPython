import netCDF4 as net
import matplotlib.pyplot as plt

import ExodusReader as er 


'''
Show a simpler way to read exodus files.
This file achieves the same thing as example1D_RF_plasma.py.

The file used in this example comes from:
https://github.com/shannon-lab/zapdos in tutorial/tutorial04
'''
def main():
    # Read in the exodus data
    path = 'test_files/RF_Plasma_WithOut_Metastables_IC.e'

    # ROUGHLY: node variables are defined in the Variables section and 
    # element variables are defined in the AuxVariables section.
    node_variables_dict, elem_variables_dict = er.read_exodus(path)

    # Plot some data
    fig, ax = plt.subplots(2, sharex=True)
    plot_node_vars = ['Ar', 'Ar+', 'em']
    plot_elem_vars = ['Ar+_density', 'em_density']
    for var in plot_node_vars:
        ax[0].plot(node_variables_dict['x_node'],
                   node_variables_dict[var],
                   label=var)
    ax[0].set_ylabel('Log Density')    
    ax[0].legend()

    for var in plot_elem_vars:
        ax[1].plot(elem_variables_dict['position'],
                   elem_variables_dict[var],
                   label=var)
    ax[1].set_ylabel('Density')
    ax[1].set_xlabel('X')
    ax[1].legend()
    ax[1].set_yscale('log')
    fig.savefig('example1D_RF_plasma_noIO.png')

if __name__ == '__main__':
    main()
