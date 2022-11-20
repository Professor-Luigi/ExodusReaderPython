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

    # Make plots over time

    fig, axes = plt.subplots(nrows=2, ncols=3,
                             sharex=True,
                             figsize=(12,7),
                             gridspec_kw=dict(wspace=0.25))
    fig.suptitle('e$^-$ Log Density at various times')

    # Pick 6 times to plot (there are too many to plot them all)
    sampled_time_indices = np.linspace(1, len(node_variables_dict['time'])-1, 6).astype(int)

    # Get the x array for the node variables.
    # This gives a 1D array of the x coordinates. There is no time
    # consideration with this.
    x = node_variables_dict['coordx'][:]

    # Plot each subplot
    for ax, sampled_time_index in zip(axes.flatten(), sampled_time_indices):
        ax.set_ylabel('Density')
        ax.set_xlabel('X')
        ax.set_title(f'{node_variables_dict["time"][sampled_time_index]:.2E} s')

        # The time of the data is the first index and the position is the second.
        ax.plot(x,node_variables_dict['em'][sampled_time_index,:])

    fig.savefig(f'example1D_RF_plasma_time_6_plots_log_noIO.png')
        
    fig, axes = plt.subplots(nrows=2, ncols=3,
                             sharex=True, sharey=True,
                             figsize=(12,7))
    fig.suptitle('e$^-$ Density at various times')

    # Plot each subplot
    for ax, sampled_time_index in zip(axes.flatten(), sampled_time_indices):
        ax.set_ylabel('Density m$^{-3}$')
        ax.set_xlabel('X')
        ax.set_title(f'{node_variables_dict["time"][sampled_time_index]:.2E} s')

        # The time of the data is the first index and the position is the second.
        # This gives the x coords at every timestep. However, since the x
        # coordinate does not change from timestep to timestep, this is not
        # the most efficient way to to this.
        ax.plot(elem_variables_dict['x'][sampled_time_index,:],
                elem_variables_dict['em_density'][sampled_time_index,:])

    fig.savefig(f'example1D_RF_plasma_time_6_plots_lin_noIO.png')

if __name__ == '__main__':
    main()
