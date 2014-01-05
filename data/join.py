# coding: utf-8
import sys
import shapefile
import csv
import os.path
import os
import shutil


def readTable(tableName,tableField):
	table = {}
	with open(tableName,'r') as csvfile:
		reader = csv.DictReader(csvfile,delimiter=';')
		for row in reader:
			key = row[tableField]
			table[key] = row
	return table


def doJoin(shpName, shpField, tableName, tableField):
	outputName = os.path.splitext(shpName)[0].lower() + "_" + os.path.splitext(tableName)[0].lower()
	print "joining %s with %s into %s" % (shpName, tableName, outputName)

	table = readTable(tableName, tableField)

	# http://geospatialpython.com/2013/04/add-field-to-existing-shapefile.html
	r = shapefile.Reader(shpName)
	w = shapefile.Writer()

	joinFieldIndex = [field[0] for field in r.fields].index(shpField)-1

	w.fields = list(r.fields)
	w.field('VARON','C','40')
	w.field('MUJER','C','40')

	for record in r.records():
		joinValue = record[joinFieldIndex]
		tableRecord = table[joinValue]
		varon = tableRecord['VARON']
		mujer = tableRecord['MUJER']
		record.append(varon)
		record.append(mujer)
		w.records.append(record)

	w._shapes.extend(r.shapes())
	w.save(outputName)

	shutil.copyfile( os.path.splitext(shpName)[0] + ".prj", outputName + ".prj" )

	return outputName


def main():
	shpName    = "Provincias.shp"
	shpField   = "Codigo"
	tableField = "CODIGO"

	tables = [
		"d1920.csv",
		"d1930.csv",
		"d1940.csv",
		"d1950.csv",
		"d1960.csv",
		"d1970.csv",
		"d1980.csv",
		"d1990.csv",
		"d2000.csv",
		"d2010.csv"
	]

	for tableName in tables:
		outputName = doJoin(shpName, shpField, tableName, tableField)
		cmd = "zip %s.zip %s.*" % (outputName,outputName)
		print cmd
		os.system(cmd)

if __name__ == "__main__":
	sys.exit(main())