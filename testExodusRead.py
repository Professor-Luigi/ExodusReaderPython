import netCDF4 as net
import numpy as np
import matplotlib.pyplot as plt


def read_name_var(name_list):
    '''
    for name_nod_var and name_elem_var
    '''
    names = []
    for name in name_list:
        current_name = ''
        for char in name.data: 
            decoded = char.decode('UTF-8')
            if decoded == '':
                break
            current_name += decoded
        names.append(current_name)
    return names

def build_dict(variables, exodus_names):
    '''
    variables    | The variables that were read in "netCDF4.Dataset(path).variables.
    exodus_names | List of tuples where the first is the exodus name for the variable and the second is the readable name.
    var_dict     | Use if there is a preexisting dictionary of variables made with this function.
    '''
    var_dict = {}
    for exodus_name, readable_name in exodus_names:
        # Store the data in variables to check their shape
        var = variables[exodus_name][:]
        
        # Check that the arrays don't have the following shape: [[1,1,1,1,1,1]].
        # Make sure the array isn't already 1d to do this change. Otherwise IndexError.
        if len(var.shape) != 1:
            # Check if this is a column vector.
            if var.shape[0] == 1 and var.shape[1] >= 1:
                # Convert to a 1D row vector.
                var = var[0]
        var_dict[readable_name] = var

    return var_dict

def make_var_dict(variables, kind=''):
    '''
    variables      | The variables that were read in "netCDF4.Dataset(path).variables.
    readable_names | The human readable names that were used in the *.i file.
    kind           | The kind of variables to build the dictionary for: node or elem.

    Create a dictionary of the names and values of the variables of interest.
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
    readable_names = read_name_var(variables[variable_key][:])

    # Make a list of the names of the variables of interest with their corresponding variable in the exodus file.
    # THIS ASSUMES A GIVEN NAMING CONVENTION IN THE EXODUS FILES WHICH MAY NEED TO BE ALTERED.
    names_exodus = [(f'{initial_f_string}{i+1}{final_f_string}', name) for i, name in enumerate(readable_names)]

    # Build the variable dictionary.
    # Keys are the readable names, values are the values.
    var_dict = build_dict(variables, names_exodus)
    return var_dict

def main():
    # Read in the exodus data
    path = 'tutorial04-PressureVsTe/RF_Plasma_WithOut_Metastables_IC.e'
    nc = net.Dataset(path)

    # Get readable names for the variables of interest
    node_var_names = read_name_var(nc.variables['name_nod_var'][:])
    elem_var_names = read_name_var(nc.variables['name_elem_var'][:])

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
        ax[0].plot(node_variables_dict['x_node'], node_variables_dict[var], label=var)
    ax[0].set_ylabel('Log Density')    
    ax[0].legend()

    for var in plot_elem_vars:
        ax[1].plot(elem_variables_dict['position'], elem_variables_dict[var], label=var)
    ax[1].set_ylabel('Density')
    ax[1].set_xlabel('X')
    ax[1].legend()
    ax[1].set_yscale('log')
    fig.savefig('test.png')
    nc.close()

if __name__ == '__main__':
    main()
