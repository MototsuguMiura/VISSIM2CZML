import os
import pandas as pd
import json
from datetime import datetime, timedelta


def convert_to_czml(input_file, output_file, start_date, sim_time=0):
    # Check if vehicle or pedestrian trajectory, then read
    if 'fzp' in input_file:
        vfile = True
    elif 'pp' in input_file:
        vfile = False
    else:
        raise AssertionError('有効なファイル形式ではありません')
    df = pd.read_csv(input_file, header=18, delimiter = ';') # this number depends on the file

    # Create Header information
    czml = [{
        "id": "document",
        "version": "1.0",
        "name": "Vissim Trajectory",
        "clock": {
            "interval": f"{start_date.isoformat()}Z/{start_date.isoformat()}Z",
            "currentTime": start_date.isoformat() + "Z", #initial time of animation
            "multiplier": 5, #animation speed
        }
    }]

    # Generate vehicle/pedestrian trajectory information
    actor_positions = {}
    #cartographic_degrees = []
    max_timestep = 0.0
    for i in range(df.shape[0]):
        actor_id = df.iloc[i]['NO']
        actor_type = df.iloc[i]['VEHTYPE'] if vfile else df.iloc[i]['PEDTYPE']
        timestep = float(df.iloc[i]['$VEHICLE:SIMSEC']) if vfile else float(df.iloc[i]['$PEDESTRIAN:SIMSEC'])
        if timestep > max_timestep:
            max_timestep = timestep
        if actor_id not in actor_positions:
            actor_positions[actor_id] = {
                "id": actor_id,
                "name": actor_id,
                "description": "1",
                "point": {
                    "color": get_color_size(actor_type, vfile)[0],
                    "pixelSize": get_color_size(actor_type, vfile)[1],
                    "outlineWidth": 2,
                },
                "position": {
                    "epoch": start_date.isoformat() + 'Z',
                    "cartographicDegrees": []
                }

            }

        # Set the z value based on the presence of the 'z' column in the CSV
        if 'COORDFRONTZ' in df.columns:
            actor_positions[actor_id]['position']['cartographicDegrees'].extend(
                [float(df.iloc[i]['$VEHICLE:SIMSEC']), float(df.iloc[i]['LONGITUDEFRONT']), float(df.iloc[i]['LATITUDEFRONT']), float(df.iloc[i]['COORDFRONTZ'])]
                if vfile else [float(df.iloc[i]['$PEDESTRIAN:SIMSEC']), float(df.iloc[i]['LONGITUDE']), float(df.iloc[i]['LATITUDE']), float(df.iloc[i]['COORDCENTERZ'])])
        else:
            actor_positions[actor_id]['position']['cartographicDegrees'].extend(
                [float(df.iloc[i]['$VEHICLE:SIMSEC']), float(df.iloc[i]['LONGITUDEFRONT']), float(df.iloc[i]['LATITUDEFRONT']), 0]
                if vfile else [float(df.iloc[i]['$PEDESTRIAN:SIMSEC']), float(df.iloc[i]['LONGITUDE']), float(df.iloc[i]['LATITUDE']), 100])

    # Update the end time of the interval to the maximum timestep value
    end_date = start_date + timedelta(seconds=sim_time if sim_time != 0 else max_timestep)
    czml[0]['clock']['interval'] = f"{start_date.isoformat()}Z/{end_date.isoformat()}Z"

    czml.extend(actor_positions.values())

    with open(output_file, 'w') as output_czml:
        json.dump(czml, output_czml, indent=1)


def get_color_size(actor_type, vfile):
    # for vehicle type
    if vfile:
        if 100 <= actor_type < 200: #Car
            return {"rgba": [0, 255, 255, 255]}, 10 #Light blue
        elif actor_type < 300: #HGV
            return {"rgba": [0, 0, 255, 255]}, 15 #Blue
        elif actor_type < 400: #Bus
            return {"rgba": [0, 255, 0, 255]}, 15 #Green
        elif actor_type < 500: #Trum
            return {"rgba": [255, 255, 0, 255]}, 15 #Yellow
        elif actor_type < 600: #Pedestrian
            return {"rgba": [255, 0, 255, 255]}, 3 #Purple
        elif actor_type < 700: #Bike
            return {"rgba": [255, 106, 0, 255]}, 5  #Orange
        else:
            return {"rgba": [255, 255, 255, 255]}, 10 #white

    # for pedestrian type
    else:
        if 100 <= actor_type < 200: #Man
            return {"rgba": [0, 0, 255, 255]}, 3 #Blue
        elif actor_type < 300: #Woman
            return {"rgba": [255, 0, 0, 255]}, 3 #Red
        elif actor_type < 400: #Wheelchair
            return {"rgba": [0, 0, 0, 255]}, 5 #Black
        else:
            return {"rgba": [255, 255, 255, 255]}, 3 #white

if __name__ == '__main__':
    # Start time of the simulation
    start_date = datetime(2023, 11, 17, 12, 0, 0)
    sim_time = 0 # 0: automatically set simulation duration by trajectory data

    # Read simulation date and time from att file (option)
    if 0: #1：use this functionality、0：do not use
        df = pd.read_csv('input/Nishi-shinjuku_Simulation Runs.att', header=19, delimiter = ';')
        date = df.iloc[0]['STARTDATE'].split('.')
        time = df.iloc[0]['STARTTM'].split(':')
        start_date = datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]), int(time[2]))
        sim_time = df.iloc[0]['SIMEND']

    # convert all fzp/pp files in input directory
    read_files = os.listdir('input')
    for file in read_files:
        base, ext = os.path.splitext(file)
        if ext == '.fzp' or ext == '.pp':
            convert_to_czml(f'input/{file}',f'output/{file}.czml', start_date - timedelta(hours=9), sim_time) #Tize zone is based on GMT