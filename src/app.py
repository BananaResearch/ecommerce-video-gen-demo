import loadenv
import gradio as gr
from ecommerce_video_gen_demo.platform.comfyui import run_workflow
from ecommerce_video_gen_demo.utils.random_utils import gen_sd_seed
import os

# 假设 comfyui 的图片生成接口地址如下
COMFYUI_URL = os.getenv('COMFYUI_BASE_URL')
print(f'COMFYUI_URL: {COMFYUI_URL}')


def generate_image(text_input, width, height):
    print(f'generate_image. {width}, {height}')
    prompt = {
        "1": {
            "inputs": {
                "ckpt_name": "sd_xl_turbo_1.0_fp16.safetensors"
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {
                "title": "Load Checkpoint"
            }
        },
        "2": {
            "inputs": {
                "text": text_input,
                "clip": [
                    "1",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Prompt)"
            }
        },
        "3": {
            "inputs": {
                "text": "text, water",
                "clip": [
                    "1",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Prompt)"
            }
        },
        "4": {
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage",
            "_meta": {
                "title": "Empty Latent Image"
            }
        },
        "5": {
            "inputs": {
                "seed": gen_sd_seed(),
                "steps": 20,
                "cfg": 8,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": [
                    "1",
                    0
                ],
                "positive": [
                    "2",
                    0
                ],
                "negative": [
                    "3",
                    0
                ],
                "latent_image": [
                    "4",
                    0
                ]
            },
            "class_type": "KSampler",
            "_meta": {
                "title": "KSampler"
            }
        },
        "6": {
            "inputs": {
                "samples": [
                    "5",
                    0
                ],
                "vae": [
                    "1",
                    2
                ]
            },
            "class_type": "VAEDecode",
            "_meta": {
                "title": "VAE Decode"
            }
        },
        "7": {
            "inputs": {
                "images": [
                    "6",
                    0
                ]
            },
            "class_type": "PreviewImage",
            "_meta": {
                "title": "Preview Image"
            }
        }
    }

    result = run_workflow(prompt)

    print(result)
    return result[0].get('images')[0]


def generate_video_from_image(image_file_path: str):
    pass


def generate_video_from_image_ui():
    with gr.Row():
        with gr.Column():
            image_upload = gr.Image(type="pil", label="上传图片")
            generate_video_button = gr.Button("生成视频")

        with gr.Column():
            output_video = gr.Video(label="输出视频")
            download_button = gr.Button("下载视频")

        def update_download_link(video_data):
            return gr.File.update(value=video_data, visible=True)

        generate_video_button.click(
            fn=generate_video_from_image,
            inputs=image_upload,
            outputs=output_video
        ).then(
            fn=update_download_link,
            inputs=output_video,
            outputs=download_button
        )


def generate_try_on_ui():
    pass


def main(*, server_port):
    with gr.Blocks() as demo:
        gr.Markdown("# 生成模特素材")
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(label="输入提示", lines=3)
                width_input = gr.Number(label='宽度', value=512)
                height_input = gr.Number(label='高度', value=1024)
                generate_button = gr.Button("生成")

            with gr.Column():
                output_image = gr.Image(label="输出图像")
                generate_button.click(
                    fn=generate_image, inputs=[prompt_input, width_input, height_input], outputs=output_image)

        gr.Markdown("## 从图片生成视频")

        generate_video_from_image_ui()

    demo.launch(server_port=server_port, root_path='/videogen')


# 启动应用
if __name__ == "__main__":
    # test_comfyui()
    main(server_port=7860)
