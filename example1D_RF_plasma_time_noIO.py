import matplotlib.pyplot as plt
import netCDF4 as net
import numpy as np

import ExodusReader as er 


'''
Show how to read an exodus file (with time dependence) using this package and
netCDF4. This way gives the option to look into the exodus file further.
This is similar to the example1DRF_plasma_time.py file.

The file used in this example comes from running the .i file in:
https://github.com/shannon-lab/zapdos in tutorial/tutorial04
'''
def main():
    # Read in the exodus data
    path = 'test_files/RF_Plasma_WithOut_Metastables-1Torr_out.e'

    node_variables_dict, elem_variables_dict = er.read_exodus(path)

    # Print the keys and the shapes of each variable
    print('\nNode Variables:\n')
    for key, value in node_variables_dict.items():
        print(key, value.shape)

    print('\nElement Variables:\n')
    for key, value in elem_variables_dict.items():
        print(key, value.shape)

    time = node_variables_dict['time']
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
        ax.plot(node_variables_dict['coordx'][:],
                node_variables_dict['em'][sampled_time_index,:],
                ls=linestyles[i], label=f'{time_ratio[i]:.3f}')
    ax.legend(title='Fraction of RF Period')
    ax.set_ylabel('Log Density')
    ax.set_xlabel('x (m)')
    ax.set_title('e$^-$ log density at various times')
    fig.savefig(f'example1D_RF_plasma_time_log_noIO.png')

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
    fig.savefig(f'example1D_RF_plasma_time_lin_noIO.png')

if __name__ == '__main__':
    main()
