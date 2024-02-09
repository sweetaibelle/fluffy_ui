import json
import os

config = {}
config_name = "config.json"

def init():
    global config
    if os.path.exists(config_name):
        config = json.load(open(config_name))
    else:
        config = json.load(open('default_prefs.json'))

def set_config(url, model, pos, neg, dimensions, direction, batch, seed, steps, cfg, sampler_name, scheduler, clip, b1, b2, s1, s2, rescale):
    global config
    config["main"] = {}
    config["main"]["url"] = url
    config["main"]["model"] = model
    config["main"]["pos"] = pos
    config["main"]["neg"] = neg
    config["main"]["dimensions"] = dimensions
    config["main"]["direction"] = direction
    config["main"]["batch"] = batch
    config["main"]["seed"] = seed
    config["main"]["steps"] = steps
    config["main"]["cfg"] = cfg
    config["main"]["sampler_name"] = sampler_name
    config["main"]["scheduler"] = scheduler
    config["main"]["clip"] = clip
    config["main"]["b1"] = b1
    config["main"]["b2"] = b2
    config["main"]["s1"] = s1
    config["main"]["s2"] = s2
    config["main"]["rescale"] = rescale
    with open(config_name, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
