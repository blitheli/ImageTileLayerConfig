# -*- coding: utf-8 -*-
#   读取当前目录下moon_np图层信息，生成相应图层序号，并保存至tile_idx_np.xlsx中


import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import json

#运行前注意填写行星和图层类型

planet = 'Moon'  #月球为Moon，火星为Mars
service = 'NP'  #赤道为EQ，北极为NP，南极为SP


def extract_json_info():
    # 读取config.json文件
    json_path = folder_path + '/config.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)

    # 获取LayerID、BBOX和WMTS_Capabilities字段的值
    layer_id = config_data["LayerID"]
    bbox = config_data["BBOX"]
    layerid_parts = layer_id.split('_')
    pic_name = "_".join(layerid_parts[2:])

    return layer_id, pic_name, bbox

tile_idx = 1000020100

# 创建一个空的DataFrame对象
df = pd.DataFrame(columns=['Planet', 'Service', 'layer_id', 'tile_idx'])


# 获取当前目录
current_directory = os.getcwd()

# 获取当前目录下所有的子文件夹
subdirectories = [name for name in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, name))]

# 筛选出以 "Moon_XX" 开头的文件夹名称
folders = [name for name in subdirectories if name.startswith("Moon_np")]


# 遍历当前目录下的子文件夹
for folder in folders:
    folder_path = os.path.join(current_directory, folder)
    tile_type_file_path = os.path.join(folder_path, "0_TileType.txt")
    with open(tile_type_file_path, "r", encoding="utf-8") as file:
        tile_idx_file = file.read().strip()
    
    if tile_idx_file == '1000020100':
        tile_idx = tile_idx + 1 
        tile_idx_path = folder_path + '/0_TileType.txt' 
        with open(tile_idx_path, 'w', encoding="utf-8") as file:
            file.write(str(tile_idx))
        tile_idx_name = folder_path + '/' + str(tile_idx) + '.txt'
        with open(tile_idx_name, "w") as file:
            pass
        
        layer_id, pic_name, bbox = extract_json_info()
        data = [planet, service, layer_id, tile_idx]
        # 将数据添加到DataFrame
        df.loc[len(df)] = data
        
        print(f'{folder_path}序号已创建')
    else: 
        print(f'{folder_path}序号已编号')



# 保存DataFrame到Excel文件
df.to_excel('tile_idx_np.xlsx', index=False)
print("tile_idx数据已成功添加到文件！")

print('全部内容生成完毕')