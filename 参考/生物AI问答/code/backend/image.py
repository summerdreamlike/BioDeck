import os
import base64
 
from openai import OpenAI
 
client = OpenAI(
    api_key = os.environ.get("MOONSHOT_API_KEY"), 
    base_url = "https://api.moonshot.cn/v1",
)
 
# 对图片进行base64编码
with open("您的图片地址", 'rb') as f:
    img_base = base64.b64encode(f.read()).decode('utf-8')
 
response = client.chat.completions.create(
    model="moonshot-v1-8k-vision-preview", 
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_base}"
                    }
                },
                {
                    "type": "text",
                    "text": "请描述这个图片"
                }
            ]
        }
    ]
)
print(response.choices[0].message.content)