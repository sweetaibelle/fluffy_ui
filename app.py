import comfy_generate as comfy
import random
import gradio as gr
from PIL import Image
import io

file = open("notes.md", "r")
notes = file.read()
file.close()

def randomize_seed():
    print("Randomizing seed")
    seed.value = random.randint(1, 18446744073709551614)
    print(seed.value)
    return seed.value

def generate(url, model, pos, neg, dimensions, direction, batch, seed, steps, cfg, sampler_name, scheduler, clip, b1, b2, s1, s2, rescale):
    width, height = dimensions.split("x")

    if direction == "Portrait":
        width, height = height, width
    width, height = int(width), int(height)

    comfy.connect(url)
    comfy.set_checkpoint(model)
    comfy.set_dimensions([width, height], batch)
    comfy.set_prompt(pos, neg)

    #seed = random.randint(1, 18446744073709551614)
    comfy.set_sampler(seed, steps, cfg, sampler_name, scheduler, 1.0)
    comfy.set_freeu([b1, b2, s1, s2])
    comfy.set_rescale(rescale)
    comfy.set_clip(clip)

    images = comfy.get_images()
    images_pil = []

    for i, image_data in enumerate(images["7"]):
        image = Image.open(io.BytesIO(image_data))
        images_pil.append(image)
    
    return images_pil

with gr.Blocks(title = "Fluffy UI", theme = "gradio/glass") as demo:
    gr.Markdown("""
                ## Fluffy UI
                This is a simpler UI for generating images using the Comfy API. You'll need to have the Comfy API running, and put the server name/port in the "Server URL" field. "127.0.0.1:8188" is default if its running on your local computer.
                
                The model field should have the exact name of the model you want to use, including any subfolders. The text below the output can be customized by editing notes.md.
                """)
    with gr.Row(equal_height = True):
        with gr.Column():
            with gr.Row():
                url = gr.Textbox(label="Server URL", value = "127.0.0.1:8188")
                model = gr.Textbox(label="Model", value = "XL/ponyDiffusionV6XL_v6.safetensors")
            pos = gr.Textbox(label="Positive Prompt", value = "source_9, cute pony, unicorn Sweetie Belle lying on her bed reading a book, beautiful, innocent, fluffy, furry, soft lighting, full body, detailed, god rays, countershading")
            neg = gr.Textbox(label="Negative Prompt", value = "sfm, blender, 3d")

            with gr.Column():
                with gr.Row():
                    dimensions = gr.Dropdown(label = "Dimensions", value = "1024x1024", multiselect= False, choices = ["1024x1024", "1152x896", "1216x832", "1344x768", "1536x640"])
                    direction = gr.Dropdown(label = "Direction", value = "Landscape", multiselect= False, choices = ["Portrait", "Landscape"])
                    batch_size = gr.Number(label="Batch Size", value = 1, step = 1, minimum = 1, precision = 0)
                with gr.Row():
                    seed = gr.Number(label="Seed", value = 0, step = 1, minimum = 0, maximum = 18446744073709551614, precision = 0, scale = 2)
                    rand_button = gr.Button("Randomize", size = 'sm', scale = 1, min_width = 0)
                    steps = gr.Number(label="Steps", value = 50, step = 1, minimum = 1, maximum = 1000, precision = 0, scale = 1, min_width = 0)
                    cfg = gr.Number(label="cfg", value = 7, step = 0.1, minimum = 1, maximum = 20, precision = 1, scale = 1, min_width = 0)
                    rand_button.click(randomize_seed, outputs = [seed])

            with gr.Row():
                sampler_name = gr.Dropdown(label="sampler_name", value = "dpmpp_3m_sde_gpu", multiselect= False, choices=["euler", "euler_ancestral", "heun", "heunpp2","dpm_2", "dpm_2_ancestral", "lms", "dpm_fast", "dpm_adaptive", "dpmpp_2s_ancestral", "dpmpp_sde", "dpmpp_sde_gpu", "dpmpp_2m", "dpmpp_2m_sde", "dpmpp_2m_sde_gpu", "dpmpp_3m_sde", "dpmpp_3m_sde_gpu", "ddpm", "lcm", "ddim", "uni_pc", "uni_pc_bh2"])

                scheduler = gr.Dropdown(label="scheduler", value = "karras", multiselect= False, choices = ["normal", "karras", "exponential", "sgm_uniform","simple","ddim_uniform"])

                clip = gr.Number(label="clip", value = -2, step = 1, minimum = -10, maximum = 10, precision = 1)

            with gr.Accordion(label = "FreeU & CFG Rescale", open = False):
                gr.Markdown("The standard FreeU values for XL models are b1=1.3, b2=1.4, s1=0.9, s2=0.2. Changing these values can affect the detail on the generated images.")
                with gr.Row():
                    b1 = gr.Number(label="B1", value = 1.3, step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
                    b2 = gr.Number(label="B2", value = 1.4, step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
                    s1 = gr.Number(label="S1", value = 0.9, step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
                    s2 = gr.Number(label="S2", value = 0.2, step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
                rescale = gr.Number(label="CFG Rescale", value = 0.7, step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
            btn = gr.Button("Generate")

        with gr.Column():
            generated_image = gr.Gallery(label="Generated Images")
            gr.Markdown(notes)
        
    btn.click(generate, inputs = [url, model, pos, neg, dimensions, direction, batch_size, seed, steps, cfg, sampler_name, scheduler, clip, b1, b2, s1, s2, rescale], outputs = [generated_image])

if __name__ == "__main__":
    demo.launch() 
