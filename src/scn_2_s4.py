#!/home/luis/anaconda3/bin/python3
#__________________________________
#       CONVERT SCN 2 S4,TEC
#             v1.0
#----------------------------------
# This program converts scn files to
# s4 and TEC files.  
# Author: Luis D.
# :)
import glob, datetime

# Declare input and output paths 
root_path = "/home/luis/Desktop/Proyects_Files/LISN/GPSs/Tareas/Resend_SCNfiles/"
input_files_path = root_path + "input_files/data_set/"
input_files_path_op = root_path + "input_files/data_procesada/"
output_files_path = root_path + "output_files/"
station = 'puc'

def getS4(files_group_name):
	firstRun=1   # equal to 1 when the script first run
	correctDay = 0
	azimuthList=[]
	elevationList=[]
	s4List=[]
	prnList=[]
	#
	day = files_group_name[-2:]
	month = files_group_name[-4:-2]
	year = files_group_name[-6:-4]
	doyrequested=datetime.datetime.strptime(year+" "+month+" "+day,"%y %m %d").strftime("%j") # get doy from month year
	#
	list_input_files = glob.glob(files_group_name + "*.scn")
	list_input_files.sort()
	archivo = open(output_files_path+"l"+station+"_"+year+month+day+".s4","w") # creates an output s4 file
	#
	for scnFile in list_input_files:
		print("Processing:",scnFile)
		inf=open(scnFile,"r")	# open scn file to process
		fileLines = inf.readlines()
		for line in fileLines:   # Sweeps all lines in current scn file
			finalLine=[]
			line1 = line.strip("\n").split(" ")  # Removes CR and creates a list with elements in the line

			if line1[0]=="T":	# if line starts with T (ex. T 21 03 13 83671)
				if not(firstRun) and correctDay:	# the first time a "T" is found do not create line of s4 file
					s4Line = yearf+" "+doyf+" "+second+" "+str(len(prnList))+" "  # First part of s4 line: year doy seconds number_of_records  (ex. 21 072    31 11)
					index=0
					for elements in prnList:  # sweeps all records
						s4Line = s4Line + prnList[index]+" "+s4List[index]+" "+azimuthList[index]+" "+elevationList[index]+" "   # second part of s4 line: prn s4 azimuth elevation prn s4 ...
						index+=1
					s4Line = s4Line + "\n"
					archivo.write(s4Line)
					
					azimuthList=[]
					elevationList=[]
					s4List=[]
					prnList=[]
				else:
					firstRun=0
			
				line1=line1[1:]
				[finalLine.append(int(x)) for x in line1 if x != ""]  # Removes all empty elements ("")
				yearf="%.2d"%finalLine[0]   # get year
				doyf=datetime.datetime.strptime(yearf+" "+"%.2d"%finalLine[1]+" "+"%.2d"%finalLine[2],"%y %m %d").strftime("%j")   # get doy from month year extracted from file
				if doyf==doyrequested:	
					correctDay=1
				else:	
					correctDay=0
				second=str(finalLine[3])   # get seconds
			else:
				[finalLine.append(float(x)) for x in line1 if x != ""]  # Removes all empty elements ("")			
				azimuthList.append(str(finalLine[0]))	# get azimuth
				elevationList.append(str(finalLine[1]))	# get elevation
				s4List.append(str(finalLine[2]))	# get s4
				prnList.append(str(int(finalLine[11])))	# get prn

	archivo.close()

	return 'Ok'

def main():
	list_input_files1 = glob.glob(input_files_path + "*.scn") # e.g. ~/dir/210826_120000.scn
	# Get unique values
	list_input_files2 = [archivo[:-11] for archivo in list_input_files1] 
	list_input_files2 = list(set(list_input_files2)) # e.g. ~/dir/210826
	
	if len(list_input_files2) > 0:
		for files_group in list_input_files2:
			getS4(files_group)

	return 'Ok'

if __name__=='__main__':
	print('GETTING STARTED ...')
	main()
	print('FINISHED!')

