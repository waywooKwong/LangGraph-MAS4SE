import json

json_string = '{"sender": "智能客服机器人", "progress": "false", "answer": "尊敬的用户，您好！很高兴为您服务。请问您能告诉我您想要开发这款软件的大致目的是什么吗？"}'

try:
    response_dict = json.loads(json_string)
    print(response_dict)
except json.JSONDecodeError as e:
    print(f"JSON 解析失败: {e}")
