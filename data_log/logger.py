import numpy as np
import pandas as pd
# Funcion para guardar datos de funcionamiento, considera tiempos de inicio y final, estado de sensores y valvulas


def add_status_log_entry(AAAA_MM_DD='2023-00-00',State = '', tiempo_inicio='', tiempo_actual='' , tiempo_termino='', valve0_status=False, valve1_status=False, sensor_caudal0_value=0.0, sensor_caudal1_value=0.0, sensormoist0_value=0.0, sensormoist1_value=0.0):
    # Check if the CSV file already exists
    try:
        # Read the existing CSV file
        datalog = pd.read_csv('log/invernadero_log_csv_{}.csv'.format(AAAA_MM_DD))
    except FileNotFoundError:
        # Create a new DataFrame if the file doesn't exist
        datalog = pd.DataFrame(columns=['State' ,'Initial Time', 'Tiempo Actual','Final Time', 'valve0_status',
                               'valve1_status', 'Sensor caudal 0', 'Sensor caudal 1', 'Sensor humedad 0', 'Sensor humedad 1'])

    # Create a new row with the status log entry
    new_entry = pd.DataFrame(
        [{'State': State, 'Initial Time': tiempo_inicio,'Tiempo Actual': tiempo_actual ,'Final Time': tiempo_termino, 'valve0_status': valve0_status, 'valve1_status': valve1_status, 'Sensor caudal 0': sensor_caudal0_value, 'Sensor caudal 1': sensor_caudal1_value,
          'Sensor humedad 0': sensormoist0_value, 'Sensor humedad 1': sensormoist1_value}])

    # Append the new row to the DataFrame
    datalog = pd.concat([datalog, new_entry], ignore_index=True)
    # Save the DataFrame to the CSV file
    datalog.to_csv('log/invernadero_log_csv_{}.csv'.format(AAAA_MM_DD), index=False)
    datalog.to_excel('log/invernadero_log_excel_{}.xlsx'.format(AAAA_MM_DD))


def get_tiempo_actual_csv(AAAA_MM_DD='2024-00-00'):
    try:
        # Read the existing CSV file
        log = pd.read_csv('log/invernadero_log_csv_{}.csv'.format(AAAA_MM_DD))
    except FileNotFoundError:
        # Create a new DataFrame if the file doesn't exist
        log = pd.DataFrame(columns=['State' ,'Initial Time', 'Tiempo Actual','Final Time', 'valve0_status',
                               'valve1_status', 'Sensor caudal 0', 'Sensor caudal 1', 'Sensor humedad 0', 'Sensor humedad 1'])
    
    
    last_tiempo_actual = log['Tiempo Actual'].iloc[-1]
    
    return last_tiempo_actual
