# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
#csv-points.py
# Last Edit on: 2017-02-03 14:25:09.00000
# Made by Toby Zhang A00987765
# Description: This script takes a CSV file and a reference shapefile feature class to generate a point feature class with the csv file
# This file does the following steps in order:
# 1) Takes input CSV file and reference for spatial reference
# 2) Checks if pre-existing file is present, then deletes it if present
# 3) Adds a ParValue, Lat and Long field and sets the data type
# 4) Fills in the table with the CSV data and creating a point for each row of data
# Dependencies: The csv data must be about partiticulate data with the particulate value, lat, and long in the exact order for this script to work.
# The csv data must also be seperated with commas and not anything else. The csv file must also contain numeric data only.
# Limitations: The trackback stack call isn't working as intended yet.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import string
import math
import sys
import os
import traceback

try:
	#Script parameters:
	inputCSV = arcpy.GetParameterAsText(0)
	inputRef = arcpy.GetParameterAsText(1)
	output = arcpy.GetParameterAsText(2)

	#Pulls out spatial reference:
	spRef = arcpy.Describe(inputRef).spatialReference
	#splits up paths and directory
	drive, path_file = os.path.splitdrive(inputCSV)
	path, file = os.path.split(path_file)

	#creates the paths, file names, and full file path directory
	try:
		outpath = drive + "\\" + path 
		outname = file.replace('.','')[:-3]  + "_FC.shp"
		outfile = outpath +"\\"+ outname
		
	except arcpy.ExecuteError:

		arcpy.AddError("path error")
		traceback.print_stack()
		traceback.print_exc()

	#creates new point feature class. Deletes old feature class of same name if exists.
	try:
		arcpy.CreateFeatureclass_management(outpath, outname, "POINT", "", "", "", spRef)

	except arcpy.ExecuteError:
		arcpy.AddWarning("File: "+outfile+" already exists! Overwriting now!"+datetime.datetime.today().strftime("%B %d, %Y") )
		if arcpy.Exists(outfile):
			arcpy.Delete_management(outfile)	
			arcpy.CreateFeatureclass_management(outpath, outname, "POINT", "", "", "", spRef)
	#Add fields and data type
	try:	
		arcpy.AddField_management(outname, "ParValue", "LONG")
		arcpy.AddField_management(outname, "Lat", "DOUBLE")
		arcpy.AddField_management(outname, "Long", "DOUBLE")
		
	except arcpy.ExecuteError:
		arcpy.AddError("add field error")
		traceback.print_stack()
		traceback.print_exc()

	#Set inputs files and field names
	inFile = open(inputCSV, "r")
	fields = ['ParValue','Lat','Long']

	cursor = arcpy.InsertCursor(outfile)

	#loops the data into an array
	try:
	
		#sets csv input as 2D array
		csv_val = []
		#sets array pointer to 1 (which allows you to skip the first line which is a string)
		i = 1
		with inFile as data_file:
		
			#for loop that goes on for each line in the csv
			for line in data_file:
				#cleans up the data and splits the input by the commas
				csv_val.append(line.strip().split(','))
				#continues to loop so long as there is input as determined by the length of columns
				while i < len(csv_val):
					#sets the pointer and pulls values out of array for the column
					pnt = arcpy.Point()
					pv = csv_val[i][0]
					y = csv_val[i][1]
					x = csv_val[i][2]
					#adds new row and sets the attributes to the x and y and point object
					row = cursor.newRow()
					pnt.X = float(x)
					pnt.Y = float(y)
					row.SHAPE = pnt
					#pushes in the data into the table and inserts the row, the +1 to iterator
					row.setValue(fields[0], float(pv))
					row.setValue(fields[1], float(x))
					row.setValue(fields[2], float(y))
					cursor.insertRow(row)
					i += 1
			#clean up
			del row
			del cursor
			inFile.close()
	except arcpy.ExecuteError:
		arcpy.AddError("loop error")
		traceback.print_stack()
		traceback.print_exc()
except arcpy.ExecuteError:
	arcpy.AddError("Arcpy related error")
	traceback.print_stack()
	traceback.print_exc()
except:
	arcpy.AddError("Global execute error")
	traceback.print_stack()
	traceback.print_exc()
