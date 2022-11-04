import netCDF4 as net
import matplotlib.pyplot as plt

import ExodusReader as er 


def main():
    # Read in the exodus data
    path = 'test_files/RF_Plasma_WithOut_Metastables_IC.e'
    nc = net.Dataset(path)

    # See all the variables in the exodus file
    print(nc.variables.keys())

    # Get the positions
    # These also may exist in the following variables
    X = nc.variables['coordx']

    # A dictionary where the keys are the variable names input into the *.i
    # file and the values are the values of the variables.
    node_variables_dict = er.transcribe_variables(nc.variables, kind='node')
    elem_variables_dict = er.transcribe_variables(nc.variables, kind='elem')

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
