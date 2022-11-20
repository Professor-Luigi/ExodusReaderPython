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

    # The rf period is the timescale that things change on.
    # These times were calcluated to span across one rf period.
    sampled_times = np.array([7.3747e-5,
                              7.3766e-5,
                              7.3784e-5,
                              7.3803e-5,
                              7.3820e-5])
    # Get the sampled time indices.
    sampled_time_indices = np.ones(len(sampled_times), dtype=int)
    for i, time_value in enumerate(sampled_times):
        # The two slices are to get into the tuple that np.where returns and to
        # get the actual index out of the array.
        sampled_time_indices[i] = int(np.where(np.isclose(time,
                                                          time_value,
                                                          rtol=0,
                                                          atol=1e-10))[0][0])

    linestyles = ['solid',
                  'dotted',
                  'dashed',
                  'dashdot',
                  (0,(1,10))
                  ]
    RF_PERIOD = 1/13.56e6 # s
    time_ratio = [(sampled_time - sampled_times[0])/RF_PERIOD for sampled_time in sampled_times]

    # Plot the log densities
    fig, ax = plt.subplots()
    for i, sampled_time_index in enumerate(sampled_time_indices):
        ax.plot(x, node_variables_dict['em'][sampled_time_index,:],
                ls=linestyles[i], label=f'{time_ratio[i]:.3f}')
    ax.legend(title='Fraction of RF Period')
    ax.set_ylabel('Log Density')
    ax.set_xlabel('x (m)')
    ax.set_title('e$^-$ log density at various times')
    fig.savefig(f'example1D_RF_plasma_time_log.png')

    # Plot the densities
    fig, ax = plt.subplots()
    for i, sampled_time_index in enumerate(sampled_time_indices):
        ax.plot(elem_variables_dict['x'][sampled_time_index,:],
                elem_variables_dict['em_density'][sampled_time_index,:],
                ls=linestyles[i], label=f'{time_ratio[i]:.3f}')
    ax.legend(title='Fraction of RF Period')
    ax.set_ylabel('Density (m$^{-3}$)')
    ax.set_xlabel('x (m)')
    ax.set_title('e$^-$ density at various times')
    fig.savefig(f'example1D_RF_plasma_time_lin.png')

if __name__ == '__main__':
    main()
