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
            if "Response" in result and "Pages" in result["Response"]:
                pages = result["Response"]["Pages"]
                for page in pages:
                    page_data = json.loads(page)  # 解析每个页面的 JSON 数据
                    st.card(
                        title=page_data["title"],
                        content=page_data["passage"],
                        date=page_data["date"],
                        site=page_data["site"],
                        url=page_data["url"],
                        image=page_data.get("images", [None])[0]  # 获取第一张图片
                    )
                    st.markdown(f"[查看详情]({page_data['url']})")  # 添加链接

            else:
                st.warning("没有找到相关结果。")

        except TencentCloudSDKException as err:
            st.error(f"发生错误: {err}")
    else:
        st.warning("请确保输入了 SecretId、SecretKey 和搜索内容！") 
