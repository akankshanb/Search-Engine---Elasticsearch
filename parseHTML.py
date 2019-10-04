from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import xlrd
import openpyxl


dataPath = join('.', 'data', 'NC_Bill_Text')
dataFiles = [f for f in listdir(dataPath) if isfile(join(dataPath, f))]

spreadsheetPath = join('.', 'data', "nc-legislation-data-2019-2020-session.xlsx")
workbook = xlrd.open_workbook(spreadsheetPath)
worksheet = workbook.sheet_by_index(0)
wb = openpyxl.load_workbook(filename=spreadsheetPath)
ws = wb.worksheets[0]


firstCol = worksheet.col(0)
billIds = []
for cell in firstCol:
  billIds.append(cell.value.decode('ascii', 'ignore'))


dataDict = {}
for f in dataFiles:
  dataFile = open(join(dataPath, f), 'r')
  data = dataFile.read()
  soup = BeautifulSoup(data)

  billId = f[0:-7]
  dataDict[billId] = ""


  for p in soup.find_all('p'):
    try: 
      pClass = p['class'][0]
      #if 'Title' in pClass:  #Title of the bill
      #  spans = p.find_all('span')
      #  dataDict[billId]['title'] = []
      #  print(spans)
      if 'Margin' in pClass or 'BillSection' in pClass:  #Basically the summary of the bill
        spans = p.find_all('span')
        spanText = ""
        for span in spans:
          spanText += str(span.text.encode('ascii', 'ignore').replace("\n", " ").replace("\r"," ").replace("{}", ""))
        dataDict[billId] = str(dataDict[billId]) +  " " + spanText
        #print(spans)
      #if 'Base' in pClass:    #Seems unneccessary
      #  spans = p.find_all('span')
      #  print(spans)
      #if 'BillSection' in pClass:   #Specific details of the bill
      #  spans = p.find_all('span')
      #  print(spans)
    except:
      print("An exception with finding class of paragraph occurred")

print(len(dataDict))
for key in dataDict:
  for i in range(1, len(billIds)):
    if billIds[i] == key:
      ws.cell(row=i+1, column=10).value = str(dataDict[key])

wb.save(spreadsheetPath)
