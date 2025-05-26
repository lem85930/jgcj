import json
import os
import itertools

# 定义四个空列表，分别用于存储不同格式的数据
data_list_for_converted = []
data_list_for_zytvbox = []
data_list_for_ysdqbox = []
data_list_for_zypcbox = []

# 初始化数字递增生成器（从1开始）
id_counter = itertools.count(1)

# 读取maqu.txt文件
with open('maqu.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 处理每一行数据
for line in lines:
    try:
        parts = line.strip().split(',')
        if len(parts) == 2:
            name = parts[0].strip()
            api_url = parts[1].strip().split('at/xml')[0]

            # 构建其他数据格式的字典（保持不变）
            data_list_for_converted.append({
                "key": name,
                "name": name,
                "api": api_url + 'at/xml',
                "useInSearchAll": True
            })
            
            data_list_for_zytvbox.append({
                "key": name,
                "name": name,
                "type": 1,
                "api": api_url,
                "searchable": 1,
                "recordable": 0
            })
            
            data_list_for_ysdqbox.append({
                "type": "",
                "sourceName": name,
                "baseUrl": "",
                "apiUrl": api_url + 'at/xml',
                "searchUrl": "",
                "detailUrl": "",
                "parserUrl": ""
            })
            
            # 构建新的zypc_data格式（包含自增ID）
            data_list_for_zypcbox.append({
                "key": name,
                "name": name,
                "api": api_url + 'at/xml',
                "playUrl": "",
                "search": 1,
                "group": "切片",
                "status": True,
                "type": 0,
                "id": str(next(id_counter)),  # 自增ID
                "isActive": True,
                "resource": "",
                "download": ""
            })
    except ValueError:
        print(f"格式错误行：{line}")

# 生成最终的JSON结构（关键修改点）
final_zypcbox_data = {
    "tbl_site": data_list_for_zypcbox  # 将列表包装在tbl_site键下
}

# 转换为JSON字符串
json_data_converted = json.dumps(data_list_for_converted, ensure_ascii=False, indent=4)
json_data_zytvbox = json.dumps(data_list_for_zytvbox, ensure_ascii=False, indent=4)
json_data_ysdqbox = json.dumps(data_list_for_ysdqbox, ensure_ascii=False, indent=4)
json_data_zypcbox = json.dumps(final_zypcbox_data, ensure_ascii=False, indent=4)  # 使用新结构

# 写入文件
with open('zyvying.json', 'w', encoding='utf-8') as f:
    f.write(json_data_converted)

with open('zytvbox.json', 'w', encoding='utf-8') as f:
    f.write(json_data_zytvbox)
    
with open('ysdqbox.json', 'w', encoding='utf-8') as f:
    f.write(json_data_ysdqbox)
    
with open('zypcbox.json', 'w', encoding='utf-8') as f:  # 关键修改点
    f.write(json_data_zypcbox)

print("转换完成，数据已保存到指定文件中。")

# 可选：删除临时文件
# if os.path.exists('maqu.txt'):
#     os.remove('maqu.txt')
