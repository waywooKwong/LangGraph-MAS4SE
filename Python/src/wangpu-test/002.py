# -*- coding: utf-8 -*-

def convert_newline_escape(json_str):
    """将字符串中的 '\\n' 转换为实际的换行符 '\n'"""
    # 替换字符串中的 '\\n' 为 '\n'
    return json_str.replace('\\n', '\n')

# 示例字符串
text = """
关于B站的详细介绍如下：\n\n### B站基本情况\n哔哩哔哩（Bilibili）成立于2009年，是一家以ACG（动画、漫画、游戏）文化为核心的年轻人社区。它以视频分享为基础，提供弹幕评论系统，使得用户在观看视频的同时可以进行实时互动。\n\n### 主要功能\n1. 视频播放：提供丰富的视频内容，包括动画、游戏、音乐、舞蹈、科技等众多领域。\n2. 弹幕评论：特色的弹幕功能，允许用户在视频播放时发送评论，与其他观众互动。\n3. 直播：支持主播进行直播，观众可以观看直播并与主播互动。\n4. 社区交流：用户可以在论坛板块进行讨论，分享自己的作品和观点。\n\n### 内容拓展\nB站不仅限于ACG内容，还拓展到了教育、科普、生活娱乐等多个领域，吸引了更广泛的用户群体。\n\n### 用户群体\nB站的用户主要是年轻人，特别是对二次元文化有兴趣的用户。\n\n### 商业模式\nB站主要通过会员订阅、直播打赏、广告收入等方式进行盈利。\n\n### 技术特点\nB站的技术栈包括了视频编码、直播技术、弹幕系统等，支持高并发和高互动性的用户需求。\n\n### 未来发展\nB站持续在内容多样化、社区建设和用户体验上投入，旨在成为年轻人的文化社区。\n\n如果您对B站的某一方面或功能有特别感兴趣或者有具体的问题，请告诉我，我会提供更加详细的信息。
"""
# 使用函数转换
converted_text = convert_newline_escape(text)

print("转换后的字符串:")
print(converted_text)