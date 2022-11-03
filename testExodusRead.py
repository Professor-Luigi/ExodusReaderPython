import netCDF4 as net
import numpy as np
import matplotlib.pyplot as plt

import AuxFunctions as af


def make_var_dict(variables, kind=''):
    '''
    Create a dictionary of the names and values of the variables of interest.
    Considers a given kind of variables.

    variables      | netCDF4.variable | The variables that were read in
                                      | "netCDF4.Dataset(path).variables.
    readable_names | list             | The human readable names that were
                                      | used in the *.i file.
    kind           | str              | The kind of variables to build the
                                      | dictionary for: node or elem.
    '''
    # Specify the values for the desired kind of variables.
    if kind == 'node':
        variable_key = 'name_nod_var'
        initial_f_string = 'vals_nod_var'
        final_f_string = ''
    elif kind == 'elem':
        variable_key = 'name_elem_var'
        initial_f_string = 'vals_elem_var'
        final_f_string = 'eb1'

    # Get readable names for the variables of interest
    readable_names = af.read_name_var(variables[variable_key][:])

    # Make a list of the names of the variables of interest with their
    # corresponding variable in the exodus file.
    # THIS ASSUMES A GIVEN NAMING CONVENTION IN THE EXODUS FILES WHICH MAY
    # NEED TO BE ALTERED.
    names_exodues = []
    for i, name in enumerate(readable_names):
        names_exodus.append(f'{initial_f_string}{i+1}{final_f_string}', name)

    # Build the variable dictionary.
    # Keys are the readable names, values are the values.
    var_dict = build_dict(variables, names_exodus)
    return var_dict

def main():
    # Read in the exodus data
    path = 'test_files/RF_Plasma_WithOut_Metastables_IC.e'
    nc = net.Dataset(path)

    # Get the positions
    # These also may exist in the following variables
    X = nc.variables['coordx']

    # A dictionary where the keys are the variable names input into the *.i
    # file and the values are the values of the variables.
    node_variables_dict = make_var_dict(nc.variables, kind='node')
    elem_variables_dict = make_var_dict(nc.variables, kind='elem')

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
    fig.savefig('test.png')
    nc.close()

if __name__ == '__main__':
    main()
