import gradio as gr
import requests

# 假设 comfyui 的图片生成接口地址如下
COMFYUI_URL = "http://127.0.0.日讯:8000/generate_image"

def generate_image(text_input):
    """
    通过向ComfyUI的API发送POST请求，提交文本数据并获取返回的图片。
    """
    response = requests.post(COMFYUI_URL, json={"text": text_input})
    
    if response.status_code == 200:
        # 假设响应中包含图片的二进制数据
        image_data = response.content
        return image_data
    else:
        # 如果请求失败，打印错误信息或处理错误
        print(f"Error: Unable to generate image - {response.status_code}")
        return None

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

def main(*,server_port):
    with gr.Blocks() as demo:
        gr.Markdown("# 生成模特素材")
        gr.Markdown("生成模特")
        
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(label="输入提示", lines=3)
                generate_button = gr.Button("生成")

            with gr.Column():
                output_image = gr.Image(label="输出图像")
                generate_button.click(fn=generate_image, inputs=prompt_input, outputs=output_image)
            
        gr.Markdown("## 从图片生成视频")
        
        generate_video_from_image_ui()



    demo.launch(server_port=server_port, root_path='/videogen')

# 启动应用
if __name__ == "__main__":
    main(server_port=7860)