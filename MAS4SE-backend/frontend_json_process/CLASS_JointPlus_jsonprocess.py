import json
import re


def format_role_name(role: str) -> str:
    """
    表达式非法会导致文本加载出错
    所以需要把非法字符串解析
    """
    illegal_characters_pattern = re.compile(
        r'[<>:"/\\|?：*]'
    )  # 定义一个正则表达式，用于匹配非法字符
    sanitized_role = illegal_characters_pattern.sub(
        "", role
    )  # 使用正则表达式替换掉所有非法字符
    sanitized_role = sanitized_role.replace(" ", "_")  # 将空格替换为下划线
    if not sanitized_role:  # 检查字符串是否为空
        raise ValueError("目录名不能为空。")
    if len(sanitized_role) > 255:  # 检查字符串是否过长
        raise ValueError("目录名过长。目录名长度不能超过255个字符。")
    return sanitized_role


def extract_data_to_simplified_json(input_data):
    import datetime

    result = {"Message": [], "Link": []}
    id_to_label = {}  # 创建一个 id 到 label_text 的映射
    for cell in input_data["cells"]:
        if cell["type"] == "app.FlowchartStart":
            label_text = cell["attrs"]["label"]["text"]
            label_text = format_role_name(label_text)
            result["Message"].append(
                {
                    "label_text": label_text,
                    "description_text": "FlowchartStart",
                    "id": cell["id"],
                }
            )
            id_to_label[cell["id"]] = label_text
        elif cell["type"] == "app.FlowchartEnd":
            label_text = cell["attrs"]["label"]["text"]
            label_text = format_role_name(label_text)
            result["Message"].append(
                {
                    "label_text": label_text,
                    "description_text": "FlowchartEnd",
                    "id": cell["id"],
                }
            )
            id_to_label[cell["id"]] = label_text
        elif cell["type"] == "app.Message":
            label_text = cell["attrs"]["label"]["text"]
            label_text = format_role_name(label_text)
            result["Message"].append(
                {
                    "label_text": label_text,
                    "description_text": cell["attrs"]["description"]["text"],
                    "id": cell["id"],
                }
            )
            id_to_label[cell["id"]] = label_text

    # 提取 Link 信息并添加 source_label 和 target_label
    for cell in input_data["cells"]:
        if cell["type"] == "app.Link":
            source_id = cell["source"]["id"]
            target_id = cell["target"]["id"]
            result["Link"].append(
                {
                    "source_label": id_to_label.get(source_id, ""),
                    "target_label": id_to_label.get(target_id, ""),
                    "source_id": source_id,
                    "target_id": target_id,
                }
            )
    simplified_data = result
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_path = (
        f"frontend_json_process/json_simplified/json_simplified_{timestamp}.json"
    )
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(simplified_data, file, indent=4, ensure_ascii=False)
    print("简化处理后的json已经保存到:", output_file_path)
    return output_file_path

# 读取 JSON 文件内容
json_file_path = "frontend_json_process/frontend-0729.json"
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

extract_data_to_simplified_json(data)