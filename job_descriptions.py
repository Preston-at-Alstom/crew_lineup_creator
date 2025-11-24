import pypdf
import pandas as pd
import datetime as dt
from dataclasses import dataclass


# Selects the weekday or weekend package
def package_selector(day_of_Week):

    weekday_package = 'TO-ON-25-227 - Job Descriptions  WeekDAYs  eff November 23 2025.pdf'
    weekend_package = 'TO-ON-25-227 - Job Descriptions  WeekENDs  eff November 23 2025.pdf'

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    return weekday_package if day_of_Week in weekdays else weekend_package


def clear_duplicates(jd):
    for entry, job in enumerate(jd):
        # Start after first entry (0)
        if entry > 0:
            # compare job number and operating days with previous entry
            current_job = job
            previous_job = jd[entry -1  ]

            
            if  current_job.job_number == previous_job.job_number and \
                current_job.operating_days == previous_job.operating_days and \
                current_job.trips == []   :
                
                jd.pop(entry)
                

    return jd


def to_df(operating_day, special_package):
    
    # Select Weekday or Weekend Package
    if special_package == None:
        selected_job_package = package_selector(operating_day)
    else:
        selected_job_package = special_package
    

    # create Job template
    @dataclass
    class Job():
        job_number          : str
        on_duty             : str
        on_duty_location    : str
        operating_time      : str
        work_time           : str
        split_time          : str
        trips               : list
        interact_with_crew  : list
        operating_days      : str
        off_duty            : str

    # create Trip template
    @dataclass
    class Trip():
        job_number          : str = ''
        service_type        : str = ''
        train_number        : str = ''
        start_location      : str = ''  
        finish_location     : str = ''
        departure           : str = ''
        arrival             : str = ''
        operating_days      : str = ''
    
    
    # creating a pdf reader object
    reader = pypdf.PdfReader(selected_job_package)

    # Find the number of pages
    number_of_pages = len(reader.pages)

    # Create list to hold all the jobs
    Job_Descriptions = []

    # Create list to hold trip info for each job
    Job_Trips = []

    # Filter list 
    filter = ['Non-Revenue', 'Revenue', 'DH', 'VAN', 'SHUTTLE', 'Split from', 'takeover', 'handover','DEF' ,'FUEL', 'STBY']

    # Loop through pages
    for  page in range(number_of_pages):
        
        # Read page content
        page_content = reader.pages[page].extract_text()


        trips_list = []
        interact_list = []    
        
        # Read line by line and extract data
        
        for line in page_content.splitlines():
            
            line_as_list = line.split()
                
            if len(line_as_list) > 0:
                first_item = line_as_list[0]
                        
                if first_item == 'Operating':
                    operating_time = line_as_list[-1]

                if first_item == 'Platform':
                    on_duty_location = line_as_list[5][0:2]
                    off_duty = line_as_list[8]
                    split_time = line_as_list[11][0:5]

                if first_item == 'Work':                
                    work_time = line_as_list[-1]

                if first_item in ['Valid', 'Eff']:
                    job_number = line_as_list[-1]
                    first_item = 'Mon-Fri'
                    on_duty = line_as_list[-4]
                    
                if first_item in ['Mon-Fri', 'Friday', 'Saturda', 'Sunday', 'Sat-Sun', 'Saturday', 'Mon-Thu']:
                    if first_item == 'Mon-Fri': operating_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                    if first_item == 'Mon-Thu': operating_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']
                    if first_item == 'Friday': operating_days  = ['Friday']
                    if first_item == 'Saturda' or first_item == 'Saturday': operating_days = ['Saturday']
                    if first_item == 'Sunday': operating_days = ['Sunday']
                    if first_item == 'Sat-Sun': operating_days = ['Saturday', 'Sunday']
                    job_number = line_as_list[-1]
                    on_duty = line_as_list[-4]
                    
                if first_item in filter:  
                    if first_item in ['VAN', 'SHUTTLE', 'STBY']: line_as_list.insert(1, '')
                    if first_item in ["Non-Revenue", "Revenue"]: line_as_list.remove('trip')
                    if first_item in ['takeover', 'handover']: line_as_list[1:1]= ['' , '', '']
                    
                    formatted_line  = ''  
                    
                    service_type    = first_item
                    train_number    = line_as_list[1]
                    start_location  = line_as_list[2]
                    finish_location = line_as_list[3]
                    departure       = line_as_list[4]
                    arrival         = line_as_list[5]
                    

                    if  first_item in ['VAN', 'SHUTTLE']:
                        formatted_line = f'{service_type} | {start_location[0:2]} {departure} > {finish_location} {arrival}'
                        
                    if  first_item in ["Non-Revenue", "Revenue", 'DH']:
                        formatted_line = f'{train_number} | {service_type} | {start_location} {departure} > {finish_location} {arrival}'

                    if first_item in ['STBY']:
                        formatted_line = f'{service_type} @ {start_location[0:2]} {departure} > {arrival}'
                    
                    if first_item in ['FUEL', 'DEF' ]:
                        formatted_line = f'{service_type} @ {start_location} {departure} > {arrival}'

                    if first_item in ['handover', 'takeover']:
                        interact_list.append(line_as_list[-1])
                        formatted_line = f'{first_item} > {line_as_list[-1]}'
                        
                        
                    trips_list.append(formatted_line)
                    Job_Trips.append(Trip(job_number, service_type, train_number, start_location, finish_location, departure, arrival, operating_days))
                    
            
        
        # Job_Descriptions[page] = Job(job_number , on_duty , on_duty_location , operating_time , work_time , split_time , trips_list , interact_list, operating_days , off_duty)
        if operating_day in operating_days:

            Job_Descriptions.append(Job(job_number , on_duty , on_duty_location , operating_time , work_time , split_time , trips_list , interact_list, operating_days , off_duty))


    

    return pd.DataFrame([job.__dict__ for job in Job_Descriptions]),  pd.DataFrame([trip.__dict__ for trip in Job_Trips])

