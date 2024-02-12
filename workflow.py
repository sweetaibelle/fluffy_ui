# Save trouble of reloading workflow from a file every time.

def get_ckpt_node(id, name):
  # "2", "XL/ponyDiffusionV6XL_v6.safetensors"

  node = {}
  node[id] = {}
  node[id]["inputs"] = {}
  node[id]["class_type"] = "CheckpointLoaderSimple"
  node[id]["_meta"] = {}
  node[id]["_meta"]["title"] = "Load Checkpoint"

  node[id]["inputs"]["ckpt_name"] = name

  return node

def get_ksampler_node(id, seed, steps, cfg, sampler_name, scheduler, denoise, model_node, pos_node, neg_node, latent_node):
  # "3", 0, 30, 7, "dpmpp_3m_sde_gpu", "karras", 1, "22", "12", "18", "5"

  node = {}
  node[id] = {}
  node[id]["inputs"] = {}
  node[id]["class_type"] = "KSampler"
  node[id]["_meta"] = {}
  node[id]["_meta"]["title"] = "KSampler"

  node[id]["inputs"]["seed"] = seed
  node[id]["inputs"]["steps"] = steps
  node[id]["inputs"]["cfg"] = cfg
  node[id]["inputs"]["sampler_name"] = sampler_name
  node[id]["inputs"]["scheduler"] = scheduler
  node[id]["inputs"]["denoise"] = denoise
  node[id]["inputs"]["model_node"] = model_node
  node[id]["inputs"]["pos_node"] = pos_node
  node[id]["inputs"]["neg_node"] = neg_node
  node[id]["inputs"]["latent_node"] = latent_node

  return node

def get_empty_latent_node(id, width, height, batch_size):
  # "5", 1024, 1024, 1

  node = {}
  node[id] = {}
  node[id]["inputs"] = {}
  node[id]["class_type"] = "EmptyLatentImage"
  node[id]["_meta"] = {}
  node[id]["_meta"]["title"] = "Empty Latent Image"

  node[id]["inputs"]["width"] = width
  node[id]["inputs"]["height"] = height
  node[id]["inputs"]["batch_size"] = batch_size

  return node

def get_vae_node(id, samples_node, vae_node):
  # "6", "3", "2"
  node = {}
  node[id] = {}
  node[id]["inputs"] = {}
  node[id]["class_type"] = "VAEDecode"
  node[id]["_meta"] = {}
  node[id]["_meta"]["title"] = "VAE Decode"

  node[id]["inputs"]["samples"] = samples_node
  node[id]["inputs"]["vae"] = vae_node

  return node

def get_preview_node(id, image_node):
  # "7", "6"

  node = {}
  node[id] = {}
  node[id]["inputs"] = {}
  node[id]["class_type"] = "PreviewImage"
  node[id]["_meta"] = {}
  node[id]["_meta"]["title"] = "Preview Image"

  node[id]["inputs"]["images"] = image_node

  return node

def get_clip_node(id, prompt, clip_node):
  # pos: "12", "pos", "33"
  # neg: "18", "neg", "33"

  node = {}
  node[id] = {}
  node[id]["inputs"] = {}
  node[id]["class_type"] = "CLIPTextEncode"
  node[id]["_meta"] = {}
  node[id]["_meta"]["title"] = "CLIP Text Encode (Prompt)"

  node[id]["inputs"]["text"] = prompt
  node[id]["inputs"]["clip"] = clip_node

  return node

def rescale_node(id, mult, model_node):
  # "21", "0.7", "22"

  node = {}
  node[id] = {}
  node[id]["inputs"] = {}
  node[id]["class_type"] = "RescaleCFG"
  node[id]["_meta"] = {}
  node[id]["_meta"]["title"] = "RescaleCFG"

  node[id]["inputs"]["multiplier"] = mult
  node[id]["inputs"]["model"] = model_node

  return node

def get_freeu_node(id, b1, b2, s1, s2, model_node):
  # "22", 1.3, 1.4, 0.9, 0.2, "2"

  node = {}
  node[id] = {}
  node[id]["inputs"] = {}
  node[id]["class_type"] = "FreeU_V2"
  node[id]["_meta"] = {}
  node[id]["_meta"]["title"] = "FreeU_V2"

  node[id]["inputs"]["b1"] = b1
  node[id]["inputs"]["b2"] = b2
  node[id]["inputs"]["s1"] = s1
  node[id]["inputs"]["s2"] = s2
  node[id]["inputs"]["model"] = model_node

  return node

def get_clip_set_node(id, clip_layer, clip_node):
  # "33", -2, "2"

  node = {}
  node[id] = {}
  node[id]["inputs"] = {}
  node[id]["class_type"] = "CLIPSetLastLayer"
  node[id]["_meta"] = {}
  node[id]["_meta"]["title"] = "CLIP Set Last Layer"

  node[id]["inputs"]["stop_at_clip_layer"] = clip_layer
  node[id]["inputs"]["clip"] = clip_node

  return node

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
      "steps": 30,
      "cfg": 7,
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
        "22",
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
        "2",
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