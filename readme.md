本项目为 “瓦片服务器”发布的影像 创建Config文件，便于网站调用，显示所有图层信息

### 所有图层文件夹均来自于“瓦片服务器”中的“自定义图源”内文件夹
### 大部分图层来源于：https://trek.nasa.gov/tiles/apidoc/trekAPI.html?body=moon
### 在每个图层文件内部
- info.txt              为图层的描述信息，自己添加，以供参考
- index.html            为图层的预览文件(手动或自动生成)
- WMTSCapabilities.xml  为图层的WMTS能力文件
- **.png                为图层的预览图
- metadata.html         为图层的元数据文件


## 通过调用createMoonConfig.py、createMarsConfig.py，自动生成 配置文件, 里面为每个图层的元数据信息描述，供网站调用
- MoonLayerConfig.json
- MarsLayerConfig.json


## 运行
- 将此文件夹通过IIS或其他服务器发布即可，客户端直接调用 **Config.json 即可！


## 数据来源
- 大部分图层文件夹来源于“红豆地球”生成的“自定义图源”内文件夹
- 新增一个数据源后，从“红豆地球”-“自定义图源”内拷贝出到此处
- 然后在文件夹内添加额外信息，如：index.html、metadata.html、**.png、WMTSCapabilities.xml
- 其中index.html需要独立测试下，是否能正常显示！右键"open with live server"，自动启动浏览器，如果能正常显示，就可以了！    


 ## 数据下载
- 在moontrek网站下载月球南北极数据时，需下载原始tif数据，发布成arcgis服务，再使用切片下载工具下载
- 下载网址格式https://trek.nasa.gov/moon/TrekWS/rest/cat/data/stream?label=[layerID]
- 其中[layerID]为moonterk中的layer_ID


20230614    初次编写
20230621    增加了自动生成配置文件的功能
20230703    增加了月球北极和南极的图层