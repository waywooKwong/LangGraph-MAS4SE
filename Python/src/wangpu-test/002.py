# -*- coding: utf-8 -*-

import json

# 修正后的 JSON 字符串示例
cleaned_json_string = """
{
    "sender": "智能客服机器人",
    "progress": "true",
    "answer": "尊敬的用户，非常感谢您提供的信息。根据您的要求，我们已经整理出以下需求说明书：\\n\\n1. 应用名称：视频分享应用\\n2. 应用功能：视频分享、社交互动（关注、评论、私信等）\\n3. 用户群体：全年龄层\\n4. 界面风格：简洁、现代\\n5. 技术选型：云服务、关系型数据库\\n6. 登录方式：用户名密码、第三方账号登录\\n7. 预算：充足\\n8. 项目管理：包含测试团队\\n\\n请您确认是否满意以上需求说明书，如果有任何修改意见，请随时告知。"
}
"""

try:
    # 解析 JSON 字符串
    response_dict = json.loads(cleaned_json_string)

    # 提取字段示例
    sender = response_dict.get("sender", "字段不存在")
    progress = response_dict.get("progress", "字段不存在")
    answer = response_dict.get("answer", "字段不存在")

    print("\n解析结果：")
    print(f"Sender: {sender}")
    print(f"Progress: {progress}")
    print(f"Answer: {answer}")

except json.JSONDecodeError as e:
    print(f"JSON 解析错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")
