import pyodbc
import os
import csv

query = """
SELECT 
    summary_facility.cwns_number, 
    summary_facility.facility_name, 
    summary_facility.facility_state,
    val(summary_facility.latitude) as latitude,
    val(summary_facility.longitude)*-1 as longitude,
    summary_facility.location_description, 
    summary_effluent.pres_effluent_treatment_level, 
    summary_effluent.pres_disinfection as disinfection,
    summary_permit.permit_type,
    summary_permit.permit,
    summary_discharge.discharge_method,
    summary_population.pres_res_total_receivng_trmt as population,
    summary_flow.exist_total AS flow_mgd
FROM ((((summary_facility INNER JOIN summary_flow ON summary_facility.cwns_number = summary_flow.cwns_number) 
INNER JOIN summary_effluent ON summary_facility.cwns_number = summary_effluent.cwns_number) 
INNER JOIN summary_population ON summary_facility.cwns_number = summary_population.cwns_number)
INNER JOIN summary_permit on summary_facility.cwns_number = summary_permit.cwns_number)
INNER JOIN summary_discharge on summary_facility.cwns_number = summary_discharge.cwns_number
WHERE summary_facility.latitude<>'';
"""

conn = pyodbc.connect(
            r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ='+os.getcwd()+r'\HQ.mdb;'
            )
cursor = conn.cursor()
cursor.execute(query)

with open('1-cwns.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([i[0] for i in cursor.description])  # heading row
    writer.writerows(cursor.fetchall())

