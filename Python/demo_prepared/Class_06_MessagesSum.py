# -*- coding: utf-8 -*-
import os
import datetime
from langchain_core.messages import HumanMessage, AIMessage

import os
import hashlib
class MessagesSum:
    def __init__(self):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def sum_message_to_file(self, messages: list):
        # 顺序遍历List输出, 保证了每次得到的都是角色最后一次输出的信息 
        for message in messages:
            if hasattr(message, 'name') and message.name:
                os.makedirs(f"MessageSum/{self.timestamp}", exist_ok=True)
                # 模型生成基本都是 markdown 语句, 所以 .md 文本效果最好
                file_path = f"MessageSum/{self.timestamp}/{message.name}.md"
                with open(file_path, 'w', encoding='UTF-8') as file:
                    file.write(message.content)
                print(f"{file_path}文本生成完成")



    def sum_prompt_to_file(self, messages: list):
        os.makedirs(f"PromptSum/{self.timestamp}", exist_ok=True)

        for i, content in enumerate(messages):
            # 使用哈希生成唯一的文件名
            file_name = hashlib.md5(content.encode()).hexdigest()
            file_path = f"PromptSum/{self.timestamp}/{file_name}.md"

            with open(file_path, 'w', encoding='UTF-8') as file:
                file.write(content)

            print(f"{file_path} 文本生成完成")

