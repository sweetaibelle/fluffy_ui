# Save trouble of reloading workflow from a file every time.

workflow = """
{
  "2": {
    "inputs": {
      "ckpt_name": "XL/ponyDiffusionV6XL_v6.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "3": {
    "inputs": {
      "seed": 0,
      "steps": 1e+23,
      "cfg": 50,
      "sampler_name": "dpmpp_3m_sde_gpu",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "22",
        0
      ],
      "positive": [
        "12",
        0
      ],
      "negative": [
        "18",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "5": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "6": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "2",
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
  },
  "12": {
    "inputs": {
      "text": "pos",
      "clip": [
        "33",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "18": {
    "inputs": {
      "text": "neg",
      "clip": [
        "33",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "21": {
    "inputs": {
      "multiplier": 0.7,
      "model": [
        "2",
        0
      ]
    },
    "class_type": "RescaleCFG",
    "_meta": {
      "title": "RescaleCFG"
    }
  },
  "22": {
    "inputs": {
      "b1": 1.3,
      "b2": 1.4,
      "s1": 0.9,
      "s2": 0.2,
      "model": [
        "21",
        0
      ]
    },
    "class_type": "FreeU_V2",
    "_meta": {
      "title": "FreeU_V2"
    }
  },
  "33": {
    "inputs": {
      "stop_at_clip_layer": -2,
      "clip": [
        "2",
        1
      ]
    },
    "class_type": "CLIPSetLastLayer",
    "_meta": {
      "title": "CLIP Set Last Layer"
    }
  }
}
"""