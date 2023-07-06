#   读取当前目录下所有文件夹内的config.json文件，生成特定的json对象（放在Layers数组中），并保存为文件
#   2023-06-20  liyunfei
#
import os
import json
import datetime

def read_config():

    config_data = {"Description":"本文件存储了瓦片服务器发布的相关图层信息",
                   "version":"1.0.0",
                   "Author":"liyunfei",
                   "CreateTime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   "Layers": []}
    
    # 循环每个文件夹 
    for root, dirs, files in os.walk(".", topdown=True):
        
        # 只处理Moon目录下的文件
        if not root.startswith(".\\Moon"):
            continue

        try:
            # 循环每个文件
            for name in files:
                if name == "config.json":
                    file_path = os.path.join(root, name)
                    with open(file_path, "r", encoding='utf-8') as config_file:
                        config_data['Layers'].append(json.load(config_file))
        except Exception as e:
            print("root: ", root)
            print("FileName: "+ name)
            print("Error: ", e)

    return config_data

jsonConfig = read_config()
with open("MoonLayerConfig.json", "w", encoding='utf-8') as file:
    json.dump(jsonConfig, file, indent=4, ensure_ascii=False) # 保证中文不乱码

print("----------end----------")