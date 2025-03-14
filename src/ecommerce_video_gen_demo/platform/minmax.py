import os
import time
import requests
import json

api_key = os.getenv('MINIMAX_API_KEY', '')
api_base = os.getenv('MINIMAX_API_BASE', '')

prompt = "请在此输入生成视频的提示词文本内容"
model = "I2V-01-Director" 
output_file_name = "output.mp4" #请在此输入生成视频的保存路径

def invoke_video_generation(prompt, first_frame_image)->str:
    print("-----------------提交视频生成任务-----------------")
    url = f"{api_base}/video_generation"
    payload = json.dumps({
      "prompt": prompt,
      "model": model,
      'first_frame_image': first_frame_image
    })
    headers = {
      'authorization': 'Bearer ' + api_key,
      'content-type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    task_id = response.json()['task_id']
    print("视频生成任务提交成功，任务ID："+task_id)
    return task_id

def query_video_generation(task_id: str):
    url = f"{api_base}/query/video_generation?task_id="+task_id
    headers = {
      'authorization': 'Bearer ' + api_key
    }
    response = requests.request("GET", url, headers=headers)
    status = response.json()['status']
    if status == 'Preparing':
        print("...准备中...")
        return "", 'Preparing'
    elif status == 'Queueing':
        print("...队列中...")
        return "", 'Queueing'
    elif status == 'Processing':
        print("...生成中...")
        return "", 'Processing'
    elif status == 'Success':
        return response.json()['file_id'], "Finished"
    elif status == 'Fail':
        return "", "Fail"
    else:
        return "", "Unknown"


def fetch_video_url(file_id: str):
    print("---------------视频生成成功，下载中---------------")
    url = f"{api_base}/files/retrieve?file_id="+file_id
    headers = {
        'authorization': 'Bearer '+api_key,
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)

    download_url = response.json()['file']['download_url']

    return download_url


def generate_video_from_image(image_base64: str, prompt: str, *, timeout: int = 300):
    task_id = invoke_video_generation(prompt, image_base64)

    while True:
        file_id, status = query_video_generation(task_id)
        if file_id != "":
            print("---------------生成成功---------------")
            download_url = fetch_video_url(file_id)
            print(f'下载链接：{download_url}')
            return download_url
        elif status == "Fail" or status == "Unknown":
            print("---------------生成失败---------------")
            raise Exception('生成失败')
        
        time.sleep(10)