# Step 1 - Data preparation

First, download the original data from the INE (Spanish Statistics Agency) [website](http://www.ine.es/daco/daco42/nombyapel/nombyapel.htm). The file I chose to download was [Nombres más frecuentes por fecha de nacimiento y provincia de nacimiento](http://www.ine.es/daco/daco42/nombyapel/nombres_por_fecha.xls)



The structure of the file is a bit different of what we need, so I decided to write a Python script to extract and format the data.

First, I prepared a small script that iterates through the relevant sheets of the workbook

	import xlrd
	import csv
	
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

For each of the sheets, we extract the data (fortunately it's the same layout in each of the sheets)

	def convertSheet(sheet,year):
		csvName = "d%04d.csv" % year
		print sheet.name,"->", csvName;
		with open( csvName, "w") as fp:
			writer = csv.writer(fp,delimiter=';')
			writer.writerow(["CODIGO","PROVINCIA","NOMBRE"])

			titleRowIndex = 3
			firstNameRowIndex = 5
			for colIndex in range(1,sheet.ncols,3):
				(code,provincia) = sheet.cell(titleRowIndex,colIndex).value.split(' - ')
				name = sheet.cell(firstNameRowIndex,colIndex).value
				writer.writerow([code,provincia.encode('utf-8'),name.encode('utf-8')])
#Step 2 - The Map
#The App