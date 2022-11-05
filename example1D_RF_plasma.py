import netCDF4 as net
import matplotlib.pyplot as plt

import ExodusReader as er 


'''
Show how to read an exodus file using this package and netCDF4.
This way gives the option to look into the exodus file further.
This file achieves the same thing as example1D_RF_plasma_noIO.py.


The file used in this example comes from:
https://github.com/shannon-lab/zapdos in tutorial/tutorial04
'''
def main():
    # Read in the exodus data
    path = 'test_files/RF_Plasma_WithOut_Metastables_IC.e'

    # Similar to open(path, 'r')
    with net.Dataset(path) as nc:
        # See all the variables in the exodus file
        print('Available Variables:')
        print()
        for key in nc.variables.keys():
            print(key)

        # Get the positions
        # These also may exist in the following variables
        X = nc.variables['coordx']

        # A dictionary where the keys are the variable names input into the *.i
        # file and the values are the values of the variables.
        # Node variables exist on the nodes and elem variables exist in between.
        # ROUGHLY: node variables are defined in the Variables section and 
        # element variables are defined in the AuxVariables section.
        node_variables_dict = er.transcribe_variables(nc.variables, kind='node')
        elem_variables_dict = er.transcribe_variables(nc.variables, kind='elem')

    # Print the keys and the shapes of each variable
    print('\nNode Variables:\n')
    for key, value in node_variables_dict.items():
        print(key, value.shape)

    print('\nElement Variables:\n')
    for key, value in elem_variables_dict.items():
        print(key, value.shape)

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
    fig.savefig('example1D_RF_plasma.png')

if __name__ == '__main__':
    main()
