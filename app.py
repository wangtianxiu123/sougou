# -*- coding: utf-8 -*-
import json
import streamlit as st
from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

# 设置页面标题
st.title("腾讯云搜索查询")

# 用户输入密钥
secret_id = st.text_input("请输入您的 SecretId:")
secret_key = st.text_input("请输入您的 SecretKey:", type="password")

# 用户输入查询内容
query = st.text_input("请输入搜索内容:")

# 用户输入分值限制
score_limit = st.number_input("请输入分值限制:", min_value=0.0, format="%.2f")

def highlight_keywords(text, keyword):
    """高亮显示关键词"""
    if keyword:
        # 使用正则表达式替换关键词，确保大小写不敏感
        import re
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub(f'<span style="color:red;">{keyword}</span>', text)
    return text

if st.button("查询"):
    if secret_id and secret_key and query:
        try:
            # 实例化一个认证对象
            cred = credential.Credential(secret_id, secret_key)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "tms.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            params = json.dumps({"Query": query})
            common_client = CommonClient("tms", "2020-12-29", cred, "", profile=clientProfile)
            result = common_client.call_json("SearchPro", json.loads(params))

            # 显示结果
            st.subheader("API 返回结果:")
            st.json(result)  # 显示原始 API 返回内容

            if "Response" in result and "Pages" in result["Response"]:
                pages = result["Response"]["Pages"]
                filtered_results = []

                # 过滤和排序结果
                for page in pages:
                    page_data = json.loads(page)  # 解析每个页面的 JSON 数据
                    score = page_data.get("score", 0)  # 获取分值
                    if score >= score_limit:  # 过滤分值
                        filtered_results.append(page_data)

                # 按照分值从高到低排序
                filtered_results.sort(key=lambda x: x["score"], reverse=True)

                # 显示过滤后的结果
                for page_data in filtered_results:
                    # 高亮显示关键词
                    highlighted_title = highlight_keywords(page_data['title'], query)
                    highlighted_passage = highlight_keywords(page_data['passage'], query)

                    # 创建卡片样式
                    st.markdown(f"""
                    <div style="border: 1px solid #e0e0e0; border-radius: 5px; padding: 10px; margin: 10px 0;">
                        <h4>{highlighted_title}</h4>
                        <p>{highlighted_passage}</p>
                        <p><strong>来源:</strong> {page_data['site']} | <strong>日期:</strong> {page_data['date']} | <strong>分值:</strong> {page_data['score']}</p>
                        <a href="{page_data['url']}" target="_blank">查看详情</a>
                    </div>
                    """, unsafe_allow_html=True)

                if not filtered_results:
                    st.warning("没有找到符合分值限制的结果。")

            else:
                st.warning("没有找到相关结果。")

        except TencentCloudSDKException as err:
            st.error(f"发生错误: {err}")
    else:
        st.warning("请确保输入了 SecretId、SecretKey 和搜索内容！") 
