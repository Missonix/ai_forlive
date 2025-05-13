from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
import json
import os
from typing import Dict, Any
import asyncio
# 初始化模型
async def init_model():
    try:
        model = ChatOpenAI(
            openai_api_key="4a9c6c92-91fa-4087-beb3-4a894d0ce586",
            openai_api_base="https://ark.cn-beijing.volces.com/api/v3",
            model_name="doubao-1.5-pro-32k-250115",
            temperature=0.7,
            streaming=True
        )
        return model
    except Exception as e:
        raise Exception(f"模型初始化失败: {str(e)}")

async def shooting_suggestions(product_name, category, country):
    try:
         # 定义系统提示词
        system_prompt_1 = """# 角色
    你是一位在跨境电商领域经验丰富的专业大师，擅长根据电商商品给出拍摄建议及方案。当用户输入商品名称、商品类目和销售国家后，你能够依据这些信息，结合目标国家当地国情及民俗，尊重当地风俗避免文化禁忌，为用户提供精准且具有针对性的拍摄建议。

    ## 技能
    ### 技能 1: 给出拍摄建议
    1. 当用户输入商品名称、商品类目和销售国家时，分析这些信息。
    2. 结合你在跨境电商领域的专业知识和过往经验，充分考虑目标国家国情民俗，为用户提供拍摄建议及方案。
    请以 JSON 格式输出，包含以下字段：
    - scenes: 拍摄场景建议:<具体场景描述>
    - style: 拍摄风格建议:<风格特点阐述>
    - lens_usage: 镜头运用建议:<镜头运用方式说明>
    - actor_selection: 演员选择建议（如适用）:<演员相关建议>
    - prop_matching: 道具搭配建议:<道具搭配说明>

    ## 限制:
    - 只回答与跨境电商商品拍摄建议相关的内容，拒绝回答无关话题。
    - 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。
    - 以json格式输出，不要输出其他内容。
    - 需充分考虑目标国家当地国情及民俗，尊重当地风俗避免文化禁忌。
    """

        # 定义提示词模板
        prompt_template1 = ChatPromptTemplate.from_messages([
            ('system', system_prompt_1),
            ('user', '商品名称：{product_name}，商品类目：{category}，销售国家：{country}')
        ])

        model = await init_model()
        parser = JsonOutputParser()
        chain1 = prompt_template1 | model | parser

        Video_suggestions = await chain1.ainvoke({"product_name": product_name, "category": category, "country": country})

        scenes = Video_suggestions["scenes"]
        style = Video_suggestions["style"]
        lens_usage = Video_suggestions["lens_usage"]
        actor_selection = Video_suggestions["actor_selection"]
        prop_matching = Video_suggestions["prop_matching"]

        # 整合json输出结果
        result = {
            "scenes": scenes,
            "style": style,
            "lens_usage": lens_usage,
            "actor_selection": actor_selection,
            "prop_matching": prop_matching
        }
        print(result)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return False


async def main():
    result = await shooting_suggestions(product_name="智能感应垃圾桶", category="家居用品", country="泰国")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
