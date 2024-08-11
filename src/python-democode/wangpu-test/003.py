import json

json_string = """
```json
{
  "sender": "智能客服机器人",
  "progress": "false",
  "answer": "当然可以。B站，全名哔哩哔哩（Bilibili），是一家中国的在线弹幕视频分享平台，成立于2009年。它以二次元文化起家，但现在已经发展成为一个包含了多元内容的视频社区，涵盖了动画、游戏、音乐、舞蹈、科技、生活等多个领域。

B站的核心功能包括：
1. 视频播放：用户可以观看和上传视频，支持弹幕评论，这是一种独特的实时评论功能，允许观看者在视频播放时发表评论，与其他观众互动。
2. 社区互动：B站拥有强大的社区氛围，用户可以在各个视频下方发表评论，参与讨论，还可以在平台上发布自己的文章和动态。
3. 内容创作：B站鼓励用户创作原创内容，无论是视频、音乐、绘画还是其他艺术形式。
4. 直播：B站还提供了直播服务，用户可以观看或进行直播，内容多样，包括游戏直播、绘画、聊天等。

请问您想了解B站的哪方面内容？是希望了解其业务模式、用户群体、还是技术实现等方面？这样我能够更准确地提供您需要的信息。"
}
```
"""

import re
import os


def to_strict_json(json_str):
    json_str = json_str.strip()
    json_str = json_str.strip("`")
    json_str = json_str.strip("json")
    # 替换换行符和回车符为 JSON 兼容的转义字符
    json_str = json_str.replace('\r\n', "\\n").replace('\n', "\\n")
    json_str = json_str.strip("\\n")
    json_str = json_str.strip("{")
    json_str = json_str.strip("}")
    json_str = json_str.strip("\\n")
    json_str = json_str.strip()
    json_str = f"{{{json_str}}}"
    json_str = json_str.replace('\\', "\\\\")
    json_str = re.sub(r'\\\\n', '\\n', json_str, count=2)

    # 确保 JSON 字符串有效

    # 转换为严格的 JSON 格式
    return json_str


cleaned_json_string = to_strict_json(json_string)
print(cleaned_json_string)
try:
    response_dict = json.loads(cleaned_json_string, strict=False)
    print(response_dict)
except json.JSONDecodeError as e:
    print(f"JSON 解析失败: {e}")
