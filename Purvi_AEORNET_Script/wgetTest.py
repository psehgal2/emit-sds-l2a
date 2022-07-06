import csv
import math
import numpy as np
from matplotlib import pyplot as plt


def get_input():
    xleft, yleft = input("What is the longitude and latitude of the bottom left corner of the EMIT image (in X <SPACE> Y coordinates)? ").split()
    xright, yright = input("What is the longitude and latitude of the top right corner of the EMIT image (in X <SPACE> Y coordinates)? ").split()
    time = input("What is the time of the image? Format: hh:mm:ss? ")
    day = input("What is the day of the year of the image (range 0-> 360)? Please refer to: https://www.scp.byu.edu/docs/doychart.html. If comparison data is from leap year, please account for that)")
    file_name = input("What is the name of the file? ")
    return xleft, yleft, xright, yright, time, day, file_name

#check if the result is in the box
def is_valid_data(x_AERONET, y_AERONET, time_AERONET, day_AERONET, xleft, yleft, xright, yright, time, day):
    #checks if the day and month are correct 
    #59th and 0th minute edge cases not considered
    if day == day_AERONET:
       hours_AERONET = int(time_AERONET[0: 2])
       minutes_AERONET = int(time_AERONET[3: 5])
       hours = int(time[0: 2])
       minutes = int(time[3: 5])
       # time buffer currently set to 1 minute
       TIME_BUFFER = 1
       max_minutes_AERONET = minutes_AERONET + TIME_BUFFER
       min_minutes_AERONET = minutes_AERONET - TIME_BUFFER
       #checks if the time matches aeronet time
       xleft = abs(float(xleft))
       yleft = abs(float(yleft))
       xright = abs(float(xright))
       yright = abs(float(yright))
       x_AERONET = abs(float(x_AERONET)) 
       y_AERONET = abs(float(y_AERONET))
       if (minutes <= max_minutes_AERONET) and (minutes >= min_minutes_AERONET) and (hours == hours_AERONET):
           #checks if the AERONET longitude and latitude are within the image box
           if (x_AERONET >= xleft and x_AERONET <= xright) or (x_AERONET <= xleft and x_AERONET >= xright):
               # checks if the y coordinate is correct and accounts for both sides of the equator
               if (y_AERONET >= yleft and y_AERONET <= yright) or (y_AERONET <= yleft and y_AERONET >= yright):
                  return True
    return False

def parse_data(): 
    xleft, yleft, xright, yright, time, day, file_name = get_input()
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            time_AERONET = row["Time(hh:mm:ss)"]
            day_AERONET = row["Day_of_Year"]
            longitude = row["Site_Longitude(Degrees)"]
            latitude = row["Site_Latitude(Degrees)"]
            if is_valid_data(longitude, latitude, time_AERONET, day_AERONET, xleft, yleft, xright, yright, time, day): 
               site = row["AERONET_Site"]
               AOD = calculate_550_AOD(row) 
               print(f'The site is: {site}. The longitude is: {longitude}. The latitude is: {latitude}. The aerosol optical depth is: {AOD} \n')           

def calculate_550_AOD(row):
    y_value_list = []
    x_value_list = []
    LOG_BASE = 10
    wavelength_list = [1640, 1020, 870, 865, 779, 675, 667, 620, 560, 555, 551, 532, 531, 510, 500, 490, 443, 440, 412, 400, 380, 340]
    wavelength_list.reverse()
    for wavelength in wavelength_list:
        AOD_value = row["AOD_{}nm".format(wavelength)]
        if AOD_value != "-999":
            y_value_list.append(float(AOD_value)) 
            x_value_list.append(wavelength/1000) 
    y_value_array = np.array(y_value_list)
    x_value_array = np.array(x_value_list)
    y_log_data = np.log10(y_value_array)    
    x_log_data = np.log10(x_value_array)
    print(x_value_array)
    print(y_value_array)
    plt.plot(x_value_array, y_value_array, linewidth=2.0)
    # plt.plot(x_log_data, y_log_data, linewidth=2.0)
    a0, a1 = np.polyfit(x_log_data, y_log_data, 1)
    print(x_log_data)
    print(y_log_data)
    curve = np.polyfit(x_log_data, y_log_data, 1)
    # for i in range(min(x_value_array), max(y_value_array)):
    #    plt.plot(i, ((LOG_BASE^(a0))*(i^a1)), 'go')  
    # plt.show() 
    freq_550_log = math.log(.550, LOG_BASE)
    print(freq_550_log)
    AOD = np.polyval(curve, freq_550_log) 
    print(AOD)
    # plt.plot(freq_550_log, AOD, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
    # # plt.show()
    AOD_550 = LOG_BASE**(AOD)
    print(AOD_550)
    plt.plot(.550, AOD_550, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
    plt.show()
    return AOD_550





if __name__ == "__main__":
    parse_data()

#be able to not consider top few rows 
            
            
            
            




