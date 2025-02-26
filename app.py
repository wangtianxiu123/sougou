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

# 用户输入模式
mode = st.selectbox("请选择返回结果类型:", options=[0, 1, 2], index=0, format_func=lambda x: f"模式 {x}")

# 用户输入指定域名
insite = st.text_input("请输入指定域名（可选）:")

# 用户输入起始时间
from_time = st.number_input("请输入起始时间（时间戳，0表示当前时间）:", min_value=0)

# 用户输入分值限制
score_limit = st.number_input("请输入分值限制:", min_value=0.0, format="%.2f")

# 默认图像
default_cover_image = "https://via.placeholder.com/400x200.png?text=No+Image"  # 默认封面图像
default_favicon = "https://via.placeholder.com/20.png?text=Favicon"  # 默认图标

if st.button("查询"):
    if secret_id and secret_key and query:
        try:
            # 实例化一个认证对象
            cred = credential.Credential(secret_id, secret_key)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "tms.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            # 构建请求参数
            params = {
                "Query": query,
                "Mode": mode,
                "Insite": insite,
                "FromTime": from_time
            }
            common_client = CommonClient("tms", "2020-12-29", cred, "", profile=clientProfile)
            result = common_client.call_json("SearchPro", params)

            # 显示 API 返回结果
            st.subheader("API 返回结果:")
            st.json(result)  # 显示原始 API 返回内容

            if "Response" in result and "Pages" in result["Response"]:
                pages = result["Response"]["Pages"]
                filtered_results = []

                # 解析和过滤结果
                for page in pages:
                    page_data = json.loads(page)  # 解析每个页面的 JSON 数据
                    filtered_results.append(page_data)

                # 按照 score 从高到低排序
                filtered_results.sort(key=lambda x: x.get("score", 0), reverse=True)

                # 显示过滤后的结果
                for page_data in filtered_results:
                    # 使用原来的格式渲染
                    title = page_data.get('title', '无标题')
                    passage = page_data.get('passage', '无内容')
                    site = page_data.get('site', '未知来源')
                    date = page_data.get('date', '未知日期')
                    score = page_data.get('score', 0)  # 获取分值
                    favicon = page_data.get("favicon", "https://via.placeholder.com/20.png?text=Favicon")  # 获取图标
                    url = page_data.get('url', '#')  # 获取链接，如果没有则使用 #

                    # 使用 HTML 渲染卡片
                    st.markdown(f"""
                    <div style="border: 1px solid #e0e0e0; border-radius: 5px; padding: 10px; margin: 10px 0;">
                        <h4>{title}</h4>
                        <p>{passage}</p>
                        <p><strong>来源:</strong> {site} | <strong>日期:</strong> {date} | <strong>分值:</strong> {score}</p>
                        <img src="{favicon}" style="width:20px; height:20px;" />
                        <a href="{url}" target="_blank">查看详情</a>
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
