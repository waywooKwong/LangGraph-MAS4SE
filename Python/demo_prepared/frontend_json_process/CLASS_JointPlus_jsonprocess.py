import json

def extract_data_to_simplified_json(input_data):
    import datetime
    result = {"Message": [], "Link": []}
    # 创建一个 id 到 label_text 的映射
    id_to_label = {}
    for cell in input_data["cells"]:
        if cell["type"] == "app.FlowchartStart":
            label_text = cell["attrs"]["label"]["text"]
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
    output_file_path = f"frontend_json_process/json_simplified/json_simplified_{timestamp}.json"
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(simplified_data, file, indent=4, ensure_ascii=False)
    print("简化处理后的json已经保存到:", output_file_path)
    return output_file_path



