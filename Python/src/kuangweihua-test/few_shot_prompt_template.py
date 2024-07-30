# zero-shot / few_shot
# 1. 创建示例样本列表，输入输出均使用占位符形式给出
from typing import List, Dict

samples: List[Dict[str, str]] = [
    {
        "phone_type": "iPhone",
        "occasion": "时尚",
        "ad_text": "iPhone手机，时尚的象征，是彰显你时尚前卫的最佳选择。",
    },
    {
        "phone_type": "小米",
        "occasion": "技术指标",
        "ad_text": "小米手机代表前沿技术的引领与强大技术指标，是赠送类技术宅的完美礼物。",
    },
    {
        "phone_type": "华为",
        "occasion": "自主、创新",
        "ad_text": "华为手机代表国产品牌的自主与创新，是你表达对自主创新支持的理想选择。",
    },
    {
        "phone_type": "一加",
        "occasion": "游戏、技术指标",
        "ad_text": "一加手机在游戏领域表现出色，具有优异的技术指标，是游戏宅的最好选择。",
    },
]
# 2. 创建提示模板对象，即：样例提示模板对象
from langchain_core.prompts import PromptTemplate

# 2-1. 提示模板字符串
prompt_template_str: str = (
    "手机类型：{phone_type}\n场景：{occasion}\n广告文案：{ad_text}"
)

# 2-2. 提示模板对象，基于样例
prompt_template_sample: PromptTemplate = PromptTemplate.from_template(
    template=prompt_template_str,
)

one_shot_sample_prompt_str_example: str = prompt_template_sample.format(
    **samples[0]
)  # 使用 ** 操作符将这个字典解包成关键字参数。
print(
    "含有单一示例样本的提示样例字符串：\n",
    one_shot_sample_prompt_str_example,
    end="\n\n",
)

# 3. 创建 FewShotPromptTemplate 对象
# 3-1. 基于 样本提示模板对象 生成 少样本提示模板对象
from langchain.prompts.few_shot import FewShotPromptTemplate

"""
    本质：
    1. 样例列表
    2. 样例提示模板对象
    3. 传入语言模型用于输入的占位符变量名
"""
few_shot_sample_prompt_template: FewShotPromptTemplate = FewShotPromptTemplate(
    examples=samples,
    example_prompt=prompt_template_sample,
    suffix="手机类型：{phone_type}\n场景：{occasion}",
    input_variables=["phone_type", "occasion"],
)
# 3-2. 生成含有样例列表的提示字符串
few_shot_sample_prompt_str: str = few_shot_sample_prompt_template.format(
    phone_type="诺基亚", occasion="职场"
)
print("少样本提示字符串", few_shot_sample_prompt_str, end="\n\n")
from modelchoise import modelchoise
from langchain_core.messages import AIMessage
chat_model = modelchoise.get_zhipuai_chat_model()
completion:AIMessage=chat_model.invoke(
    input=few_shot_sample_prompt_str
)
print(completion)

# 4. 使用示例选择器
'''
向量数据库
    1. FAISS 参考前面内容
    2. Qdrant：
        保证支撑本地使用 Qdrant 的 WebServer 模式
        1. 安装 qdrant client
            pip install qdrant client
        2. 安装 qdrant 和 langchain 链接器
            pip install langchain-qdrant
        3. Qdrant WebServer
        4. 防火墙 6333 入站端口
'''
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Qdrant
from langchain_core.example_selectors import SemanticSimilarityExampleSelector

embeddings = HuggingFaceEmbeddings(
    model_name="models\m3e-base",
    model_kwargs={'device': 'cpu'})
print("Embedding from huggingface: \n", embeddings)

text_splitter = RecursiveCharacterTextSplitter()
# 4-1 初始化一个实例选择器对象
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples=samples,
    embeddings=embeddings,
    vectorstore_cls=Qdrant,
    k=2,
)

few_shot_prompt_template_sample_by_example_selector = FewShotPromptTemplate(
    examples=samples,
    example_prompt=prompt_template_sample,
    suffix="手机类型：{phone_type}\n场景：{occasion}",
    input_variables=["phone_type", "occasion"],
)

few_shot_prompt_by_example_selector_str = few_shot_prompt_template_sample_by_example_selector.format(
    phone_type="联想",
    occasion="游戏、职场"
)

completion=chat_model.invoke(input=few_shot_prompt_by_example_selector_str)
print(completion)