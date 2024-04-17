"""
demo.py
Spring 2023

Demonstrate file and directory handling.
"""

import pandas as pd
import geopandas as gpd
import os
import glob
import matplotlib.pyplot as plt

#
#  Function for listing files conveniently
#

def list_files(title,files):
    print(f'\n{title}:\n')
    [ print('  ',f) for f in files ]

#%%
#
#  Listing contents of a directory
#

files = os.listdir('raw')
list_files('Files in raw:',files)

#%%
#
#  Listing files using wildcard characters
#

nyiso = glob.glob('raw/20??01*')
list_files('NYISO files for January', nyiso)

bg = glob.glob('raw/bg??.csv')
list_files('Block group files', bg)

#%%
#
#  Working with path components
#

for fname in ['raw/bg06.csv', 'demo.py', 'raw/gb06.csv', 'raw']:

    print(f'\n{fname}:\n')
    print('   Basename:', os.path.basename(fname))
    print('   Dirname: ', os.path.dirname(fname))
    print('   Split:   ', os.path.split(fname))
    print('   Splitext:', os.path.splitext(fname))

    exists = os.path.exists(fname)
    print('   Exists?  ', exists)
    if exists:
        print('   Dir?     ', os.path.isdir(fname))
        print('   File?    ', os.path.isfile(fname))

#%%
#
#  Selecting and appending with file names
#

bg_data = {}

print('\nSelecting and appending files:\n')

for f in bg:
    raw = pd.read_csv(f)
    (path,filename) = os.path.split(f)
    bg_data[filename] = raw
    print('File',filename,'has',len(raw),'lines')

bg_all = pd.concat(bg_data)

print('\nAppended data has',len(bg_all),'lines')

print('\nIncludes filename as the index:\n')
print(bg_all.sample(10))

#%%
#
#  Reading an Excel workbook
#

bg_xlsx = glob.glob('raw/bg*.xlsx')
list_files('BG worksheet list',bg_xlsx)

#
#  Case 1: single sheet
#

case1 = 'raw/bg_single.xlsx'
wb1 = pd.read_excel(case1)
print(f'\nCase 1, single sheet: {case1}\n')
print(wb1.head())

#
#  Case 2: multiple sheets
#

case2 = 'raw/bg_multiple.xlsx'
wb2 = pd.read_excel(case2,sheet_name=None)
print(f'\nCase 2, multiple sheets: {case2}')
print('\nType of wb2:', type(wb2))
print('\nKeys:', wb2.keys())
print('\nExtracting a sheet:\n')
print(wb2['bg01'])

#%%
#
#  Writing a Stata databank. Need to make sure columns are
#  legal Stata variable names.
#

wb1.rename(columns={'block group':'block_group'},inplace=True)
wb1.to_stata('bg_single.dta',write_index=False)

dta_files = glob.glob('*.dta')
list_files('DTA files',dta_files)

#
#  Reading a Stata databank
#

wbx = pd.read_stata('bg_single.dta')

print('\nComparing data after rereading:\n')
print( (wb1 == wbx).all() )

#%%
#
#  Reading a shapefile from a zip with multiple layers.
#
#  Append the name of the SHP file to the zipfile's name
#  after an exclamation point.
#

zip1 = 'multiple_layers.zip'
layer = 'county.shp'

county = gpd.read_file(zip1+'!'+layer)

#
#  Zip with shapefile in a subdirectory
#
#  Append the name of the subdirectory (no .shp) to the zipfile's
#  name after an exclamation point.
#

zip2 = 'nested_layer.zip'
subdir = 'stores'

stores = gpd.read_file(zip2+'!'+subdir)

#
#  Draw a map
#

fig,ax1 = plt.subplots(dpi=300)
county.plot(color='tan',ax=ax1)
stores.plot(ax=ax1)
ax1.axis('off')
