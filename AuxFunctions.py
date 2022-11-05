import numpy as np


def read_name_var(name_list):
    '''
    This function reads in a list of names from the exodus file and converts
    them to a readable format instead of a numpy bytes array.

    name_list | numpy.array | An 2D array where each element is an array that
                            | contains the name of a variable as bytes.
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
    This function constructs the dictionary that contains the data and the
    readable names in variables. The keys are the names and the values are
    the values.

    variables    | netCDF4.variable | The variables that were read in
                                    | "netCDF4.Dataset(path).variables.
    exodus_names | list             | List of tuples where the first is the
                                    | exodus name for the variable and the
                                    | second is the readable name.
    '''
    var_dict = {}
    for exodus_name, readable_name in exodus_names:
        # Store the data in variables to check their shape
        var = variables[exodus_name][:]
        
        # Check that the arrays don't have the following shape: [[1,1,1,1,1,1]].
        # Make sure the array isn't already 1d to do this change. Otherwise IndexError.
        # This really is only necessary for 1D simulations.
        if len(var.shape) != 1:
            # Check if this is a column vector.
            if var.shape[0] == 1 and var.shape[1] >= 1:
                # Convert to a 1D row vector.
                var = var[0]
        var_dict[readable_name] = var

    return var_dict
