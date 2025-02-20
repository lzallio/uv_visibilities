#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 16:18:52 2025

@author: lzallio
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def read_txt_file(file_path):
    """
    Reads .txt and returns df
    """
    try:
        #Skip 3 lines of comments
        data = pd.read_csv(file_path, skiprows=3, delim_whitespace=True, header=None)
        
        #5 cols
        if data.shape[1] != 5:
            raise ValueError("File has not exactly 5 columns.")
        
        #Names
        data.columns = ['u[m]', 'v[m]', 'Re(V)[Jy]', 'Im(V)[Jy]', 'weight']
        
        return data
    except Exception as e:
        print(f"Error while reading the file: {e}")
        return None
    


def rebin_and_plot(df, u_col='u[m]', v_col='v[m]', 
                   ReV_col='Re(V)[Jy]', weight_col='weight', n_bins=100, 
                   num=100, path_to_save='./'):
    """
    Re-bin the data in u, v, and compute the weighted average <Re(V)> in each bin.
    """
    
    # Extract the data from the DataFrame
    u = df[u_col].values
    v = df[v_col].values
    ReV = df[ReV_col].values
    weight = df[weight_col].values

    # Define the bin edges for u and v
    u_bins = np.linspace(u.min(), u.max(), n_bins)
    v_bins = np.linspace(v.min(), v.max(), n_bins)

    #Compute weighted sum of wV
    hist_wReV, u_edges, v_edges = np.histogram2d(u, v, 
                                                 bins=[u_bins, v_bins], 
                                                 weights=weight * ReV)

    #Compute sum of w
    hist_weight, _, _ = np.histogram2d(u, v, bins=[u_bins, v_bins], 
                                       weights=weight)

    #Compute weighted average <Re(V)> in each bin
    weighted_avg_ReV = np.divide(hist_wReV, hist_weight, 
                                 where=hist_weight != 0)

    weighted_avg_ReV = hist_wReV / hist_weight

    #Grid (u, v values for each bin center)
    u_centers = (u_edges[:-1] + u_edges[1:]) / 2
    v_centers = (v_edges[:-1] + v_edges[1:]) / 2

    #2D plot + cb
    plt.figure(figsize=(8, 6))
    plt.imshow(weighted_avg_ReV.T, extent=[u_centers.min(), u_centers.max(), 
                                           v_centers.min(), v_centers.max()],
               origin='lower', aspect='auto', cmap='seismic', 
               interpolation='nearest', 
               vmin=-5, vmax=5)

    #Ticks
    cbar = plt.colorbar(label=r'<Re(V)> [Jy]')
    cbar.ax.tick_params(labelsize=15)
    
    plt.xlabel(u_col, fontsize=15)
    plt.ylabel(v_col, fontsize=15)
    plt.title(r'Channel '+str(num), fontsize=20)
    
    plt.tick_params(axis='both', labelsize=15,direction='in', which='both')
    plt.tight_layout()

    #Show
    plt.savefig(path_to_save, dpi=100, bbox_inches='tight')
    plt.show()
    


def rebin_and_plot_3d(df, u_col='u[m]', v_col='v[m]', 
                      ReV_col='Re(V)[Jy]', weight_col='weight', n_bins=100, 
                      num=100, path_to_save='./'):
    """
    Re-bin the data in u, v, and compute the weighted average <Re(V)> in each bin.
    Then plot the data in a 3D plot with u, v, and Re(V) on the z-axis.
    """
    
    # Extract the data from the DataFrame
    u = df[u_col].values
    v = df[v_col].values
    ReV = df[ReV_col].values
    weight = df[weight_col].values

    # Define the bin edges for u and v
    u_bins = np.linspace(u.min(), u.max(), n_bins)
    v_bins = np.linspace(v.min(), v.max(), n_bins)

    # Compute weighted sum of ReV
    hist_wReV, u_edges, v_edges = np.histogram2d(u, v, 
                                                 bins=[u_bins, v_bins], 
                                                 weights=weight * ReV)

    # Compute sum of weights
    hist_weight, _, _ = np.histogram2d(u, v, bins=[u_bins, v_bins], 
                                       weights=weight)

    # Compute weighted average <Re(V)> in each bin
    weighted_avg_ReV = np.divide(hist_wReV, hist_weight, 
                                 where=hist_weight != 0)
    weighted_avg_ReV = hist_wReV / hist_weight

    # Grid (u, v values for each bin center)
    u_centers = (u_edges[:-1] + u_edges[1:]) / 2
    v_centers = (v_edges[:-1] + v_edges[1:]) / 2

    # Create a 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create meshgrid for u and v centers
    U, V = np.meshgrid(u_centers, v_centers)
    
    # Flatten the meshgrid to plot the points
    U_flat = U.flatten()
    V_flat = V.flatten()
    ReV_flat = weighted_avg_ReV.flatten()

    # Plotting the 3D scatter plot
    scatter = ax.scatter(U_flat, V_flat, ReV_flat, c=ReV_flat, cmap='seismic', 
               marker='o')
    ax.set_zlim(-5, 5)
    
    scatter.set_clim(vmin=-5, vmax=5)
    
    # Labels and title
    ax.set_xlabel(u_col, fontsize=15)
    ax.set_ylabel(v_col, fontsize=15)
    ax.set_zlabel(r'<Re(V)> [Jy]', fontsize=15)
    ax.set_title(f'Channel {num}', fontsize=20)

    # Set tick parameters
    ax.tick_params(axis='both', labelsize=12)

    # Show color bar
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label(r'<Re(V)> [Jy]', fontsize=15)

    # Display the plot
    plt.tight_layout()
    plt.show()
    #fig.savefig(path_to_save, dpi=100, bbox_inches='tight')


path = '/your_path/'
to_keep = ['u[m]', 'v[m]', 'Re(V)[Jy]', 'weight'] #don't change this...


def run(path, name='msfile_name', n_chan=960, 
        n_bins=150, to_keep=['u[m]', 'v[m]', 'Re(V)[Jy]', 'weight']):
    for i in range(0, n_chan):
        
        name = name
        file = name+'_'+str(i)+'.txt'
        data_path = path+file
        data = read_txt_file(data_path)
        data_fin = data[to_keep]
        
        
        rebin_and_plot(data_fin, n_bins=n_bins, num=i, 
                       path_to_save=path+name+'_2D_'+str(i)+'.png')
        #rebin_and_plot_3d(data_fin, n_bins=50, 
        #                  num=i, path_to_save=path+name+'_3D_'+str(i)+'.png')







