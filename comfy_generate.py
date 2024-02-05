import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
from urllib import request, parse
import workflow

server_url = ""

# Generate a random client id
client_id = str(uuid.uuid4())

# open websocket connection
ws = websocket.WebSocket()

# Load the workflow from file
#comfy_workflow = json.load(open('workflow_api_2.json'))
comfy_workflow = json.loads(workflow.workflow)

# Functions to interact with the server

def connect(url):
    global server_url
    server_url = url
    print ("Connecting to server at", server_url)
    ws.connect("ws://{}/ws?clientId={}".format(server_url, client_id))

def queue():
    p = {"prompt": comfy_workflow, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://{}/prompt".format(server_url), data=data)
    return json.loads(request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = parse.urlencode(data)
    with request.urlopen("http://{}/view?{}".format(server_url, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with request.urlopen("http://{}/history/{}".format(server_url, prompt_id)) as response:
        return json.loads(response.read())
    
def get_images():
    print ("Sending prompt to ComfyUI.")
    prompt_id = queue()['prompt_id']
    output_images = {}

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            # print(message)
            # type -> progress will have 'value' and 'max' in the data, for a progress bar.
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data
    
    print ("Execution is done. Fetching images.")
    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

def save_images(images, prefix):
    print ("Saving images.")
    for i, image_data in enumerate(images["7"]):
        with open(f"{prefix}_{i}.png", "wb") as f:
            f.write(image_data)

# Functions to edit the workflow
            
def set_checkpoint(checkpoint):
    comfy_workflow["2"]["inputs"]["ckpt_name"] = checkpoint

def set_dimensions(dim, batch_size=1):
    comfy_workflow["5"]["inputs"]["width"] = dim[0]
    comfy_workflow["5"]["inputs"]["height"] = dim[1]
    comfy_workflow["5"]["inputs"]["batch_size"] = batch_size

def set_prompt(pos, neg):
    comfy_workflow["12"]["inputs"]["text"] = pos
    comfy_workflow["18"]["inputs"]["text"] = neg

def set_sampler(seed, steps, cfg, sampler_name, scheduler, denoise=1):
    comfy_workflow["3"]["inputs"]["seed"] = seed
    comfy_workflow["3"]["inputs"]["steps"] = steps
    comfy_workflow["3"]["inputs"]["cfg"] = cfg
    comfy_workflow["3"]["inputs"]["sampler_name"] = sampler_name
    comfy_workflow["3"]["inputs"]["scheduler"] = scheduler
    comfy_workflow["3"]["inputs"]["denoise"] = denoise

def set_freeu(freeu):
    comfy_workflow["22"]["inputs"]["b1"] = freeu[0]
    comfy_workflow["22"]["inputs"]["b2"] = freeu[1]
    comfy_workflow["22"]["inputs"]["s1"] = freeu[2]
    comfy_workflow["22"]["inputs"]["s2"] = freeu[3]

def set_rescale(rescale):
    comfy_workflow["21"]["inputs"]["rescale"] = rescale

def set_clip(clip):
    comfy_workflow["33"]["inputs"]["stop_at_clip_layer"] = clip

def set_filename_prefix(prefix):
    comfy_workflow["17"]["inputs"]["filename_prefix"] = prefix


