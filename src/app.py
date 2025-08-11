import gradio as gr
from PIL import Image
from fastapi import FastAPI, APIRouter
import uvicorn
from ecommerce_video_gen_demo.platform.comfyui import run_workflow, upload_image
from ecommerce_video_gen_demo.platform.minmax import generate_video_from_image as gvfi
from ecommerce_video_gen_demo.utils.image_utils import img_to_base64
from ecommerce_video_gen_demo.comfyui_workflow.flux_dev_fp8 import get_prompt_info
from ecommerce_video_gen_demo.comfyui_workflow.replace_background import get_prompt_info as replace_bg_prompt_info, IMAGE_SIZE_LIST
import os
from wechat_assistant.bw_appinfo import init_app_info
from wechat_assistant.faq_assistant import router as faq_router
from ecommerce_video_gen_demo.utils.logger import setup_logger

from dotenv import load_dotenv, find_dotenv

# 初始化日志记录器
logger = setup_logger(__name__)
load_dotenv(find_dotenv())
init_app_info()

app = FastAPI()

# 假设 comfyui 的图片生成接口地址如下
COMFYUI_URL = os.getenv('COMFYUI_BASE_URL')
logger.info(f'COMFYUI_URL: {COMFYUI_URL}')


def generate_image(text_input, width, height):
    input = text_input + \
        'This is a high quality,diffuse light,highly detailed,4k,realistic people photograph.'

    prompt_info = get_prompt_info(input, width, height)
    prompt = prompt_info.get('prompt', {})
    result_node_id = prompt_info.get('result_node_id')
    result = run_workflow(prompt)

    node_result = next(
        (node for node in result if node['node_id'] == result_node_id), None)

    if (node_result is None):
        raise Exception('未找到结果')

    return node_result.get('images')[0]


def generate_video_from_image(img, prompt: str):
    if not img:
        raise gr.Error('未上传图片')

    if not prompt:
        raise gr.Error('未输入指令')

    return gvfi(img_to_base64(img), prompt)


def generate_video_from_image_ui():
    gr.Markdown("## 从图片生成视频")
    with gr.Row():
        with gr.Column():
            image_upload = gr.Image(type="pil", label="上传图片")
            prompt_input = gr.Textbox(label="输入提示词", lines=3)

            gr.HTML(
                '<a href="https://vrfi1sk8a0.feishu.cn/wiki/WosowbIXtiZpZRkmiH9cZ2R6nUf" target="_blank">运镜指令说明</a>')

            generate_video_button = gr.Button("生成视频")

        with gr.Column():
            output_video = gr.Video(label="输出视频")

        generate_video_button.click(
            fn=generate_video_from_image,
            inputs=[image_upload, prompt_input],
            outputs=output_video
        )


def generate_try_on_ui():
    gr.HTML('<hr>')
    gr.Markdown("# AI 换衣")
    gr.HTML(
        "<a href='https://catvton.baresearch.cn/' target='_blank'>AI 换装</a>")


def generate_remove_bg(image: Image.Image):
    logger.info('remove_bg')
    result = upload_image(image)
    file_name = result.get('name')

    prompt = {
        "1": {
            "inputs": {
                "images": [
                    "3",
                    0
                ]
            },
            "class_type": "PreviewImage",
            "_meta": {
                "title": "Preview Image"
            }
        },
        "2": {
            "inputs": {
                "image": file_name
            },
            "class_type": "LoadImage",
            "_meta": {
                "title": "Load Image"
            }
        },
        "3": {
            "inputs": {
                "model": "RMBG-2.0",
                "sensitivity": 1,
                "process_res": 1024,
                "mask_blur": 0,
                "mask_offset": 0,
                "background": "Alpha",
                "invert_output": False,
                "optimize": "default",
                "refine_foreground": False,
                "image": [
                    "2",
                    0
                ]
            },
            "class_type": "RMBG",
            "_meta": {
                "title": "Remove Background (RMBG)"
            }
        },
        "4": {
            "inputs": {
                "mask": [
                    "3",
                    1
                ]
            },
            "class_type": "LayerMask: MaskPreview",
            "_meta": {
                "title": "LayerMask: MaskPreview"
            }
        }
    }

    result = run_workflow(prompt)

    logger.info(f'result: {result}')
    return result[1].get('images')[0]


def generate_remove_bg_ui():
    gr.HTML('<hr>')
    gr.Markdown("# 去除背景")

    with gr.Row():
        with gr.Column():
            image_upload = gr.Image(type="pil", label="上传图片")
            generate_button = gr.Button("去除背景")
        with gr.Column():
            output_image = gr.Image(label="输出图片", format='png')

        generate_button.click(fn=generate_remove_bg, inputs=[
                              image_upload], outputs=output_image)


def generate_replace_bg_ui():
    gr.HTML('<hr>')
    gr.Markdown("# 替换背景")

    def generate_replace_bg(image: Image.Image, prompt: str, height: int, resolution: str):
        if not image:
            raise gr.Error('未上传图片')

        if not prompt:
            raise gr.Error('未输入指令')

        if height < 500:
            raise gr.Error('高度过低')

        if height > 2000:
            raise gr.Error('高度过高')

        result = upload_image(image)
        image_name = result.get('name')

        prompt_info = replace_bg_prompt_info(
            image_name, prompt, height, resolution)
        prompt = prompt_info.get('prompt', {})
        result_node_id = prompt_info.get('result_node_id')
        result = run_workflow(prompt)

        node_result = next(
            (node for node in result if node['node_id'] == result_node_id), None)
        logger.info(f'replace bg result: {node_result}')

        if (node_result is None):
            raise Exception('未找到结果')

        return node_result.get('images')[0]

    with gr.Row():
        with gr.Column():
            image_upload = gr.Image(type="pil", label="上传图片")
            prompt_input = gr.Textbox(label="输入新背景提示词(只能使用英文)", lines=4)
            height = gr.Number(label='输入图片重绘高度', value=1368)
            resolution = gr.Dropdown(IMAGE_SIZE_LIST, label='生成图片尺寸', )
            generate_button = gr.Button("替换背景")
        with gr.Column():
            output_image = gr.Image(label="输出图片", format='png')

            generate_button.click(fn=generate_replace_bg, inputs=[
                                  image_upload, prompt_input, height, resolution], outputs=output_image)


def main(*, server_port):
    with gr.Blocks() as demo1:
        gr.Markdown("# 生成模特素材")
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(label="输入提示词(只能使用英文)", lines=3)
                width_input = gr.Number(label='宽度', value=768)
                height_input = gr.Number(label='高度', value=1368)
                generate_button = gr.Button("生成")

            with gr.Column():
                output_image = gr.Image(label="输出图片", format="png")
                generate_button.click(
                    fn=generate_image, inputs=[prompt_input, width_input, height_input], outputs=output_image)

        generate_try_on_ui()
        generate_remove_bg_ui()
        generate_replace_bg_ui()

    with gr.Blocks() as demo2:
        generate_video_from_image_ui()

    gr.mount_gradio_app(app, demo1, path="/videogen")
    gr.mount_gradio_app(app, demo2, path="/videogenpro")

    api_router = APIRouter(prefix='/vg-api')
    api_router.include_router(faq_router)
    app.include_router(api_router)

    uvicorn.run(app, host="0.0.0.0", port=server_port)


# 启动应用
if __name__ == "__main__":
    # test_comfyui()
    main(server_port=7860)
