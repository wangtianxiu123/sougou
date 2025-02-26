# -*- coding: utf-8 -*-
import json
import streamlit as st
from entctencloud.common.common_client import CommonClient
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
            st.json(result)  # 以 JSON 格式展示 API 返回结果

            # 自定义展示效果
            st.subheader("展示效果:")
            st.write(f"您搜索的内容是: **{query}**")
            # 这里可以添加更多的展示效果

        except TencentCloudSDKException as err:
            st.error(f"发生错误: {err}")
    else:
        st.warning("请确保输入了 SecretId、SecretKey 和搜索内容！") 