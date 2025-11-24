import datetime as dt
import pandas as pd
import job_descriptions


def generate_filename():
    date  = dt.date.today() + dt.timedelta(days=1)
    month = date.strftime("%B")
    day   = f'{date.day:02d}' 
    year  = date.year
    day_of_week = date.strftime('%A')

    formated_date = f'{day_of_week} {month} {day}, {year}'

    return f'GO and UPE Crew Lineup {month} {day}, {year}.xlsx', day_of_week, formated_date


def create_lineup(lineup_object, special_package):

    filename, day_of_week , formated_date = generate_filename()


    # Columns to save
    required_columns = ('Tour #', 'Crew Number','QCTO Daily', 'CTO Daily', 'CSA Daily', 'Extra CTO Daily', 
                        'Extra CSA Daily', 'Qualified Daily', 'Terms Daily', 'QCTO', 'CTO', 'CSA', 'Extra CTOs', 'Extra CSAs')
    

    # Exclusion lists
    go_jobs         = range(100000, 399999)
    extra_jobs      = range(4000  , 4999 )
    extra_jobs_2    = range(400000 , 499999 )
    drivers_jobs    = range(9000  , 9899  )
    upe_jobs        = range(500000, 599999)
    #crew_dispatcher= range(9900, 9999)
    #spare_board    = range(3000,3999)

   
    # create a dataframe from the source data
    source_df = pd.read_excel(lineup_object, usecols=required_columns)
    source_df = source_df.rename(columns={'Crew Number': 'Crew #'})
            
    go_lineup     = source_df[source_df['Tour #'].isin(go_jobs)     ] 
    extra_lineup  = source_df[source_df['Tour #'].isin(extra_jobs)  ] 
    extra_lineup_2= source_df[source_df['Tour #'].isin(extra_jobs_2)] 
    driver_lineup = source_df[source_df['Tour #'].isin(drivers_jobs)] 
    upe_lineup    = source_df[source_df['Tour #'].isin(upe_jobs)    ] 
    
    job_info, _   = job_descriptions.to_df(day_of_week, special_package)
    job_numbers   = job_info['job_number'].tolist()
    on_duty_times = job_info['on_duty'].tolist()

    job_numbers   += ['19000', '19240', '29000', '29240'] 
    on_duty_times += ['03:00', '15:00', '03:00', '15:00']

    job_info_list = dict(zip (job_numbers, on_duty_times))
    

    compiled_lineup = pd.concat([go_lineup, extra_lineup, extra_lineup_2, driver_lineup, upe_lineup], ignore_index=True)
        
    compiled_lineup.to_excel(filename, index = False, engine='openpyxl')
    
    return filename, job_info_list, formated_date

