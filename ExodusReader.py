import netCDF4 as net

import AuxFunctions as af


def transcribe_variables(variables, kind=''):
    '''
    Create a dictionary of the names and values of the variables of interest.
    Considers a given kind of variables. Requires use of fileIO with netCDF4. 

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
    names_exodus = []
    for i, name in enumerate(readable_names):
        names_exodus.append((f'{initial_f_string}{i+1}{final_f_string}', name))

    # Build the variable dictionary.
    # Keys are the readable names, values are the values.
    var_dict = af.build_dict(variables, names_exodus)
    return var_dict

def read_exodus(path_to_file):
    '''
    Reads the exodus file and outputs a dictionary with keys being the variable
    names and the values as the values of the variable. Does the IO inside so
    the user doesn't have to think about it.

    path_to_file | str | The path to the exodus file.
    '''

    with net.Dataset(path_to_file) as nc:
        # A dictionary where the keys are the variable names input into the *.i
        # file and the values are the values of the variables.
        node_variables_dict = transcribe_variables(nc.variables, kind='node')
        elem_variables_dict = transcribe_variables(nc.variables, kind='elem')

        # Add the time array to both dictionaries
        node_variables_dict['time'] = nc.variables['time_whole'][:]
        elem_variables_dict['time'] = nc.variables['time_whole'][:]

        # Add the position arrays to the node variables.
        # Sometimes they are not added by default. They are 1D arrays.
        node_variables_dict['coordx'] = nc.variables['coordx'][:]
        node_variables_dict['coordy'] = nc.variables['coordy'][:]
        node_variables_dict['coordz'] = nc.variables['coordz'][:]

    return node_variables_dict, elem_variables_dict
