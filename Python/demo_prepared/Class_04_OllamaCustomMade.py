# -*- coding: utf-8 -*-

import os
import subprocess # python 运行命令行指令
from langchain_community.chat_models import ChatOllama
from langchain_experimental.llms.ollama_functions import OllamaFunctions
class OllamaCustomMade:
    def __init__(self, model_name, role, duty):
        self.model_name = model_name
        self.role = role
        self.duty = duty
        self.target_model_name =  role + "-"  + model_name
        self.model_system_prompt = f"""You now is a developer in Sofeware Company,
        Your role is {self.role},
        Your duty is {self.duty},
        Answer as your role and Process request according to your duty,
        the assistant, only."""
        self.model = None
        
    def CustomMade(self):
        Modelfile_path = f"src/Ollama_Modelfile/{self.target_model_name}_Modelfile"
        with open(Modelfile_path, 'w') as file:
            file.write(f"FROM {self.model_name}\n")
            file.write("PARAMETER temperature 0.9\n")
            file.write(f"SYSTEM \"\"\"{self.model_system_prompt}\"\"\"")
        print("ollama 角色定制文本已生成:",Modelfile_path)
        
        subprocess.run(['ollama', 'serve']) 
        subprocess.run(['ollama', 'pull', self.model_name])
        subprocess.run(['ollama', 'create', self.target_model_name, '-f', Modelfile_path])
        print("ollama 模型已经创建:", self.target_model_name)
        
    def RemoveModel(self):
        subprocess.run(['ollama', 'rm', self.target_model_name]) 
        print()
    
    def get_ChatOllama(self):
        self.CustomMade()
        model = ChatOllama(model=self.target_model_name)
        self.model = model
        print("model:",model)
        print(f"ChatOllama 加载 Model SystemPrompt 定制的 {self.target_model_name} 成功")
        return model
        
# # 测试代码:
# OllamaBuild = OllamaCustomMade(model_name='phi3',role='ProjectManager',duty='ManageProject')
# model = OllamaBuild.get_ChatOllama()
# result = model.invoke("hello?")
# print("result:",result.content)