import PyPDF2

newfile = open('inText.txt','w')
file = open('sample-resumes_scs.pdf','rb')
pdfreader = PyPDF2.PdfFileReader(file)
num = pdfreader.getNumPages()
print(num)
#for i in range(num):
pageobj = pdfreader.getPage(5)
newfile.write(pageobj.extractText())
file.close()
newfile.close()
