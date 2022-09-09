Work completed by Purvi Sehgal in July 2022 under mentorship of Dr. David Thompson
Program that takes in EMIT image 4 corners' latitude and longitude, time, and date, finds matching AERONET sites, interpolates AOD values to find AOD at 550 nm, 
and prints matching AERONET sites and respective AOD values.

Instructions:

Program input example provided in file ExampleData.png and ExampleData2.png

Run the program in FinalScript.py and input numbers as it asks. It will print matching sites and AOD values.

X refers to longitude and Y refers to latitude.

When inputting four EMIT corner lat/long, go in a clockwise direction. 

Negative values occur depending on the location with respect to the prime meridian and equator, so be cognizant of that.

The TIME_BUFFER is 5 minutes AKA 300 seconds, which can be modified. The TIME_BUFFER accounts for the fact that the 
time may not be the exact same for EMIT images and AERONET sites. 

Currently, the program was developed so that the year does not matter when matching EMIT images and AERONET sites. To ensure this, CURRENT_YEAR can be set to any constant number. However,
if we want the year to matter, hence only match 2022 EMIT images to 2022 AERONET sites, the code will need to be modified.

This program does not consider different time zones. Please test on a large data set before using. 
