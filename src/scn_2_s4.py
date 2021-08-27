# Extracts s4 data from scn files in GPS LISN stations
import glob, datetime

yearList= ["21"]
monthList = ["08"]
dayList = ["26"] #["07","14","15","16","29"]
station= "puc"

inPath= "/home/luis/Desktop/Proyects_Files/LISN/GPSs/Tareas/Resend_SCNfiles/input_files/"
outPath="/home/luis/Desktop/Proyects_Files/LISN/GPSs/Tareas/Resend_SCNfiles/output_files/"

firstRun=1   # equal to 1 when the script first run
correctDay = 0

azimuthList=[]
elevationList=[]
s4List=[]
prnList=[]

print(station)
for yearR in yearList:

	for monthR in monthList:

		for dayR in dayList:		
			doyrequested=datetime.datetime.strptime(yearR+" "+monthR+" "+dayR,"%y %m %d").strftime("%j")   # get doy from month year
			scnFileList=glob.glob1(inPath,yearR+monthR+dayR+"*.scn")  # Creates a list of scn files in input folder, there should be 24 per day
			scnFileList.sort()  # sort list
			s4of=open(outPath+"l"+station+"_"+yearR+monthR+dayR+".s4","w")	 # creates output s4 file
			for scnFile in scnFileList:			# Sweeps all scn files in the list
				print("Processing:",scnFile)
				inf=open(inPath+scnFile,"r")		# open scn file to process
				fileLines = inf.readlines()
				for line in fileLines:   # Sweeps all lines in current scn file
					finalLine=[]
					line1 = line.strip("\n").split(" ")  # Removes CR and creates a list with elements in the line

					if line1[0]=="T":			# if line starts with T (ex. T 21 03 13 83671)
						if not(firstRun) and correctDay:		# the first time a "T" is found do not create line of s4 file
							s4Line=yearf+" "+doyf+" "+second+" "+str(len(prnList))+" "  # First part of s4 line: year doy seconds number_if_records  (ex. 21 072    31 11)
							index=0
							for elements in prnList:  # sweeps all records
								s4Line = s4Line + prnList[index]+" "+s4List[index]+" "+azimuthList[index]+" "+elevationList[index]+" "   # second part of s4 line: prn s4 azimuth elevation prn s4 ...
								index+=1
							s4Line = s4Line + "\n"
							s4of.write(s4Line)
							
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
						azimuthList.append(str(finalLine[0]))   	# get azimuth
						elevationList.append(str(finalLine[1]))   # get elevation
						s4List.append(str(finalLine[2]))				# get s4
						prnList.append(str(int(finalLine[11])))	# get prn
						#tecList.append(  		    finalLine[xx])		# get tec
		
		s4of.close()
		
		
