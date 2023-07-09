# -*- coding: utf-8 -*-

import os
import json
import requests
from googletrans import Translator


#运行前注意填写行星和图层类型

planet = 'Moon'  #月球为Moon，火星为Mars
service = 'EQ'  #赤道为EQ，北极为NP，南极为SP



# 读取文本文件内容
info_path = 'info.txt'  # 指定文本文件的路径

with open(info_path, 'r') as file:
    info = file.read()

#定义翻译函数
def translate_text(text):
    if not text:
        return ''  # 如果文本为空，返回空字符串
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(text, src='auto', dest='zh-CN')
    return translation.text

def extract_info(string):
    lines = string.split('\n')  # 将字符串按行分割成列表
    title = lines[0]  # 第二行为title
    layer_id = None
    bbox = None
    wmts_endpoint = None
    abstract = None
    projection = None
    if service == "EQ":
        service_lower = 'eqc'
    else:
        service_lower = service.lower()

    for index, line in enumerate(lines):
        if line.startswith('Layer ID :'):
            layer_id_raw = line.split(':')[1].strip()  # 提取Layer ID后的内容，并去除首尾空格
            layer_id = planet + "_" + service_lower + "_" + layer_id_raw
        elif line.startswith('bbox :'):
            bbox_str = line.split(':')[1].strip().split(',')  # 提取bbox后的内容，并去除首尾空格
            bbox = [float(num) for num in bbox_str]
        elif line.startswith('WMTS Endpoint :'):
            start_index = line.index("WMTS Endpoint :") + len("WMTS Endpoint :")
            wmts_endpoint = line[start_index:].strip()

        elif line.startswith('Projection :'):
            projection_lines = lines[index + 1:]  # 获取"Projection"行后面的所有行
            projection = '\n'.join(projection_lines)  # 将这些行合并为一个字符串，每行之间用换行符分隔
            break
    
    title = None
    for i, line in enumerate(lines):
        if 'Layer ID :' in line:
            title = lines[i-1].strip()
            break
    
    abstract_index = info.find("Abstract")
    colon_index = info.find(":", abstract_index)
    abstract = info[colon_index+1:].split('\n', 1)[0]
    
    layerid_parts = layer_id.split('_')
    pic_name = "_".join(layerid_parts[2:])
    icon = "{MoonImage}\\" + layer_id + "\\" + pic_name + "-120.png"
    preview = "{MoonImage}\\" + layer_id + "\\index.html"
    wmts_capabilities =  "{MoonImage}\\" + layer_id + "\\WMTSCapabilities.xml"
    metadata = "{MoonImage}\\" + layer_id + "\\MetaData.html"
    folder_path = os.path.join(r'./', layer_id)
    
    abstract_cn = translate_text(abstract)
    
    return title, layer_id, bbox, wmts_endpoint, icon, abstract, preview, wmts_capabilities, metadata, projection, folder_path, abstract_cn, pic_name

title, layer_id, bbox, wmts_endpoint, icon, abstract, preview, wmts_capabilities, metadata, projection, folder_path, abstract_cn, pic_name = extract_info(info)
print("Title:", title)
print("Layer ID:", layer_id)
print("Icon:", icon)
print("bbox:", bbox)
print("WMTS Endpoint :", wmts_endpoint)
print("Abstract :", abstract)
print(abstract_cn)
print("preview :", preview)
print("wmts_capabilities :", wmts_capabilities)
print("metadata :", metadata)
print("Projection:", projection)

def generate_config_file(title, layer_id, bbox, projection, icon, abstract, preview, wmts_capabilities, metadata, folder_path):

    
    config = {
        "ProjectionType": "SP",
        "Title": title,
        "LayerID": layer_id,
        "Icon": icon,
        "BBOX": bbox,
        "Abstract": abstract_cn,
        "Projection": "urn:ogc:def:crs:IAU2000::30120",
        "Preview": preview,
        "WMTS_Capabilities": wmts_capabilities,
        "MetaData": metadata
    }
    
    file_path = os.path.join(folder_path, "config.json")  # 指定文件夹路径和文件名
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4,ensure_ascii=False)


wmts_url = 'https://trek.nasa.gov/tiles/' + planet + '/'+ service + '/' + pic_name + '/1.0.0/WMTSCapabilities.xml'
folder_path = './' + layer_id

# 使用os.mkdir()函数创建文件夹
if not os.path.exists(folder_path):
    # 使用os.makedirs()函数创建文件夹（如果不存在）
    os.makedirs(folder_path)
else:
    print("文件夹已经存在。")

# 生成 config.json 文件
generate_config_file(title, layer_id, bbox, projection, icon, abstract, preview, wmts_capabilities, metadata, folder_path)

#下载wtms文件

def download_wmts(url):
    response = requests.get(url, stream=True)
    file_name = url.split('/')[-1]  # 获取文件名
       
    save_file_path = os.path.join(folder_path, file_name)  # 拼接保存文件的完整路径

    with open(save_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    print(f"wmts文件已保存到：{save_file_path}")


download_wmts(wmts_url)


#下载pic文件
pic_url = 'https://trek.nasa.gov/tiles/' + planet + '/'+ service + '/' + pic_name + '/thumbnail/' + pic_name + '-120.png'

def download_pic(url):
    response = requests.get(url, stream=True)
    file_name = pic_name + '-120.png'  # 获取文件名
       
    save_file_path = os.path.join(folder_path, file_name)  # 拼接保存文件的完整路径

    with open(save_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    print(f"pic文件已保存到：{save_file_path}")


download_pic(pic_url)

#下载metadata文件

metadata_url = 'https://trek.nasa.gov/' + planet.lower() + '/TrekWS/rest/cat/metadata/fgdc/html?label=' + pic_name

def save_webpage(url):
    response = requests.get(url)
    save_file_path = folder_path + '/' + 'metadata.html'

    with open(save_file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)

    print(f"meta网页已保存到：{save_file_path}")

save_webpage(metadata_url)

#生成info文件
def write_to_info():
    layer_id_txt = "Layer ID:" + layer_id
    bbox_txt = "bbox:" + str(bbox)
    wmts_endpoint_txt = "WMTS Endpoint :" + wmts_endpoint
    abstract_txt = "Abstract :" + abstract
    projection_txt = "Projection:" + projection
    strings = [title, layer_id_txt, bbox_txt, wmts_endpoint_txt, abstract_txt, abstract_cn, projection_txt]
    
    save_file_path = folder_path + '/info.txt'
    
    with open(save_file_path, 'w') as file:
        for idx, string in enumerate(strings, start=1):
            file.write(string + '\n')
    print(f"info已保存到：{save_file_path}")
write_to_info()