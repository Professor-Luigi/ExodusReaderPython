import AuxFunctions as af


def transcribe_variables(variables, kind=''):
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
    names_exodus = []
    for i, name in enumerate(readable_names):
        names_exodus.append((f'{initial_f_string}{i+1}{final_f_string}', name))

    # Build the variable dictionary.
    # Keys are the readable names, values are the values.
    var_dict = af.build_dict(variables, names_exodus)
    return var_dict

