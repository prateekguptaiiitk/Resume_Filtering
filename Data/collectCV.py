from tkinter import Tk
import os,os.path
import logging, time

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

PATH = os.path.join(os.getcwd(),'CVs')
r = Tk()
r.withdraw()

result = ""
cvno = 1
res = ""

try:
	while (True):
		result = r.selection_get(selection = 'CLIPBOARD')
		if res != result:
			with open(os.path.join(PATH,'cv'+str(cvno)),'wb') as fout:
				fout.write(result.encode('utf-8'))
				res = result
				logging.info('cv'+str(cvno)+' SUCCESS.')
				cvno += 1
				time.sleep(3)
except KeyboardInterrupt:
	r.destroy()
	logging.warning('PGM Interrupted.')
