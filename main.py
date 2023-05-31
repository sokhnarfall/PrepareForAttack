import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from shapely.geometry import Point, Polygon
from scipy.interpolate import griddata
import numpy as np


class ProcessGameState:
    # read the inputted pickle file into a pandas DataFrame
    def __init__(self, file_path):
        self.df = pd.read_pickle(file_path) 

    def in_boundary(self, boundary_coordinates):
        boundary_polygon = Polygon(boundary_coordinates)
        # iterate through each row in the DataFrame to check if the point is within the boundary
        return self.df.apply(lambda row: Point(row['x'], row['y']).within(boundary_polygon), axis=1)

    def extract_weapon_classes(self):
        weapon_classes = []
        # 
        for index, row in self.df.iterrows():
            inventory = row['inventory']
            print(inventory)
            # if inventory is not empty and key 'weapon_class' exists, store this key's value in a 
            # list and return the list once iteration is complete
            if inventory is not None:
                classes = [item['weapon_class'] for item in inventory if 'weapon_class' in item]
                weapon_classes.append(classes)
            else:
                weapon_classes.append([])
        return weapon_classes


    def generate_heatmap(self, area_name, resolution=100): # creates a heatmap of the CT side in a specific area
        # filter through DataFrame and select rows where the team is 'Team2', side is 'CT', and 
        # the area name matches the provided area_name
        team2_ct_in_bombsiteb = self.df[(self.df['team'] == 'Team2') & (self.df['side'] == 'CT') & (self.df['area_name'] == area_name)]
        # create a grid of x and y values based on coordinates in filtered DataFrame
        x = np.linspace(team2_ct_in_bombsiteb['x'].min(), team2_ct_in_bombsiteb['x'].max(), resolution)
        y = np.linspace(team2_ct_in_bombsiteb['y'].min(), team2_ct_in_bombsiteb['y'].max(), resolution)
        grid_x, grid_y = np.meshgrid(x, y)
        values = np.ones(len(team2_ct_in_bombsiteb))
        grid_z = griddata((team2_ct_in_bombsiteb['x'], team2_ct_in_bombsiteb['y']), values, (grid_x, grid_y), method='cubic')
        plt.figure(figsize=(10, 8))
        sns.heatmap(grid_z, cmap='coolwarm')
        plt.title(f"Heatmap of Team2 CT side in {area_name}")
        plt.show()

pgs = ProcessGameState('game_state_frame_data.pickle')

if "BombsiteB" in pgs.df[pgs.df['team'] == 'Team2']['area_name'].unique():
    print("'BombsiteB' is present in the 'area_name' column for Team2.")
else:
    print("'BombsiteB' is not present in the 'area_name' column for Team2.")

boundary_coordinates = [[-1735, 250], [-2024, 398], [-2806, 742], [-2472, 1233], [-1565, 580]]
pgs.df['in_boundary'] = pgs.in_boundary(boundary_coordinates)

team2_t_in_boundary = pgs.df[(pgs.df['team'] == 'Team2') & (pgs.df['side'] == 'T') & pgs.df['in_boundary']]

if len(pgs.df) != 0:
    print(f"Percentage of Team2 T side entering via light blue boundary: {len(team2_t_in_boundary) / len(pgs.df) * 100}%")
else:
    print("No data to process.")

# add weapon_classes column to the DataFrame
pgs.df['weapon_classes'] = pgs.extract_weapon_classes()

# filter DataFrame to select rows where the team is 'Team2', the side is 'T', the area name is 'BombsiteB', 
# and the number of rifles/SMGs in the weapon classes is at least 2
team2_t_with_rifles_or_smgs = pgs.df[
    (pgs.df['team'] == 'Team2') & 
    (pgs.df['side'] == 'T') & 
    (pgs.df['area_name'] == 'BombsiteB') & 
    (pgs.df['weapon_classes'].apply(lambda x: x.count('rifle') + x.count('smg') >= 2))
]

if not team2_t_with_rifles_or_smgs.empty:
    average_timer = team2_t_with_rifles_or_smgs['clock_time'].mean()
    print(f"Average clock_time that Team2 on T side enters BombsiteB with at least 2 rifles or SMGs: {average_timer}")
else:
    print("No data to process for Team2 on T side with at least 2 rifles or SMGs in BombsiteB.")

pgs.generate_heatmap('BombsiteB')
