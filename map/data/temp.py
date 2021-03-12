import pandas as pd
import datetime
import utils.display as display


if __name__ == '__main__':
    display.configure_pandas()
    print(datetime.datetime.now())
    trajectory = pd.read_csv('history_trajectories.csv', parse_dates=['timestamp'])
    print(datetime.datetime.now())
    print(trajectory)
    trajectory.iloc[:100000].to_csv('part_trajectories.csv', index=False)
