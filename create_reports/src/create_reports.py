from glob import glob 
from datetime import datetime

root_path = "/home/luis/Desktop/Proyects_Files/LISN/GPSs/Tareas/Resend_SCNfiles/create_reports/"
input_files_path = root_path + "input_files/"
output_files_path = root_path + "output_files/"

data_type = 's4'

def max_days(month, year): # month & year: strings 
    if month == '01':
        return 31
    elif month == '02': # Leap year 
        year = int(year)
        if year%4==0:
            if year%100==0:
                if year%400==0:
                    return 29
                else:
                    return 28
            else:
                return 29
        else:
            return 28
    elif month == '03':
        return 31
    elif month == '04':
        return 30
    elif month == '05':
        return 31
    elif month == '06':
        return 30
    elif month == '07':
        return 31
    elif month == '08':
        return 31
    elif month == '09':
        return 30
    elif month == '10':
        return 31
    elif month == '11':
        return 30
    elif month == '12':
        return 31

def filter_stations(stations_path): # arg: list
    new_stations_list = []
    for station in stations_path:
        station_name = station[len(input_files_path):-1] # e.g. 'lhyo'
        if station_name[0]=='l' and len(station_name)==4:
            new_stations_list.append(station)
    return new_stations_list

def filter_years(years_path): # arg: list
    new_years_list = []
    for year in years_path:
        year_name = year.strip('/').split('/')[-1] # e.g. '2021'
        if year_name.isnumeric() and len(year_name)==4:
            new_years_list.append(year)
    return new_years_list

def filter_months(months_path): # arg: list
    new_months_list = []
    for month in months_path:
        month_name = month.strip('/').split('/')[-1] # e.g. '10'
        if month_name.isnumeric():
            if 0<int(month_name)<13:
                new_months_list.append(month)
    return new_months_list

def create_reports():
    # Create the stations list 
    list_stations = glob(input_files_path+'*/') 
    list_stations = filter_stations(list_stations)
    list_stations.sort()

    for station_path in list_stations:
        station_name = station_path[-5:-1] # e.g. 'lhyo'
        f = open(output_files_path + "reporte_" + station_name + ".txt", 'w')
        f.write("GPS files report - LISN network \n")
        f.write("------------------------------- \n")
        f.write("Station: " + station_name + "\n")
        f.write("File type: " + data_type + "\n")
        f.write("------------------------------- \n")
        #
        # Create the year list 
        #new_path = input_files_path + station_name + "/"
        list_years = glob(station_path + '*/') 
        list_years = filter_years(list_years)
        list_years.sort()
        for year_path in list_years:
            year_name = year_path[-5:-1] # e.g. '2021'
            # write on status file
            f.write("\n")
            f.write(year_name + "\n")
            #f.write(data_type + "\n")

            # Create the month list 
            list_months = glob(year_path+'*/') 
            list_months = filter_months(list_months)
            list_months.sort()
            #print(list_months)
            for month_path in list_months:
                month_name = month_path[-3:-1] # e.g. '08'
                list_s4 = glob(month_path + "scint/" + "*s4.gz")
                list_s4.sort()
                #print(month_name)
                #print()
                # Create the file's body 
                status_files = []
                mes = range(max_days(month_name, year_name))
                for day in mes:
                    day = str(day+1).zfill(2) # e.g. '07'
                    fecha_comp = month_path + "scint/" + station_name + "_" + year_name[-2:] + month_name + day + ".s4.gz" # e.g. 'lcuz_210205.s4.gz'
                    #print(fecha_comp)
                    if fecha_comp in list_s4:
                        status_files.append(str(1))
                    else:
                        status_files.append(str(0))

                status_files2 = ",".join(status_files) # create a single string 
                # write on status file
                f.write(month_name + "\n")
                f.write(status_files2 + "\n")
        
        f.write("\n") 
        f.write("-------------------------------------------- \n")
        f.write("File generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " UTC-5")    
        f.close()
    
    print("Reports were created succesfully!")
    return 'Ok'    

def main():
    create_reports()
    return 'Ok'

if __name__=='__main__':
	print('GETTING STARTED ...')
	main()
	print('FINISHED!')