## Dependencies
import pandas as pd
import numpy as np

## PREPARE FUNCTION (PREVIOUS FORMAT)
def previous_prep(file_name):

    path = f"input/{file_name}"
    citibike_previous = pd.read_csv(path, low_memory=False)
    sample_previous = citibike_previous.sample(frac=0.02)
    sample_previous.reset_index(inplace=True)
    sample_previous.columns = sample_previous.columns.str.replace(' ', '').str.lower()

    gender_list = []
    for i in range(len(sample_previous)):
        if (sample_previous['gender'][i] == 1):
            gender_list.append('Male')
        elif (sample_previous['gender'][i] == 2):
            gender_list.append('Female')
        else:
            gender_list.append('Unknown')     
    
    sample_previous['gender_cat'] = gender_list
    # sample_previous['birthyear'] = sample_previous['birthyear'].astype(np.int64)

    columns_previous = ['bikeid',
                        'starttime', 'stoptime', 'tripduration',
                        'startstationid', 'startstationname',
                        'endstationid', 'endstationname',
                        'startstationlatitude', 'startstationlongitude', 
                        'endstationlatitude', 'endstationlongitude', 'usertype', 'birthyear', 'gender_cat']

    clean_previous =  sample_previous[columns_previous]
    clean_previous = clean_previous.rename(columns = {
        'bikeid': 'Bike Id',
        'starttime': 'Start DateTime',
        'stoptime': 'End DateTime',
        'tripduration': 'Duration [s]',
        'startstationid': 'Start Station Id',
        'startstationname': 'Start Station Name',
        'endstationid': 'End Station Id',
        'endstationname': 'End Station Name',
        'startstationlatitude': 'Start Lat',
        'startstationlongitude': 'Start Lon', 
        'endstationlatitude': 'End Lat',
        'endstationlongitude': 'End Lon',
        'usertype': 'Membership',
        'birthyear': 'Birth Year',
        'gender_cat': 'Gender'
    })

    return clean_previous


## PREPARE FUNCTION (CURRENT FORMAT)
def current_prep(file_name):

    path = f"input/{file_name}"
    citibike_current = pd.read_csv(path, low_memory=False)
    sample_current = citibike_current.sample(frac=0.02)
    sample_current.reset_index(inplace=True)
    
    delta = pd.to_datetime(sample_current['ended_at']) - pd.to_datetime(sample_current['started_at'])
    sample_current['Duration [s]'] = delta.dt.total_seconds().astype(np.int64)

    membership_list = []
    for i in range(len(sample_current)):
        if (sample_current['member_casual'][i] == 'member'):
            membership_list.append('Subscriber')
        elif (sample_current['member_casual'][i] == 'casual'):
            membership_list.append('Customer')
        else:
            membership_list.append('Unknown')  
    sample_current['Membership'] = membership_list

    columns_current = ['started_at',
                    'ended_at',
                    'Duration [s]',
                    'start_station_id',
                    'start_station_name',
                    'end_station_id',
                    'end_station_name',
                    'start_lat',
                    'start_lng',
                    'end_lat',
                    'end_lng',
                    'Membership']

    clean_current = sample_current[columns_current]
    clean_current = clean_current.rename(columns={
        'started_at': 'Start DateTime',
        'ended_at': 'End DateTime',
        'start_station_id': 'Start Station Id',
        'start_station_name': 'Start Station Name',
        'end_station_id': 'End Station Id',
        'end_station_name': 'End Station Name',
        'start_lat': 'Start Lat',
        'start_lng': 'Start Lon',
        'end_lat': 'End Lat',
        'end_lng': 'End Lon'
    })

    return clean_current


## PREVIOUS FORMAT LOOP
file_counter = 1

for year in range(4):
    for month in range(12):
        file_name = f"{2017+year}{month+1:02d}-citibike-tripdata.csv"
        clean_previous = previous_prep(file_name)

        if file_counter == 1:
            complete_previous = clean_previous
        else:
            complete_previous = complete_previous.append(clean_previous, ignore_index = True)
        
        print(f"File {file_counter:02d}: {file_name} (previous)")
        file_counter += 1

## Append January-2021
clean_previous = previous_prep("202101-citibike-tripdata.csv")
complete_previous = complete_previous.append(clean_previous, ignore_index = True)
print(f"File 00: 202101-citibike-tripdata.csv (previous)")

## Export to CSV
# complete_previous.to_csv("output/complete_previous.csv", index=False)


## CURRENT FORMAT LOOP
file_counter = 1

for month in range(5):
    file_name = f"2021{month+2:02d}-citibike-tripdata.csv"
    clean_current = current_prep(file_name)

    if file_counter == 1:
        complete_current = clean_current
    else:
        complete_current = complete_current.append(clean_current, ignore_index = True)
        
    print(f"File {file_counter:02d}: {file_name} (current)")
    file_counter += 1

## Export to CSV
# complete_current.to_csv("output/complete_current.csv", index=False)


## APPEND CURRENT TO PREVIOUS
citibike_analytics = complete_previous.append(complete_current, ignore_index = True)

## EXPORT TO CSV
citibike_analytics.to_csv("output/citibike_analytics.csv", index=False)

## END OF SCRIPT MSG
print("Data preparation is complete!")