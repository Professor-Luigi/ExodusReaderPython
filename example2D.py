import matplotlib.pyplot as plt
import netCDF4 as net
import numpy as np

import ExodusReader as er


'''
Show how to read in a 2D exodus file with netCDF4.

The file used in this example comes from running:
https://github.com/lcpp-org/zapdos/tree/devel/problems/poisson_transient.i
'''
def main():
    # Read in the exodus data
    path = 'test_files/poisson_uniform_out.e'

    with net.Dataset(path) as nc:
        # See all the variables in the exodus file
        print('Available Variables:')
        print()
        for key in nc.variables.keys():
            print(key, nc.variables[key][:].shape)
            print(nc.variables[key][:])

        node_variables_dict = er.transcribe_variables(nc.variables, kind='node')
        elem_variables_dict = er.transcribe_variables(nc.variables, kind='elem')
        time = nc.variables['time_whole'][:]
        x = nc.variables['coordx'][:]
        y = nc.variables['coordy'][:]
        print(nc.variables['node_ns1'][:])
        print(nc.variables['node_ns2'][:])
        print(nc.variables['node_ns3'][:])
        print(nc.variables['node_ns4'][:])
        print(nc.variables['connect1'][:].shape)


    # Print the keys and the shapes of each variable
    print('\nNode Variables:\n')
    for key, value in node_variables_dict.items():
        print(key, value.shape)

    print('\nElement Variables:\n')
    for key, value in elem_variables_dict.items():
        print(key, value.shape)

    umin = node_variables_dict['u'].min()
    umax = node_variables_dict['u'].max()
    fig, ax = plt.subplots(figsize=(8,8))
    for x_pt, y_pt, u in zip(x,y,node_variables_dict['u']):
        ax.scatter(x_pt,y_pt, marker='s', s=400, c=[u], vmin=umin, vmax=umax)
    ax.axis('equal')
    fig.savefig('example2D.png')

if __name__ == '__main__':
    main()