# MessagesSum = MessagesSum()
# messages=[HumanMessage(content='请设计一个银行管理系统'), HumanMessage(content='请设计一个银行管理系统'), AIMessage(content='设计一个银行管理系统是一个复杂的任务，涉及多个模块和功能。以下是一个简化的版本，概述了主要的功能模块和基本的设计思路。\n\n### 一、系统目标\n\n1. **安全性**：确保用户资金和信息的安全。\n2. **便捷性**：简化用户操作，提高工作效率。\n3. **可靠性**：系统稳定，数据准确无误。\n4. **扩展性**：方便未来添加新功能或与其他系统集成。\n\n### 二、核心功能模块\n\n1. **用户管理**\n    - 用户注册、登录、信息修改、密码找回等。\n    - 实名认证和权限控制。\n  \n2. **账户管理**\n    - 银行账户的开设、查询、冻结、销户等。\n    - 余额查询、交易记录查询。\n\n3. **资金转账**\n    - 同行转账、跨行转账。\n    - 设置转账限额和审核机制。\n\n4. **存款与贷款**\n    - 定期存款、活期存款、理财产品。\n    - 贷款申请、审批、还款等。\n\n5. **报表与统计**\n    - 用户余额、交易额、贷款额的统计。\n    - 定期生成财务报表。\n\n6. **风险管理**\n    - 欺诈检测、异常交易警报。\n    - 风险评估和信贷控制。\n\n7. **系统设置与维护**\n    - 用户权限分配、操作日志。\n    - 数据备份和恢复。\n\n### 三、技术选型\n\n1. **前端**：HTML/CSS/JavaScript，框架如React或Vue。\n2. **后端**：Java、Python或C#，框架如Spring Boot、Django或ASP.NET。\n3. **数据库**：MySQL、Oracle或PostgreSQL。\n4. **安全**：SSL加密，两步验证，防火墙等。\n5. **云服务**：如AWS、Azure或阿里云。\n\n### 四、具体实现\n\n1. **用户管理**\n    - 使用JWT（JSON Web Tokens）进行身份验证。\n    - 用户信息存储在数据库中，使用哈希加密存储密码。\n\n2. **账户管理**\n    - 通过RESTful API进行前后端交互。\n    - 对敏感操作设置权限验证。\n\n3. **资金转账**\n    - 引入第三方支付服务，如支付宝或银联。\n    - 设定每日转账限额和交易次数限制。\n\n4. **存款与贷款**\n    - 根据不同产品设定利率和期限。\n    - 通过信用评分系统进行贷款审批。\n\n5. **报表与统计**\n    - 使用数据可视化工具，如ECharts。\n    - 定期生成PDF报表。\n\n6. **风险管理**\n    - 引入机器学习算法，进行异常检测。\n    - 建立风险控制模型。\n\n7. **系统维护**\n    - 设置系统日志，记录操作记录。\n    - 定期进行数据备份。\n\n这只是一个基础的设计思路，实际应用中需要根据具体需求进行详细设计和调整。希望这对你有所帮助。', name='TechLeader'), HumanMessage(content='请设计一个银行管理系统'), HumanMessage(content='请设计一个银行管理系统'), AIMessage(content='设计一个银行管理系统是一个复杂的任务，涉及多个模块和功能。以下是一个简化的版本，概述了主要的功能模块和基本的设计思路。\n\n### 一、系统目标\n\n1. **安全性**：确保用户资金和信息的安全。\n2. **便捷性**：简化用户操作，提高工作效率。\n3. **可靠性**：系统稳定，数据准确无误。\n4. **扩展性**：方便未来添加新功能或与其他系统集成。\n\n### 二、核心功能模块\n\n1. **用户管理**\n    - 用户注册、登录、信息修改、密码找回等。\n    - 实名认证和权限控制。\n  \n2. **账户管理**\n    - 银行账户的开设、查询、冻结、销户等。\n    - 余额查询、交易记录查询。\n\n3. **资金转账**\n    - 同行转账、跨行转账。\n    - 设置转账限额和审核机制。\n\n4. **存款与贷款**\n    - 定期存款、活期存款、理财产品。\n    - 贷款申请、审批、还款等。\n\n5. **报表与统计**\n    - 用户余额、交易额、贷款额的统计。\n    - 定期生成财务报表。\n\n6. **风险管理**\n    - 欺诈检测、异常交易警报。\n    - 风险评估和信贷控制。\n\n7. **系统设置与维护**\n    - 用户权限分配、操作日志。\n    - 数据备份和恢复。\n\n### 三、技术选型\n\n1. **前端**：HTML/CSS/JavaScript，框架如React或Vue。\n2. **后端**：Java、Python或C#，框架如Spring Boot、Django或ASP.NET。\n3. **数据库**：MySQL、Oracle或PostgreSQL。\n4. **安全**：SSL加密，两步验证，防火墙等。\n5. **云服务**：如AWS、Azure或阿里云。\n\n### 四、具体实现\n\n1. **用户管理**\n    - 使用JWT（JSON Web Tokens）进行身份验证。\n    - 用户信息存储在数据库中，使用哈希加密存储密码。\n\n2. **账户管理**\n    - 通过RESTful API进行前后端交互。\n    - 对敏感操作设置权限验证。\n\n3. **资金转账**\n    - 引入第三方支付服务，如支付宝或银联。\n    - 设定每日转账限额和交易次数限制。\n\n4. **存款与贷款**\n    - 根据不同产品设定利率和期限。\n    - 通过信用评分系统进行贷款审批。\n\n5. **报表与统计**\n    - 使用数据可视化工具，如ECharts。\n    - 定期生成PDF报表。\n\n6. **风险管理**\n    - 引入机器学习算法，进行异常检测。\n    - 建立风险控制模型。\n\n7. **系统维护**\n    - 设置系统日志，记录操作记录。\n    - 定期进行数据备份。\n\n这只是一个基础的设计思路，实际应用中需要根据具体需求进行详细设计和调整。希望这对你有所帮助。', name='TechLeader'), AIMessage(content='设计银行管理系统是一个非常复杂的项目，需要考虑到各种功能和安全性问题。你所提供的概述是非常全面的，以下是对你设计思路的一些补充和建议：\n\n### 一、系统目标\n\n- **合规性**：确保系统符合国家相关金融法律法规和政策要求。\n\n### 二、核心功能模块\n\n**补充：**\n\n1. **用户管理**\n   - 用户行为分析，以防止洗钱等非法行为。\n\n2. **资金转账**\n   - 实时转账与定时转账功能。\n   - 支持国际转账及外汇管理。\n\n3. **存款与贷款**\n   - 提供在线咨询服务，为用户提供贷款、存款产品的解释和推荐。\n\n4. **报表与统计**\n   - 实时数据监控和预警系统。\n   - 对数据进行多维度分析，支持管理层的决策。\n\n5. **风险管理**\n   - 定期进行压力测试，评估系统承受金融风险的能力。\n\n### 三、技术选型\n\n**建议：**\n\n- **前端**：考虑到用户体验和交互设计，可引入Ant Design等UI设计语言，提升系统界面的友好性和一致性。\n- **后端**：对于高并发处理，可以考虑使用如Java的Spring Cloud微服务架构，提高系统性能和可维护性。\n- **数据库**：对于大型银行系统，可能需要考虑分布式数据库解决方案，如分布式数据库中间件MyCat等。\n- **中间件**：引入消息队列如RabbitMQ或Kafka，用于处理异步任务和系统间的解耦合。\n\n### 四、具体实现\n\n**补充：**\n\n1. **用户管理**\n   - 引入多因素认证（MFA）机制，比如手机动态验证码、生物识别等。\n\n2. **账户管理**\n   - 提供账户冻结、解冻的审核流程和日志记录。\n\n3. **资金转账**\n   - 与国家反洗钱系统对接，进行交易监控。\n   - 采用事务管理确保转账过程的原子性。\n\n4. **存款与贷款**\n   - 提供在线计算器，帮助用户预估利息和还款额。\n\n5. **报表与统计**\n   - 报表审核和电子签名，确保报表的权威性。\n\n6. **风险管理**\n   - 建立反欺诈系统，集成行为分析、生物识别等技术。\n\n7. **系统维护**\n   - 引入自动化运维工具，如Ansible、Docker等，提升部署和运维效率。\n   - 建立灾备中心，确保系统的高可用性。\n\n在设计和实现过程中，务必重视与相关金融监管部门的沟通，确保系统的合规性。同时，需要不断对系统进行安全评估和优化，以应对不断变化的网络环境和安全威胁。', name='QA1'), AIMessage(content='您好, 我是客服机器人Bot2, 我已将您的意见反馈, 请等待反馈结果', name='Bot02')]
# MessagesSum.sum_message_to_file(messages=messages)
