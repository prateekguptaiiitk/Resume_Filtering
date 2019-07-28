import os
import logging, time

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

li = os.listdir('/Volumes/Seagate Expansion Drive/skybits dataset/stackexchange1')

comm = "7z x -y stackexchange/"

for i in range(1, len(li)):
	name = li[i]
	print("[INFO: EXTRACTION OF FILE", i, "-", name, "UNDER PROGRESS]")

	newname = li[i][:-3]
	os.system("mkdir "+ newname)
	commTemp = comm + name + " -o" + newname
	os.system("cd "+ newname)
	os.system(commTemp)
	os.system("cd ..")
	print("")

print("EVERYTHING OK, SUCCESSFULLY EXTRACTED ALL THE FILES!")