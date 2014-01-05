# coding: utf-8
import sys
import shapefile
import csv
import os.path
import os

def readTable(tableName,tableField):
	table = {}
	with open(tableName,'r') as csvfile:
		reader = csv.DictReader(csvfile,delimiter=';')
		for row in reader:
			key = row[tableField]
			table[key] = row
	return table


def doJoin(shpName, shpField, years, tableField):
	outputName = "provincias_names"
	print "joining %s with all years into %s" % (shpName, outputName)

	yearTables = {}
	for year in years:		
		tableName = "d%s.csv" % (year,)
		yearTables[year] = readTable(tableName, tableField)

	# http://geospatialpython.com/2013/04/add-field-to-existing-shapefile.html
	r = shapefile.Reader(shpName)
	w = shapefile.Writer()

	joinFieldIndex = [field[0] for field in r.fields].index(shpField)-1

	w.fields = list(r.fields)
	for year in years:
		w.field(year + '_VARON','C','40')
		w.field(year + '_MUJER','C','40')

	for record in r.records():
		joinValue = record[joinFieldIndex]
		for year in years:
			tableRecord = yearTables[year][joinValue]
			varon = tableRecord['VARON']
			mujer = tableRecord['MUJER']
			record.append(varon)
			record.append(mujer)
		w.records.append(record)

	w._shapes.extend(r.shapes())
	w.save(outputName)

	return outputName


def main():
	shpName    = "Provincias.shp"
	shpField   = "Codigo"
	tableField = "CODIGO"
	years = [
		"1920",
		"1930",
		"1940",
		"1950",
		"1960",
		"1970",
		"1980",
		"1990",
		"2000",
		"2010"
	]

	outputName = doJoin(shpName, shpField, years, tableField)
	cmd = "zip %s.zip %s.*" % (outputName,outputName)
	os.system(cmd)

if __name__ == "__main__":
	sys.exit(main())
