# -*- coding: utf-8 -*-
#   遍历sp文件夹，生成index.html文件


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

# Python实现unproject方法
def unproject(x, y):
    lon = x * 90.0 / (2727718) #月球直径1,737,400m
    lat = y * 90.0 / (2727718)
    return [lon, lat]

# Python实现unprojectToDegreesBounds方法
def unprojectToDegreesBounds(bounds):
    mins = unproject(bounds[0], bounds[1])
    maxs = unproject(bounds[2], bounds[3])
    #return [toDegrees(mins[0]), toDegrees(mins[1]), toDegrees(maxs[0]), toDegrees(maxs[1])]
    return [mins[0],mins[1], maxs[0], maxs[1]]

#获取wmts中地图层数
def count_tile_matrices(xml_file):
    #with open(xml_file, 'r', encoding='utf-8') as file:
    #    xml = file.read()
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    tile_matrix_count = 0
    for element in root.iter('{http://www.opengis.net/wmts/1.0}TileMatrix'):
        tile_matrix_count += 1
    
    return tile_matrix_count

# 生成index文件
def write_index():
    
    bbox_west = str(bbox[0])
    bbox_east = str(bbox[2])
    bbox_south = str(bbox[1])
    bbox_north = str(bbox[3])

    bbox_lon_0 = (bbox[0] + bbox[2])/2
    bbox_lat_0 = (bbox[1] + bbox[3])/2

    bbox_lon = str(round(bbox_lon_0, 2))
    bbox_lat = str(round(bbox_lat_0, 2))

    wmts_path = folder_path + '/' + 'WMTSCapabilities.xml'
    wmts_count_0 = count_tile_matrices(wmts_path)
    wmts_count = str(wmts_count_0)

    minZoom = str(wmts_count_0 // 2)

    with open('index.html', 'r', encoding='utf-8') as file:
        index_0 = file.read()
    replaced_xml = index_0.replace("{tile_idx}", tile_idx_file)
    replaced_xml = replaced_xml.replace("{layer_id}", layer_id)
    replaced_xml = replaced_xml.replace("{bbox_west}", bbox_west)
    replaced_xml = replaced_xml.replace("{bbox_east}", bbox_east)
    replaced_xml = replaced_xml.replace("{bbox_south}", bbox_south)
    replaced_xml = replaced_xml.replace("{bbox_north}", bbox_north)
    replaced_xml = replaced_xml.replace("{bbox_lon}", bbox_lon)
    replaced_xml = replaced_xml.replace("{bbox_lat}", bbox_lat)
    replaced_xml = replaced_xml.replace("{minZoom}", minZoom)
    replaced_xml = replaced_xml.replace("{maxZoom}", wmts_count)

    index_path = folder_path + '/' + 'index.html'
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(replaced_xml)

    print(f"index.html已保存到：{index_path}")


# 获取当前目录
current_directory = os.getcwd()

# 获取当前目录下所有的子文件夹
subdirectories = [name for name in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, name))]

# 筛选出以 "Moon_XX" 开头的文件夹名称
folders = [name for name in subdirectories if name.startswith("Moon_np")]


# 遍历当前目录下的子文件夹
for folder in folders:
    folder_path = os.path.join(current_directory, folder)
    if "index.html" not in os.listdir(folder_path):
        tile_type_file_path = os.path.join(folder_path, "0_TileType.txt")
        with open(tile_type_file_path, "r", encoding="utf-8") as file:
            tile_idx_file = file.read().strip()
        
        layer_id, pic_name, bbox = extract_json_info()
        if service == 'SP' or service == 'NP':      #如果是南北极图层，修改bbox单位为degree
            bbox = unprojectToDegreesBounds(bbox)
        write_index()


        print(f'{folder_path}index文件已生成')




print('全部内容生成完毕')