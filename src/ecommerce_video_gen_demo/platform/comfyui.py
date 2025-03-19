import os
from io import BytesIO
import requests
import json
from time import time, sleep
from typing import Dict
from ecommerce_video_gen_demo.utils.file_utils import generate_timestamp_filename
import PIL

def get_comfyui_base_url():
    return os.getenv('COMFYUI_BASE_URL', '')

def upload_image(image: PIL.Image.Image):
    byte_io = BytesIO()
    image.save(byte_io, format='PNG')
    byte_io.seek(0)

    url = f'{get_comfyui_base_url()}/api/upload/image'
    files = { 'image': (f'{generate_timestamp_filename()}.png', byte_io, 'image/png') }
    
    resp = requests.post(url, files=files)
    print('----上传结果----')
    print(resp.text)
    return resp.json()

def get_image(filename, subfolder, folder_type):
    data = {'filename': filename, 'subfolder': subfolder, 'type': folder_type}
    resp = requests.get(f'{get_comfyui_base_url()}/view', params=data)

    print(resp.request.url)


    image_data = BytesIO(resp.content)
    image = PIL.Image.open(image_data)

    return image

def get_history_api(prompt_id: str):
        resp = requests.get(f'{get_comfyui_base_url()}/history/{prompt_id}')
        return resp.json()

def run_prompt_api(prompt: Dict) -> Dict:
    p = {'prompt': prompt}
    data = json.dumps(p).encode('utf-8')
    resp =  requests.post(f'{get_comfyui_base_url()}/prompt', data=data)

    return resp.json()

def wait_for_image(prompt_id: str, timeout: int = 30):
    start_time = time()
    while True:
        history_result = get_history_api(prompt_id)
        history = history_result.get(prompt_id, None)
        
        if (history):
            return True

        current_time = time()
        sleep(1)
        if (current_time - start_time > timeout):
            return False



def run_workflow(prompt: Dict):
    ret = run_prompt_api(prompt)
    prompt_id = ret.get('prompt_id') 

    if (not prompt_id):
        raise Exception('prompt_id is None')

    wait_result = wait_for_image(prompt_id)

    if (not wait_result):
        raise Exception('request timeout')

    
    history_result = get_history_api(prompt_id)
    history = history_result.get(prompt_id, None)

    output_images = []

    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        images_output = []
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)

        output_images.append({
            'node_id': node_id,
            'images': images_output
        })

    return output_images



    
