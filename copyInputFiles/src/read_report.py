from shutil import copy2
from glob import glob

root_path = '/home/luis/Desktop/Proyects_Files/LISN/GPSs/Tareas/Resend_SCNfiles/'
report_path = root_path + 'createReports/output_files/'
input_path = root_path + 'copyInputFiles/input_files/'
output_path = root_path + 'copyInputFiles/output_files/'

station = 'lhyo'

def get_month_name(month): # arg:str ('06')
    if month == '01': return '01-Jan'
    elif month == '02': return '02-Feb'
    elif month == '03': return '03-Mar'
    elif month == '04': return '04-Apr'
    elif month == '05': return '05-May'
    elif month == '06': return '06-Jun'
    elif month == '07': return '07-Jul'
    elif month == '08': return '08-Aug'
    elif month == '09': return '09-Sep'
    elif month == '10': return '10-Oct'
    elif month == '11': return '11-Nov'
    elif month == '12': return '12-Dec'
    else: return ''   

def search_copy_s4(station):
    f = open(report_path + 'reporte_' + station + '.txt', 'r')
    fLines = f.readlines()
    i = 0
    state = 0 # indicate whether data migth begin 
    for line in fLines:
        line_i = line.strip("\n").split(" ")
        if line_i[0] != "***":
            # Read data within body 
            if state>0:
                if state==1: # year
                    year = line_i[0]
                    state=2
                elif state==2: # month
                    if line_i[0]!='':
                        month = line_i[0]
                        state=3
                    else:
                        state=1
                elif state==3: # days
                    for day in range(len(line_i)):
                        # Copy files 
                        if line_i[day]=='0':
                            # create input path
                            scnfile_prefix = year[-2:] + month + str(day).zfill(2) # e.g. '210810'
                            date_path = year + '/' + get_month_name(month) + '/' + scnfile_prefix # e.g. '2021/08-Aug/210810'
                            files_scn = glob(input_path + date_path + "*scn.gz")
                            if len(files_scn)>0:
                                for file in files_scn:
                                    copy2(file, output_path)
                                print("Files " + scnfile_prefix + "_*.scn.gz were copied succesfully!")
                    state=2
            else: # state=0
                # Read header
                if line_i[0]=="File_type":
                    file_type = line_i[1]
                elif line_i[0]=="Station":
                    station = line_i[1]
                # Read body
                elif line_i[0]=='':
                    state = 1
        else:
            #print("The end!")
            break 

def main():
    search_copy_s4(station=station)

if __name__=='__main__':
	print('GETTING STARTED ...')
	main()
	print('FINISHED!')
