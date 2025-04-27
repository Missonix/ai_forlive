from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
import json
import os
from typing import Dict, Any
import asyncio
from core.response import ApiResponse
from robyn import Response, status_codes

# 初始化模型
async def init_model():
    try:
        model = ChatOpenAI(
            openai_api_key="31711a19-2c64-4337-a7b1-70be31e1fdd2",
            openai_api_base="https://ark.cn-beijing.volces.com/api/v3",
            model_name="doubao-pro-32k-241215",
            temperature=0.7,
            streaming=True
        )
        return model
    except Exception as e:
        raise Exception(f"模型初始化失败: {str(e)}")

async def speech_generation(input, Scenario):
    try:
        # 定义系统提示词
        system_prompt_1 = """# 角色
        你是一位经验丰富且专业的电商直播产品卖点解析大师，凭借深厚的行业经验和敏锐的市场洞察力，能够深入剖析用户提供的产品信息，精准提炼并生成极具吸引力的电商直播话术相关内容。

        ## 技能
        ### 技能 1: 解析并生成产品信息
        1. 当用户提供产品信息后，迅速且准确地解析或生成商品名称/类目（如服饰、美妆、3C 等），核心卖点，价格策略（原价/折扣价/限时优惠），目标人群（性别、年龄、消费场景）。
        2. 最终输出字段需严格按照以下详细格式：
            - 商品名称：product_name
            - 商品类目：明确写出具体属于哪类产品，例如“时尚女装”“高端美妆”“智能 3C 产品”等
            - 核心卖点：全面阐述产品独特优势，突出吸引消费者的关键因素
            - 价格策略：详细说明原价、折扣价及限时优惠的具体情况，如“原价 500 元，现折扣价 300 元，限时优惠额外再减 50 元”
            - 目标人群：清晰定位目标消费群体，如“年轻女性，年龄在 20 - 35 岁之间，适合日常休闲场景消费”
        3. 最终输出字段严格要求：
            - 商品名称：product_name
            - 商品类目：product_category
            - 核心卖点：selling_points
            - 价格策略：discount
            - 目标人群：crowd
        4. 你必须以JSON格式返回结果,包含以下字段:
            {{
                "product_name": "商品名称",
                "product_category": "商品类目(如时尚女装/高端美妆/智能3C产品等)",
                "selling_points": "核心卖点(全面阐述产品独特优势)",
                "discount": "价格策略(详细说明原价、折扣价及限时优惠)",
                "crowd": "目标人群(清晰定位目标消费群体)"
            }}

        ## 限制:
        - 只围绕电商直播产品卖点解析相关内容进行回复，坚决拒绝回答无关话题。
        - 输出内容必须严格按照JSON格式返回,不得有任何其他格式。
        - 若用户提供的信息不完整，如仅提及核心卖点、折扣等部分信息，需自行合理分析生成缺失内容。

        """

        # 定义提示词模板
        prompt_template1 = ChatPromptTemplate.from_messages([
            ('system', system_prompt_1),
            ('user', '{input}')
        ])

        model = await init_model()
        parser = JsonOutputParser()
        chain1 = prompt_template1 | model | parser

        # 产品解析生成输出 
        analyze_products = await chain1.ainvoke({"input": input})

        product_name = analyze_products['product_name']
        product_category = analyze_products['product_category']
        selling_points = analyze_products['selling_points']
        discount = analyze_products['discount']
        crowd = analyze_products['crowd']

        # 话术生成
        # 定义系统提示词
        system_prompt_2 = """
        # 角色
        你是一位经验丰富、专业资深的电商直播话术生成专家，对各类电商产品和直播话术技巧有着深入的了解。你擅长结合产品详细信息（包括名称、类目、卖点、折扣、目标人群）以及不同的直播场景（日常、大促、节日），生成完整且具有吸引力的话术脚本，涵盖开场白、产品介绍、促销环节、逼单策略以及结尾等各个部分。

        ## 技能
        ### 技能 1: 生成直播话术脚本
        1. 当用户提供产品信息（名称、类目、卖点、折扣、人群）以及场景（日常、大促、节日）时，根据这些信息生成完整话术脚本。
        2. 开场白要能够吸引观众注意力，自然引出产品。
        3. 产品介绍部分需突出产品特点、优势以及对目标人群的价值。
        4. 促销环节要清晰说明折扣力度、优惠活动等。
        5. 逼单策略要具有紧迫感，促使观众尽快下单。
        6. 结尾要简洁有力，引导观众关注、点赞、下单等。
        ===回复示例===
        ### 开场白
        [具体开场白内容]

        ### 产品介绍
        [详细产品介绍内容]

        ### 促销
        [具体促销活动说明]

        ### 逼单
        [有力的逼单话术]

        ### 结尾
        [简洁结尾话术]
        ===示例结束===
        7. 你必须以JSON格式返回结果,包含以下字段:
        {{
            "output": {{
                "开场白": "吸引观众注意力的开场白",
                "产品介绍": "突出产品特点和优势的介绍",
                "促销": "清晰的折扣和优惠活动说明",
                "逼单": "具有紧迫感的逼单话术",
                "结尾": "引导观众行动的结尾话术"
            }}
        }}

        ## 限制:
        - 输出内容必须围绕电商直播话术生成展开，拒绝回答与该任务无关的话题。
        - 所生成的话术脚本必须包含开场白、产品介绍、促销、逼单、结尾这几个部分，不能遗漏。
        - 必须严格按照JSON格式返回,不得包含任何其他格式的内容。
        - 回复内容需语言通顺、逻辑合理。 
        """

        # 定义提示词模板
        prompt_template2 = ChatPromptTemplate.from_messages([
            ('system', system_prompt_2),
            ('user', '商品名称：{product_name},商品类目：{product_category},商品卖点：{selling_points},商品折扣：{discount},目标人群：{crowd},直播场景：{Scenario}')
        ])

        chain2 = prompt_template2 | model | parser
        speech_generation = await chain2.ainvoke({"product_name": product_name, "product_category": product_category, "selling_points": selling_points, "discount": discount, "crowd": crowd, "Scenario": Scenario})
        output = speech_generation['output']


        # 整合json输出结果
        result = {
            "product_name": product_name,
            "product_category": product_category,
            "selling_points": selling_points,
            "discount": discount,
            "crowd": crowd,
            "Scenario": Scenario,
            "output": output
        }
        print(result)
        return result  # 直接返回字典结果

    except Exception as e:
        print(f"Error: {e}")
        return False

async def main():
    input = """云南高山黑糖姜茶 姨妈期必备 
❗划重点：无添加蔗糖！3秒速溶！ 
【直播间专属】拍2盒发5盒 再送保温杯 
配料表：纯甘蔗汁+罗平小黄姜 
保质期：2025.06.18 假一赔十 
孕产妇禁用 糖尿病患者慎用 """
    result = await speech_generation(input=input, Scenario="日常")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

