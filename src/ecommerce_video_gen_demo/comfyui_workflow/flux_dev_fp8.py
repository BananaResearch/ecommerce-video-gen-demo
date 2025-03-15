from ecommerce_video_gen_demo.utils.random_utils import gen_sd_seed


def get_prompt_info(prompt: str, width: int, height: int):
    prompt_dict = {
        "6": {
            "inputs": {
                "text": prompt,
                "clip": [
                    "30",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Positive Prompt)"
            }
        },
        "8": {
            "inputs": {
                "samples": [
                    "31",
                    0
                ],
                "vae": [
                    "30",
                    2
                ]
            },
            "class_type": "VAEDecode",
            "_meta": {
                "title": "VAE Decode"
            }
        },
        "9": {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": [
                    "8",
                    0
                ]
            },
            "class_type": "SaveImage",
            "_meta": {
                "title": "Save Image"
            }
        },
        "27": {
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            },
            "class_type": "EmptySD3LatentImage",
            "_meta": {
                "title": "EmptySD3LatentImage"
            }
        },
        "30": {
            "inputs": {
                "ckpt_name": "flux1-dev-fp8.safetensors"
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {
                "title": "Load Checkpoint"
            }
        },
        "31": {
            "inputs": {
                "seed": gen_sd_seed(),
                "steps": 20,
                "cfg": 1,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1,
                "model": [
                    "30",
                    0
                ],
                "positive": [
                    "35",
                    0
                ],
                "negative": [
                    "33",
                    0
                ],
                "latent_image": [
                    "27",
                    0
                ]
            },
            "class_type": "KSampler",
            "_meta": {
                "title": "KSampler"
            }
        },
        "33": {
            "inputs": {
                "text": "",
                "clip": [
                    "30",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Negative Prompt)"
            }
        },
        "35": {
            "inputs": {
                "guidance": 2,
                "conditioning": [
                    "6",
                    0
                ]
            },
            "class_type": "FluxGuidance",
            "_meta": {
                "title": "FluxGuidance"
            }
        }
    }

    result_node = '9'
    
    return {
        "prompt": prompt_dict,
        "result_node_id": result_node,
    }

    
