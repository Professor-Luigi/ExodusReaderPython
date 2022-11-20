import matplotlib.pyplot as plt
import netCDF4 as net
import numpy as np

import ExodusReader as er 


'''
Show how to read an exodus file (with time dependence) using this package and
netCDF4. This way gives the option to look into the exodus file further.

The file used in this example comes from running the .i file in:
https://github.com/shannon-lab/zapdos in tutorial/tutorial04
'''
def main():
    # Read in the exodus data
    path = 'test_files/RF_Plasma_WithOut_Metastables-1Torr_out.e'

    # Similar to open(path, 'r')
    with net.Dataset(path) as nc:
        # See all the variables in the exodus file
        print('Available Variables:')
        print()
        for key in nc.variables.keys():
            print(key)

        # A dictionary where the keys are the variable names input into the *.i
        # file and the values are the values of the variables.
        # Node variables exist on the nodes and elem variables exist in between.
        # ROUGHLY: node variables are defined in the Variables section and 
        # element variables are defined in the AuxVariables section.
        node_variables_dict = er.transcribe_variables(nc.variables, kind='node')
        elem_variables_dict = er.transcribe_variables(nc.variables, kind='elem')

        # Time is relatively easier to get to
        time = nc.variables['time_whole'][:]
        dt = time[1] - time[0] 

        # This is the positions for the node variables. To get the positions
        # of the element variables, use 'position' key in elem_variables_dict.
        # This gives a 1D array of the x coordinates. There is no time
        # consideration with this.
        x = nc.variables['coordx'][:]

        # This introduces some challenge into using this interface for getting
        # data from these files. It is recommended to check what keys are in
        # the nc.variables and the node/element variables before any analysis
        # is done.

    # Print the keys and the shapes of each variable
    print('\nNode Variables:\n')
    for key, value in node_variables_dict.items():
        print(key, value.shape)

    print('\nElement Variables:\n')
    for key, value in elem_variables_dict.items():
        print(key, value.shape)

    # Make plots over time

    fig, axes = plt.subplots(nrows=2, ncols=3,
                             sharex=True,
                             figsize=(12,7),
                             gridspec_kw=dict(wspace=0.25))
    fig.suptitle('e$^-$ Log Density at various times')

    # Pick 6 times to plot (there are too many to plot them all)
    sampled_time_indices = np.linspace(1, len(time)-1, 6).astype(int)

    # Plot each subplot
    for ax, sampled_time_index in zip(axes.flatten(), sampled_time_indices):
        ax.set_ylabel('Density')
        ax.set_xlabel('X')
        ax.set_title(f'{time[sampled_time_index]:.2E} s')

        # The time of the data is the first index and the position is the second.
        ax.plot(x,node_variables_dict['em'][sampled_time_index,:])

    fig.savefig(f'example1D_RF_plasma_time_6_plots_log.png')
        
    fig, axes = plt.subplots(nrows=2, ncols=3,
                             sharex=True, sharey=True,
                             figsize=(12,7))
    fig.suptitle('e$^-$ Density at various times')

    # Plot each subplot
    for ax, sampled_time_index in zip(axes.flatten(), sampled_time_indices):
        ax.set_ylabel('Density m$^{-3}$')
        ax.set_xlabel('X')
        ax.set_title(f'{time[sampled_time_index]:.2E} s')

        # The time of the data is the first index and the position is the second.
        # This gives the x coords at every timestep. However, since the x
        # coordinate does not change from timestep to timestep, this is not
        # the most efficient way to to this.
        ax.plot(elem_variables_dict['x'][sampled_time_index,:],
                elem_variables_dict['em_density'][sampled_time_index,:])

    fig.savefig(f'example1D_RF_plasma_time_6_plots_lin.png')
#    fig, ax = plt.subplots(2, sharex=True)
#    plot_node_vars = ['Ar', 'Ar+', 'em']
#    plot_elem_vars = ['Ar+_density', 'em_density']
#    for var in plot_node_vars:
#        ax[0].plot(node_variables_dict['x_node'],
#                   node_variables_dict[var],
#                   label=var)
#    ax[0].set_ylabel('Log Density')    
#    ax[0].legend()
#
#    for var in plot_elem_vars:
#        ax[1].plot(elem_variables_dict['position'],
#                   elem_variables_dict[var],
#                   label=var)
#    ax[1].set_ylabel('Density')
#    ax[1].set_xlabel('X')
#    ax[1].legend()
#    ax[1].set_yscale('log')
#    fig.savefig('example1D_RF_plasma.png')

if __name__ == '__main__':
    main()
