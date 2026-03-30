import os
import requests

# 1. 搜索：获取关于孙福友的最新网页动态
def get_search_results():
    url = "https://google.serper.dev/search"
    payload = {
        "q": "华为 孙福友 出席 活动 峰会 论坛", 
        "gl": "cn", "hl": "zh-cn", "tbs": "qdr:w"
    }
    headers = {'X-API-KEY': os.getenv("SERPER_API_KEY")}
    response = requests.post(url, json=payload)
    return response.json()

# 2. 智选：让 DeepSeek 提取真正的活动信息
def ai_filter_events(search_data):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    prompt = f"请分析以下搜索结果，提取关于'孙福友'（华为电力数字化军团CEO）近期或未来将要出席的会议、论坛或活动。要求：1. 排除已过期的旧闻；2. 提取时间、地点和活动名称。如果没发现相关活动，请仅回答'无'。数据：{search_data}"
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    return result['choices'][0]['message']['content']

# 3. 推送：发送到微信
def send_to_wechat(content):
    push_key = os.getenv("PUSH_KEY")
    url = "https://api2.pushdeer.com/message/push"
    payload = {
        "pushkey": push_key,
        "text": "📅 孙福友活动监测日报",
        "desp": content,
        "type": "markdown"
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    results = get_search_results()
    report = ai_filter_events(results)
    
    if "无" not in report:
        send_to_wechat(report)
    else:
        print("今日暂无新活动动态。")