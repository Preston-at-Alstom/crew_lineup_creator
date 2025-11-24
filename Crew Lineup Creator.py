import streamlit as st
import backend
import format_report


st.set_page_config(
    page_title="Crew Lineup Creator",
    layout="wide",)

st.header('Crew Lineup Creator')


with st.form("my_form"):
   lineup_upload = st.file_uploader('Upload OMS tour file (tblTourOfDuty........xlsx)', type='xlsx')
   special_package = st.file_uploader('Upload Special Package (baseline package used if left blank)', type='pdf')
   
   st.form_submit_button('Create Crew Line-up')

if lineup_upload is not None:
 
   filename, job_info_list, formated_date = backend.create_lineup(lineup_upload, special_package)

   format_report.format(filename, job_info_list, formated_date)


   with open(filename, 'rb') as file:
        st.download_button(label = 'Download Line-up',
                    data = file, 
                    file_name = filename, 
                    mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',


                    )