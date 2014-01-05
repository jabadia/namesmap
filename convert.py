# coding: utf-8
import xlrd
import csv

def convertSheet(sheet,year):
	csvName = "d%04d.csv" % year
	print sheet.name,"->", csvName;
	with open( csvName, "w") as fp:
		writer = csv.writer(fp,delimiter=';')
		writer.writerow(["CODIGO","PROVINCIA","VARON","MUJER"])

		titleRowIndex = 3
		maleNameRowIndex = 5
		femaleNameRowIndex = 29
		for colIndex in range(1,sheet.ncols,3):
			(code,provincia) = sheet.cell(titleRowIndex,colIndex).value.split(' - ')
			varon = sheet.cell(maleNameRowIndex,colIndex).value
			mujer = sheet.cell(femaleNameRowIndex,colIndex).value
			writer.writerow([code,provincia.encode('utf-8'),varon.encode('utf-8'), mujer.encode('utf-8')])


def main():
	book = xlrd.open_workbook("nombres_por_fecha.xls")

	sheetNames = [
		# u"Indice",
		# u"ESPAÑA_hombres",
		# u"ESPAÑA_mujeres",
		(u"NACIDOS ANTES DE 1930",1920),
		(u"NACIDOS EN AÑOS 30",1930),
		(u"NACIDOS EN AÑOS 40",1940),
		(u"NACIDOS EN AÑOS 50",1950),
		(u"NACIDOS EN AÑOS 60",1960),
		(u"NACIDOS EN AÑOS 70",1970),
		(u"NACIDOS EN AÑOS 80",1980),
		(u"NACIDOS EN AÑOS 90",1990),
		(u"NACIDOS EN AÑOS 2000",2000),
		(u"NACIDOS EN AÑOS 2010",2010)
	];

	for (sheetName,year) in sheetNames:
		sheet = book.sheet_by_name(sheetName);
		convertSheet(sheet,year);



main();