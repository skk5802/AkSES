"""
A very specific script to go through the SNAP Permafrost dataset and find the specific months and years that we want for the AK project, move them to a project folder in ArcGIS, and clip them to a border of your choosing

Author: Sharon Kuo (kuo@d.umn.edu)
"""

import os
import arcpy
import pathlib
import glob
import pandas
import shutil
from arcpy import env
from arcpy.sa import *
from pathlib import Path

#This is where all the raw files are
input_dir = pathlib.Path(r"C:\Users\kuo\Documents\SNAP_data\Permafrost\gipl_talikthickness_cmip5_2021-2120")

#This is the project folder you will be working out of
env_workspace = pathlib.Path(r"C:\Users\kuo\Documents\ArcGIS\Projects\Seward_Michael\SNAP_Perma_talikthickness_Sew_Mich")

#This creates a dictionary of all the months you want for all the years you want. You can change these manually here
perma_dict = {}
year_list = [2023, 2025, 2030, 2035, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120]
model_list = ["5ModelAvg_rcp45", "5ModelAvg_rcp85"]
for year in year_list:
    perma_dict[year] = model_list
print(perma_dict)


#This takes all the entries in that dictionary and moves it to your project folder so that you only have the months/years that you want
for year, models in perma_dict.items():
     for model in models:          
          current_files = [f for f in input_dir.glob(f"*{model}_*{year}.tif")]
          [shutil.copy(filename, env_workspace) for filename in current_files]


#Now go to your workspace where your subsetted files are (this one is definitely necessary)
os.chdir(env_workspace)

#Make a list of all the geotifs
runlist = glob.glob("*.tif")
print(len(runlist)) #if this is still over a thousand files, you are in the wrong folder

# Identify the input polygon feature class with the areas of interest to clip

fc = pathlib.Path(r"C:\Users\kuo\Documents\ArcGIS\Projects\MyProject7\ClipSewardMichael.lyrx")

#Identify the raster you want to clip, what you want the resulting clipped raster to be called, and then run the clip function
#Bus notes: Keep .tif in the out_name even though it is annoying or Arcpy thinks you want a grid and then you only get 13 characters, which is bananas. 

for run in runlist:
    raster = pathlib.Path(env_workspace).joinpath(run)
    run_name = str(run)
    out_name = run_name.replace(".tif", "_clipped.tif")
    out_raster = pathlib.Path(env_workspace).joinpath(out_name)
    arcpy.management.Clip(in_raster = str(raster), out_raster = str(out_raster), in_template_dataset = str(fc), nodata_value = 666, clipping_geometry = 'ClippingGeometry')
