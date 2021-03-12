import json
import pandas as pd
from pandas import Timestamp
from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from map.backend import data_loader



# Create your views here.

trajectory = pd.read_csv('map/data/part_trajectories.csv', parse_dates=['timestamp'])
ce = pd.read_csv('map/data/ce_v3.csv', parse_dates=['begin_time', 'end_time', 'charging_duration'])

def index(request):
    print(request)
    # Select trajectory of requested license
    if 'plate' not in request.GET:
        plate = trajectory.at[0, 'plate']
    else:
        plate = request.GET['plate']
    begin = trajectory['plate'].searchsorted(plate)
    end = trajectory['plate'].searchsorted(plate, side='right')
    license_trajectory = trajectory.iloc[begin: end]
    # Load charging station info
    cs_info = data_loader.cs_info()
    # Select ce of requested license
    license_ce = ce.loc[ce['licence'] == plate]
    content = {'cs_info': cs_info, 'licenses': trajectory['plate'].unique(), 'license': plate,
               'trajectory': license_trajectory.to_dict(orient='records'), 'ce': license_ce.to_dict(orient='records')}
    return render(request, 'map/map.html', content)


def ce_trajectory_data(request):
    print(request.GET)
    plate = request.GET['license']
    ce_index = int(request.GET['index'])
    # Select trajectory of requested license

    begin = trajectory['plate'].searchsorted(plate)
    end = trajectory['plate'].searchsorted(plate, side='right')
    license_trajectory = trajectory.iloc[begin: end]

    licence_ce = ce.loc[ce['licence'] == plate]

    begin_time = licence_ce.at[licence_ce.index[ce_index], 'begin_time']
    end_time = licence_ce.at[licence_ce.index[ce_index], 'end_time']

    trajectory_begin = license_trajectory['timestamp'].searchsorted(begin_time)
    trajectory_end = license_trajectory['timestamp'].searchsorted(end_time, side='right')

    trajectory_begin = 0 if trajectory_begin - 7 < 0 else trajectory_begin - 7
    ce_trajectory = license_trajectory.iloc[trajectory_begin: trajectory_end + 30]
    ce_trajectory.reset_index(inplace=True, drop=False)
    ce_trajectory = ce_trajectory.to_dict(orient='records')
    print(ce_trajectory)
    ce_trajectory = json.dumps(ce_trajectory, cls=DjangoJSONEncoder, ensure_ascii=False)
    return HttpResponse(ce_trajectory)
