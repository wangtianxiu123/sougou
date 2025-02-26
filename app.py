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

        except TencentCloudSDKException as err:
            st.error(f"发生错误: {err}")
    else:
        st.warning("请确保输入了 SecretId、SecretKey 和搜索内容！")
