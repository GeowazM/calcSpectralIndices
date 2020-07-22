#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Description:
        This script uses a band set calculate the NDVI, the NDWI & the BuiltUp Index.
        Afterwards the scripts eyport each single band plus the calculated indices.
        Last the script merges the bands in a single band set (raster stack).
        
        Input:      wholeFilename.tif
        Output:     Sindle bands & indices as tif files &
                    Virtual & usual raster band set
    
    Structure:
                0. Functions
                    a) Export single bands                                     exportSingleBand
                    b) NDVI calculator                                         calcNDVI
                    c) BuiltUp Index calculator                                calcBuiltUp
                    d) NDWI Index Calculator                                   calcNDWI
                
                I.    Import filename    
                II.   Label postfix of the indices
                III.  Check if file exist
                IV.   Calculate NDVI
                V.    Calculate NDWI
                VI.   Calculate Built Up Index
                VII.  Label filenames for single bands & indices
                VIII. Get one band and write it
                IX.   Label virtual & final raster
                X.    Build virtual raster
                XI.   Translate virtual raster to raster
    
Author: Mario Blersch
Date: February 2020
"""

# a) Function to Export single bands
def exportSingleBand(image_file, band_number, output_file):
    # Create the file
    with rasterio.open(image_file) as src:
        band = src.read(band_number)
    # Set spatial characteristics of the output object to mirror the input
    kwargs = src.meta
    kwargs.update(
        dtype=rasterio.float32,
        count = 1)
    with rasterio.open(output_file, 'w', **kwargs) as dst:
            dst.write_band(1, band.astype(rasterio.float32))
    return 'exportSingleBand done'



# b) NDVI calculator
def calcNDVI(image_file, output_file):
    # Formula source: https://wiki.orfeo-toolbox.org/index.php/Radiometric_Indices
    # Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
    with rasterio.open(image_file) as src:
        band_red = src.read(3)
    with rasterio.open(image_file) as src:
        band_nir = src.read(4)
    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')
    # Calculate NDVI
    ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)
    # Set spatial characteristics of the output object to mirror the input
    kwargs = src.meta
    kwargs.update(
        dtype=rasterio.float32,
        count = 1)
    # Create the file
    with rasterio.open(output_file, 'w', **kwargs) as dst:
            dst.write_band(1, ndvi.astype(rasterio.float32))
    return ndvi
      
# c) BuiltUp Index calculator
def calcBuiltUp(image_file, output_file):
    # Source: https://wiki.orfeo-toolbox.org/index.php/ISU
    # Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
    with rasterio.open(image_file) as src:
        band_red = src.read(3)
    with rasterio.open(image_file) as src:
        band_nir = src.read(4)
    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')
    # Calculate NDVI
    builtup = 100 - 25 * band_nir.astype(float) / band_red.astype(float)
    # Set spatial characteristics of the output object to mirror the input
    kwargs = src.meta
    kwargs.update(
        dtype=rasterio.float32,
        count = 1)
    # Create the file
    with rasterio.open(output_file, 'w', **kwargs) as dst:
            dst.write_band(1, builtup.astype(rasterio.float32))
    return builtup
      

# d) NDWI Index Calculator
def calcNDWI(image_file, output_file):
    # Source: #https://wiki.orfeo-toolbox.org/index.php/NDWI_(Mc_Feeters,_1996)
    # Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
    with rasterio.open(image_file) as src:
        band_green = src.read(2)
    with rasterio.open(image_file) as src:
        band_nir = src.read(4)
    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')
    # Calculate NDVI
    ndwi = (band_green.astype(float) - band_nir.astype(float)) / (band_green.astype(float) + band_nir.astype(float))
    # Set spatial characteristics of the output object to mirror the input
    kwargs = src.meta
    kwargs.update(
        dtype=rasterio.float32,
        count = 1)
    # Create the file
    with rasterio.open(output_file, 'w', **kwargs) as dst:
            dst.write_band(1, ndwi.astype(rasterio.float32))
    return ndwi
      


  
if __name__ == "__main__":
    import rasterio
    import numpy
    import os.path
    import os

    # I. Import filename
    img = '/home/geowazm/Documents/05_WS-201920/Master_Thesis/DATA/VHR_images/Ikonos/121-130/po_2661437_0000000/po_2661437_bgrn_0000000_2000_classified/po_2661437_bgrn_0000000_2000_img_clip.tif'    
    
    # II. Label postfix of the indices
    label_ndvi = '_b5_ndvi.tif'
    label_ndwi = '_b6_ndwi.tif'
    label_builtup = '_b7_builtup.tif'
    
    # III. Check if file exist
    if os.path.isfile(img):
        print ('{} -> exist'.format(img))
    else:
        print ("File not exist")

    # IV. Calculate NDVI
    ndvi = img[:-4] + '{}'.format(label_ndvi)
    ndvi_result = calcNDVI(img, ndvi)
    if ndvi_result.all is not None:
        print('NDVI finished')
    
    # V. Calculate NDWI
    ndwi = img[:-4] + '{}'.format(label_ndwi)
    ndwi_result = calcNDWI(img, ndwi)
    if ndwi_result.all is not None:
        print('NDWI finished')
    
    # VI. Calculate Built Up Index
    builtup = img[:-4] + '{}'.format(label_builtup)
    builtup_result = calcBuiltUp(img, builtup)
    if builtup_result.all is not None:
        print('BuiltUp Index finished') 
    
    # VII. Label filenames for single bands & indices
    blue = img[:-4] + '_b1_blue.tif'
    green = img[:-4] + '_b2_green.tif'
    red = img[:-4] + '_b3_red.tif'
    nir = img[:-4] + '_b4_nir1.tif'
    lbl_ndvi = img[:-4] + '_b5_ndvi.tif'
    lbl_ndwi = img[:-4] + '_b6_ndwi.tif'
    lbl_builtup = img[:-4] + '_b7_builtup.tif'

    # VIII. Get one band and write it
    #exportSingleBand(img, 1, cstl)
    exportSingleBand(img, 1, blue)
    exportSingleBand(img, 2, green)
    exportSingleBand(img, 3, red)
    exportSingleBand(img, 4, nir)
    print('Single bands written')

    # IX. Label virtual & final raster
    label_vrt = '_vrt_stack.tif'
    label_rst = '_rst_stack.tif'
    vrt_raster = img[:-4] + '{}'.format(label_vrt)
    raster_stack = img[:-4] + '{}'.format(label_rst)
    
    # X. Build virtual raster
    cmd_vrt = 'gdalbuildvrt -separate {} {} {} {} {} {} {} {}'.format(vrt_raster, blue, green, red, nir, lbl_ndvi, lbl_ndwi, lbl_builtup)
    os.system(cmd_vrt)
    
    # XI. Translate virtual raster to raster
    cmd_final = 'gdal_translate {} {}'.format(vrt_raster, raster_stack)
    os.system(cmd_final)
    print('Bands merged')
    
    
    
    
    
    