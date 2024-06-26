import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import numpy as np
import csv
import os
import math
from tqdm import tqdm
import gc

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def read_csv(file_path):
    csv_data = []

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    del(csv_data[0])

    def convert_row(row):
        if row[0]=='True':IsCrashed = True
        else : IsCrashed = False
        return [IsCrashed] + [float(value) for value in row[1:]]
    csv_data = [convert_row(row) for row in csv_data]

    return (csv_data)

def calculate_yaw(path):
    yaw_angles = []
    for i in range(len(path) - 1):
        dx = path[i + 1][0] - path[i][0]
        dy = path[i + 1][1] - path[i][1]
        yaw = math.atan2(dy, dx)
        yaw_angles.append(yaw)
    yaw_angles.append(yaw_angles[-1])  # 마지막 yaw 값은 이전 값으로 동일하게 설정
    return np.array(yaw_angles)

def plot_figure(csv_data,figure_name):
    w=16
    h=5
    fig, ax = plt.subplots(figsize=(w, h))

    fig.patch.set_edgecolor('black')
    fig.patch.set_linewidth(50)  # 테두리 두께 설정

#-----------------------------------------------------------------------------------------------------------------------------
    # 자동차 경로 그리기 (빨간색, 파란색, 녹색)   . csv파일 읽어오기. 정규화 진행하기(0~1)

    
    x_sacle = (170) / (csv_data[-1][11])
    x_shift = (-14.5) - (csv_data[0][6] * x_sacle)

    if(csv_data[0][7] > 0) :
        y_sacle = (21.5) / (csv_data[0][7]+3)
    else :
        y_sacle = (21.5) / (csv_data[0][7]+3)

    for row in csv_data:
        for i in [1,6,11]:
            if i < len(row):  # 행의 길이를 벗어나지 않는지 확인
                row[i] = row[i]*x_sacle + x_shift

        for i in [2,7,12]:
            if i < len(row):  # 행의 길이를 벗어나지 않는지 확인
                row[i] += 3
                row[i] = row[i]*y_sacle

    

    blue_path = np.array([[row[1], row[2]] for row in csv_data])
    red_path = np.array([[row[6], row[7]] for row in csv_data])
    green_path = np.array([[row[11], row[12]] for row in csv_data])


