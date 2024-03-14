import json

# 定义两个空列表，分别用于存储两种格式的数据
data_list_for_converted = []
data_list_for_zytvbox = []

# 打开并读取maqu.txt文件
with open('maqu.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 遍历每一行，解析接口信息
for line in lines:
    # 分割行内容以获取资源网站名称和接口URL
    parts = line.strip().split(',')
    if len(parts) == 2:
        # 提取资源网名称和接口URL
        name = parts[0].strip()
        api_url = parts[1].strip().split('at/xml')[0] + '/at/xml'
        
        # 构建字典并添加到converted_data列表中
        data_dict_for_converted = {
            "key": name,
            "name": name,
            "api": api_url,
            "useInSearchAll": True
        }
        data_list_for_converted.append(data_dict_for_converted)
        
        # 构建字典并添加到zytvbox_data列表中
        data_dict_for_zytvbox = {
            "key": name,
            "name": name,
            "type": 1,
            "api": api_url,
            "searchable": 1,
            "recordable": 0
        }
        data_list_for_zytvbox.append(data_dict_for_zytvbox)

# 将两种格式的数据列表分别转换为JSON格式的字符串
json_data_converted = json.dumps(data_list_for_converted, ensure_ascii=False, indent=4)
json_data_zytvbox = json.dumps(data_list_for_zytvbox, ensure_ascii=False, indent=4)

# 将两种格式的JSON数据分别写入到新的文件中
with open('zyvying.json', 'w', encoding='utf-8') as json_file_converted:
    json_file_converted.write(json_data_converted)

with open('zytvbox.json', 'w', encoding='utf-8') as json_file_zytvbox:
    json_file_zytvbox.write(json_data_zytvbox)

print("转换完成，数据已保存到zyvying.json和zytvbox.json文件中。")
file_path = 'maqu.txt'

if os.path.exists(file_path):
    os.remove(file_path)
    print('maqu.txt已删除')
else:
    print('maqu.txt不存在')
