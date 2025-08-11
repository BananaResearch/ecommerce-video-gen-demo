from ecommerce_video_gen_demo.utils.random_utils import gen_sd_seed


def get_prompt_info(prompt: str, width: int, height: int):
    prompt_dict = {
        "8": {
            "inputs": {
            "samples": [
                "31",
                0
            ],
            "vae": [
                "39",
                0
            ]
            },
            "class_type": "VAEDecode",
            "_meta": {
            "title": "VAE Decode"
            }
        },
        "9": {
            "inputs": {
            "filename_prefix": "flux_krea/flux_krea",
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
        "31": {
            "inputs": {
            "seed": gen_sd_seed(),
            "steps": 20,
            "cfg": 1,
            "sampler_name": "euler",
            "scheduler": "simple",
            "denoise": 1,
            "model": [
                "38",
                0
            ],
            "positive": [
                "45",
                0
            ],
            "negative": [
                "42",
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
        "38": {
            "inputs": {
            "unet_name": "flux1-krea-dev_fp8_scaled.safetensors",
            "weight_dtype": "default"
            },
            "class_type": "UNETLoader",
            "_meta": {
            "title": "Load Diffusion Model"
            }
        },
        "39": {
            "inputs": {
            "vae_name": "ae.safetensors"
            },
            "class_type": "VAELoader",
            "_meta": {
            "title": "Load VAE"
            }
        },
        "40": {
            "inputs": {
            "clip_name1": "clip_l.safetensors",
            "clip_name2": "t5xxl_fp16.safetensors",
            "type": "flux",
            "device": "default"
            },
            "class_type": "DualCLIPLoader",
            "_meta": {
            "title": "DualCLIPLoader"
            }
        },
        "42": {
            "inputs": {
            "conditioning": [
                "45",
                0
            ]
            },
            "class_type": "ConditioningZeroOut",
            "_meta": {
            "title": "ConditioningZeroOut"
            }
        },
        "45": {
            "inputs": {
            "text": prompt,
            "clip": [
                "40",
                0
            ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
            "title": "CLIP Text Encode (Prompt)"
            }
        }
    }

    result_node = '9'
    
    return {
        "prompt": prompt_dict,
        "result_node_id": result_node,
    }

    
