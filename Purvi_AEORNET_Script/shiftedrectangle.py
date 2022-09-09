import csv
from datetime import datetime
from bisect import bisect_left
import math
import numpy as np
from matplotlib import pyplot as plt

def create_dictionary():
    file_name = input("What is the filename?")
    dict = {}
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            time_AERONET = row["Time(hh:mm:ss)"]
            day_AERONET = row["Day_of_Year(Fraction)"]
            timestamp = convert_to_timestamp(day_AERONET, time_AERONET)
            longitude = row["Site_Longitude(Degrees)"]
            latitude = row["Site_Latitude(Degrees)"]
            site = row["AERONET_Site"]
            AOD = str(calculate_550_AOD(row))
            dict[timestamp] = (time_AERONET, longitude, latitude, site, AOD)
    return dict

def get_input():
    x1, y1 = input("What is the longitude and latitude of the first corner of the EMIT image (in X <SPACE> Y coordinates)? ").split()
    x2, y2 = input("What is the longitude and latitude of the second corner of the EMIT image (in X <SPACE> Y coordinates) in clockwise direction? ").split()
    x3, y3 = input("What is the longitude and latitude of the third corner of the EMIT image (in X <SPACE> Y coordinates) in clockwise direction? ").split()
    x4, y4 = input("What is the longitude and latitude of the fourth corner of the EMIT image (in X <SPACE> Y coordinates) in clockwise direction? ").split()
    return x1, y1, x2, y2, x3, y3, x4, y4 


def calculate_550_AOD(row):
    y_value_list = []
    x_value_list = []
    LOG_BASE = 10
    wavelength_list = [1640, 1020, 870, 865, 779, 675, 667, 620, 560, 555, 551, 532, 531, 510, 500, 490, 443, 440, 412, 400, 380, 340]
    for wavelength in wavelength_list:
        AOD_value = row["AOD_{}nm".format(wavelength)]
        if AOD_value != "-999":
            y_value_list.append(float(AOD_value)) 
            x_value_list.append(wavelength/1000) 
    y_value_array = np.array(y_value_list)
    x_value_array = np.array(x_value_list)
    y_log_data = np.log10(y_value_array)    
    x_log_data = np.log10(x_value_array)
    # plt.plot(x_value_array, y_value_array, linewidth=2.0)
    # plt.plot(x_log_data, y_log_data, linewidth=2.0)
    #a0, a1 = np.polyfit(x_log_data, y_log_data, 1)
    curve = np.polyfit(x_log_data, y_log_data, 1)
    # for i in range(min(x_value_array), max(y_value_array)):
    #    plt.plot(i, ((LOG_BASE^(a0))*(i^a1)), 'go')  
    # plt.show() 
    freq_550_log = math.log(.550, LOG_BASE)
    AOD = np.polyval(curve, freq_550_log) 
    AOD_550 = LOG_BASE**(AOD)
    # plt.plot(.550, AOD_550, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
    # plt.show()
    return AOD_550

def convert_to_timestamp(date, time):
    #why is date messing up in csv
    CURRENT_YEAR = 2022
    year = CURRENT_YEAR #arbitrary year so that year does not affect results
    #accounts for day/month given in one digit instead of 2
    month_pos = date.find('/')
    month = int(date[0:month_pos])
    day_pos = date[month_pos+1:].find('/')
    day = int(date[month_pos+1: day_pos+month_pos+1])
    # month = int(date[3:5])
    # day = int(date[0:2])
    hour_pos = time.find(':')
    hour = int(time[0:hour_pos])
    minute_pos = time[hour_pos+1:].find(':')
    minute = int(time[hour_pos+1: minute_pos+hour_pos+1])
    minute_pos = minute_pos+hour_pos+1
    # hour = int(time[0:2])
    #minute = int(time[3:5])
    second = int(time[minute_pos+1: minute_pos+3])
    #second = int(time[6:8])
    daytime = datetime(year, month, day, hour, minute, second)
    dtimestamp = daytime.timestamp()
    return dtimestamp


def get_EMIT_time():
    time = input("What is the time of the image? Format: hh:mm:ss? ")
    date = input("What is the date of the image? Format: mm/dd/yyyy? ")
    EMIT_timestamp = convert_to_timestamp(date, time)
    return EMIT_timestamp    

#consider different time zones? 
def sort_dictionary(dict):
    keys = list(dict.keys())
    keys.sort()
    return keys

def find_similar_time(EMIT_time, sorted_list, dict):
    # time buffer currently set to five minutes
    dict_sorted = {}
    TIME_BUFFER = 300 
    max_minutes_EMIT = EMIT_time + TIME_BUFFER
    min_minutes_EMIT = EMIT_time - TIME_BUFFER
    #binary search
    max_index = bisect_left(sorted_list, max_minutes_EMIT)
    min_index = bisect_left(sorted_list, min_minutes_EMIT)
    similar_times = sorted_list[min_index:max_index] 
    x1, y1, x2, y2, x3, y3, x4, y4 = get_input()
    for time in similar_times:
        dict_sorted[time] = dict[time]
        if is_valid_data(dict_sorted, time, x1, y1, x2, y2, x3, y3, x4, y4):
           AOD_550 = dict_sorted[time][4]
           site = dict_sorted[time][3]
           longitude = dict_sorted[time][1]
           latitude = dict_sorted[time][2]
           time = dict_sorted[time][0]
           print(f'The site is: {site}. The longitude is: {longitude}. The latitude is: {latitude}. The time is: {time}. The aerosol optical depth is: {AOD_550} \n')


def is_valid_data(dict_sorted, time, x1, y1, x2, y2, x3, y3, x4, y4):
    if dict_sorted == {}:
        return False 
    x_AERONET = dict_sorted[time][1]
    y_AERONET = dict_sorted[time][2]
    x_AERONET = float(x_AERONET)
    y_AERONET = float(y_AERONET)
    x1 = float(x1)
    y1 = float(y1)  
    x2 = float(x2)
    y2 = float(y2)
    x3 = float(x3)
    y3 = float(y3)
    x4 = float(x4)
    y4 = float(y4)
    #checks if the AERONET longitude and latitude are within the image box
    return PointInRectangle(x_AERONET, y_AERONET, x1, y1, x2, y2, x3, y3, x4, y4)

#no two coordinates can have same x and y values (i.e. 3000, 3000 and 5000, 5000)
#checks if in rectangle by creating two triangles and checking if in any of the two triangles 
def PointInRectangle(x_AERONET, y_AERONET, x1, y1, x2, y2, x3, y3, x4, y4):
    
    check_in_rectangle = PointInTriangle(x1, y1, x2, y2, x3, y3, x_AERONET, y_AERONET) or PointInTriangle(x1, y1, x4, y4, x3, y3, x_AERONET, y_AERONET)
    return check_in_rectangle

#used formula from online 
def PointInTriangle(x1, y1, x2, y2, x3, y3, x, y):
    det = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    return  det * ((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) >= 0 and det * ((x3 - x2) * (y - y2) - (y3 - y2) * (x - x2)) >= 0 and det * ((x1 - x3) * (y - y3) - (y1 - y3) * (x - x3)) >= 0    

#mainloop     
if __name__ == "__main__":
    dict = create_dictionary()
    sorted_list = sort_dictionary(dict)
    EMIT_timestamp = get_EMIT_time()
    dict_sorted = find_similar_time(EMIT_timestamp, sorted_list, dict)






