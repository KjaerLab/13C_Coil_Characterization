#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 10:56:50 2024

@author: Emil Christensen, emil.christensen@sund.ku.dk
"""

#Import packages
import numpy as np
import matplotlib.pyplot as plt
import pydicom

def GRE_dcm_analysis(path, plot, Npts,coil,dB):
    #Inputs: Dicompath to a scan. plot, 0 = no plot 1 = plot, Npts = amount of 
    #datapoints to use for signal, dB = 1 - you will get your calculations of SNR in dB 
   
    coil = coil
    data = pydicom.dcmread(path)
    
    #Extract avereges and image from dicom file
    averages = data.NumberOfAverages
    img = data.pixel_array
    
    #flatten signal and get the noise
    flatSignal = img.flatten()
    sortSignal = sorted(flatSignal)
    noise = sortSignal[0:1000]
    noiseSD = np.std(noise)
    
    #Calculate and SNR image
    SNRimg = img/noiseSD
    
    #dB or no dB calculation
    if dB == 1:
        print('You choose the calculate SNR in dB')
        SNR = 10*np.log10(SNRimg)
        
        flatSNRdB = SNR.flatten()
        sorted_part_indices = np.argsort(flatSNRdB)  # Get indices that would sort the array
               
        top_part_indices = sorted_part_indices[-Npts:]  # Indices of the top N values
               
        top_SNR_values = flatSNRdB[top_part_indices]
               
        SNR_mean = np.mean(top_SNR_values)
               
        top_part_coords = np.unravel_index(top_part_indices, SNR.shape)
    else:
            
        sorted_part_indices = np.argsort(flatSignal)  # Get indices that would sort the array
               
        top_part_indices = sorted_part_indices[-Npts:]  # Indices of the top N values
               
        top_SNR_values = flatSignal[top_part_indices]
               
        SNR_mean = np.mean(top_SNR_values)
               
        top_part_coords = np.unravel_index(top_part_indices, SNR.shape)
     
    #Add an SNR plot to the output    
    if plot == 1:
        print(f'You choose to make a plot with the signal defined as the {Npts} highest valued points')
       # Step 5: Plot the original matrix and highlight top values
        plt.figure(figsize=(8, 8))
        plt.imshow(SNR, vmin=0)  # Display the original image (matrix)
        plt.colorbar()
       # Overlay the locations of the highest values
        plt.scatter(top_part_coords[1], top_part_coords[0], color='red', s=10, label=f'Top {Npts} values')
       
       # Add a legend and show the plot
        plt.legend()
        plt.title(f'SNR with {averages} averages and coil {coil}. Mean SNR {SNR_mean}')
        plt.show()
    else:
        pass
    
    return (SNR, SNR_mean)