# Elanco-Placement-Program-Technical-Task---Backend

This project looks at a Tick Sighting data set. It is a back end system for a web application that processes, analyses and manages the data.

This project looks at a Tick Sighting data set. It is a back end system for a web application that processes, analyses and manages the data. Throughout this project I used AI to support my work. However, I did not have a subscription to them so had to use many different forms. Due to this I was not able to implement the APIs successfully as I have never worked with them before and did not feel confident doing so in a short period of time without the support of a team or AI.

When considering using APIs for this project I would need to import a client to my back end code that will wrap API calls. After receiving the API information (such as what species the user wants to see data for) the API should be converted into the same layout as the rest of my code so it is readable to the program. Then the function is processed. The data will then be saved and fed back to the API. The ways to make the APIs more secure is to make sure there is no data missing when it is passed in or out of my program and, if it is, informing the user that there has been an issue and it needs to be looked at to check it has been run correctly. Another problem that might arise is data quality issues. The way to reduce this is by running test data and moderating it, making sure your data is consistent and making the appropriate changes where it is not.

Within this project my code takes in the tick sighting.xlsx file. It then filters it so that any repeated data is deleted so there is only one copy. This reduces errors when analysing it as there will not be multiple of the exact same file. It also filters all the empty values and saves them as "unknown" so that none of the data is lost; it is just filed correctly. The next change that is made to the file is the date is set to ISO 8601 format so there is no confusion on what order it is in and how to read it, keeping it consistent throughout the data set. It will then produce a matrix to show the user what file was read, any rows deleted and where the data is now saved as a CSV. This was mainly for testing purposes.

The code then allows the user to search the code by time and location, whether this be from a set time or between times as well as up to a time. It allows the user to express where they want the data to be saved and then confirms how many rows have been saved to that file when run correctly.

The code then can write a report on a file the user chooses, saved as report.txt, that contains the total sightings, the number of cases per location and the number of sightings per month.

## how to run code
To download the repository:
git clone https://github.com/naomi634/Elanco-Placement-Program-Technical-Task---Backend.git

To get the code folder:
cd Elanco-Placement-Program-Technical-Task---Backend/ElancoCode

Then to run the main file:
python main.py

To filter data you can do a few things:
  - To filter on location (in this example it’s London but it can be anything) = python main.py search --location London
  - To filter on time (this one is between two dates but you can choose to just put a start point or an end) = python main.py search --start 2019-07-08 --end 2024-12-05
  - And you can combine them = python main.py search --location London --start 2019-07-08 --end 2024-12-05
  - You can save the filtered data as a CSV = python main.py search --location London -o london_filtered.csv

To report on the data:
  - To report on the whole data set = python main.py report
  - To report on a filtered file = python main.py report london_filtered.csv
  - All the reports will be saved as report.txt and will replace all the data previously in it.