#-----------------------------------------------------------------------------------------------------------------------------
    red_yaws = calculate_yaw(blue_path)
    blue_yaws = calculate_yaw(red_path)
    green_yaws = calculate_yaw(green_path)

    # 자동차 그리기 함수 (orientation 포함)
    def draw_car(ax, position, yaw, color, linestyle = '-', alpha=0.5):
        scale = 2.5
        car_width, car_height = 4 * scale, 2.8 * scale
        car_zorder = 4
        
        # 변환 설정
        t = transforms.Affine2D().rotate_around(position[0], position[1], yaw) + ax.transData
        car = patches.Rectangle((position[0] - car_width / 2, position[1] - car_height / 2), 
                                car_width, car_height, linewidth=2.5, linestyle=linestyle, alpha=alpha, color=color, zorder=car_zorder,
                                transform=t)
        
        ax.add_patch(car)
        ax.plot(position[0], position[1], 'o', color=color, markersize=8, zorder=car_zorder)


    #collision index
    Collision_indexs = []
    for i, row in enumerate(csv_data):
        if row[0] == True:
            Collision_indexs.append(i)

    if len(Collision_indexs)==0 :
        path_line_width = 2.5
        path_line_zorder = 3
        ax.plot(blue_path[:, 0], blue_path[:, 1], 'b-', linewidth=path_line_width, zorder=path_line_zorder)
        ax.plot(red_path[:, 0], red_path[:, 1], 'r-', linewidth=path_line_width, zorder=path_line_zorder)
        ax.plot(green_path[:, 0], green_path[:, 1], 'g-', linewidth=path_line_width, zorder=path_line_zorder)
        #############################
        num_of_marker = 8
        marker_frequency = int( len(csv_data)/num_of_marker )

        for i in range(0, len(green_path)):
            if(i == 0) or (i % marker_frequency == 0): draw_car(ax, green_path[i], green_yaws[i], 'green')
        for i in range(0, len(blue_path)):
            if(i == 0) or (i % marker_frequency == 0): draw_car(ax, blue_path[i], red_yaws[i], 'blue')
        for i in range(0, len(red_path)):
            if(i == 0) or (i % marker_frequency == 0): draw_car(ax, red_path[i], blue_yaws[i], 'red')

    else :
        C_index = min(Collision_indexs)
        #############################
        path_line_width = 2.5
        path_line_zorder = 3

        blue_path_before_coll = blue_path[:C_index]
        blue_path_after_coll = blue_path[C_index:]
        ax.plot(blue_path_before_coll[:, 0], blue_path_before_coll[:, 1], 'b-', linewidth=path_line_width, zorder=path_line_zorder)
        ax.plot(blue_path_after_coll[:, 0], blue_path_after_coll[:, 1], 'b', linewidth=path_line_width, linestyle="--", zorder=path_line_zorder)


        red_path_before_coll = red_path[:C_index]
        red_path_after_coll = red_path[C_index:] 
        ax.plot(red_path_before_coll[:, 0], red_path_before_coll[:, 1], 'r-', linewidth=path_line_width, zorder=path_line_zorder)
        ax.plot(red_path_after_coll[:, 0], red_path_after_coll[:, 1], 'r', linewidth=path_line_width, linestyle="--", zorder=path_line_zorder)


        green_path_before_coll = green_path[:C_index]
        green_path_after_coll = green_path[C_index:]       
        ax.plot(green_path_before_coll[:, 0], green_path_before_coll[:, 1], 'g-', linewidth=path_line_width, zorder=path_line_zorder)
        ax.plot(green_path_after_coll[:, 0], green_path_after_coll[:, 1], 'g', linewidth=path_line_width, linestyle="--", zorder=path_line_zorder)

        #############################
        num_of_marker_before_coll = 5
        marker_frequency_before_coll = int( C_index / num_of_marker_before_coll )
        
        num_of_marker_after_coll = 3
        marker_frequency_after_coll = int( (len(csv_data)-C_index) / num_of_marker_after_coll )


        for i in range(0, C_index):
            if(i == 0) or (i == C_index) or (i % marker_frequency_before_coll == 0): draw_car(ax, green_path[i], green_yaws[i], 'green')
        for i in range(C_index, len(green_path)):
            if(i != C_index) and (i % marker_frequency_after_coll == 0): draw_car(ax, green_path[i], green_yaws[i], 'green', linestyle = '--', alpha=0.45)


        for i in range(0, C_index+1):
            if(i == 0) or (i == C_index) or (i % marker_frequency_before_coll == 0): draw_car(ax, blue_path[i], red_yaws[i], 'blue')
        for i in range(C_index, len(blue_path)):
            if(i != C_index) and (i % marker_frequency_after_coll == 0): draw_car(ax, blue_path[i], red_yaws[i], 'blue', linestyle = '--', alpha=0.45)


        for i in range(0, C_index+1):
            if(i == 0) or (i == C_index) or (i % marker_frequency_before_coll == 0): draw_car(ax, red_path[i], blue_yaws[i], 'red')
        for i in range(C_index, len(red_path)):
            if(i != C_index) and (i % marker_frequency_after_coll == 0): draw_car(ax, red_path[i], blue_yaws[i], 'red', linestyle = '--', alpha=0.45)


        collision_point = [(csv_data[C_index][1] + csv_data[C_index][6])/2,
                        (csv_data[C_index][2] + csv_data[C_index][7])/2]

        collision_maker_zorder = 5
        ax.plot(collision_point[0], collision_point[1], '*', color='black', markersize=30, zorder=collision_maker_zorder)
        ax.plot(collision_point[0], collision_point[1], '*', color='orange', markersize=20, zorder=collision_maker_zorder)
#-----------------------------------------------------------------------------------------------------------------------------
   # 도로 배경 그리기
    road = patches.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color='lightgrey')
    ax.add_patch(road)
    white_line_width = 6
    white_line_zorder = 1
    line = ax.axhline(y=-12.5, color='white', linestyle='dashed', linewidth=white_line_width, zorder=white_line_zorder)
    line.set_dashes([5, 4.1])  # [선의 길이, 간격]
    line = ax.axhline(y=12.5, color='white', linestyle='dashed', linewidth=white_line_width, zorder=white_line_zorder)
    line.set_dashes([5, 4.1])  # [선의 길이, 간격]

#-----------------------------------------------------------------------------------------------------------------------------
    ax.set_xlim(-20, 180)
    ax.set_ylim(-30, 30)
    ax.set_aspect('auto')
    plt.axis('off')
    
    plt.savefig(figure_name, bbox_inches='tight', pad_inches=0.04)
    plt.close('all')


directory_list = ['Case1(curved_motion)', 'Case2(linear_motion)', 'Case3(POMDP)', 'Case4(without_ROIreward)', 'Case5(original)']
sub_directory_list = ['left_behind', 'right_behind']
status_directory_list = ['collision', 'fail', 'ROI_collision']

gc.collect()

for D in directory_list:
    for SD in sub_directory_list:
        for SSD in status_directory_list:
            try:
                directory = os.path.join(D,SD,SSD)

                csv_files = []
                for filename in os.listdir(directory):
                    if filename.endswith(".csv"):
                        csv_files.append(filename)

                for file in csv_files:
                    csv_path = os.path.join(directory, file)
                    csv_data =  read_csv(csv_path)

                    path_parts = os.path.normpath(csv_path).split(os.sep)

                    image_directory = os.path.join('selected_figure', path_parts[0])
                    create_folder_if_not_exists(image_directory)

                    
                    image_name = f"{SD}_{SSD}_{path_parts[-1][:-4]}.png"
                    image_path = os.path.join(image_directory, image_name)

                    plot_figure(csv_data, image_path)
            except:
                continue