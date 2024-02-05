import gradio as gr
import comfy_generate as comfy
import prefs
import random

prefs.init()

file = open("notes.md", "r")
notes = file.read()
file.close()

def randomize_seed():
    print("Randomizing seed")
    seed.value = random.randint(1, 18446744073709551614)
    print(seed.value)
    return seed.value

def generate(url, model, pos, neg, dimensions, direction, batch, seed, steps, cfg, sampler_name, scheduler, clip, b1, b2, s1, s2, rescale, progress=gr.Progress()):
    width, height = dimensions.split("x")

    if direction == "Portrait":
        width, height = height, width
    width, height = int(width), int(height)

    comfy.connect(url)
    comfy.set_checkpoint(model)
    comfy.set_dimensions([width, height], batch)
    comfy.set_prompt(pos, neg)

    comfy.set_sampler(seed, steps, cfg, sampler_name, scheduler, 1.0)
    comfy.set_freeu([b1, b2, s1, s2])
    comfy.set_rescale(rescale)
    comfy.set_clip(clip)

    prefs.set_config(url, model, pos, neg, dimensions, direction, batch, seed, steps, cfg, sampler_name, scheduler, clip, b1, b2, s1, s2, rescale)

    progress(0, "Getting Images")
    images = comfy.get_images(progress)

    progress(50, "Collecting images")
    return comfy.images_to_pil(images)

with gr.Blocks(title = "Fluffy UI", theme = "gradio/glass") as tab:
    with gr.Row(equal_height = True):
        with gr.Column():
            with gr.Row():
                url = gr.Textbox(label="Server URL", value = prefs.config["main"]["url"])
                model = gr.Textbox(label="Model", value = prefs.config["main"]["model"])
            pos = gr.Textbox(label="Positive Prompt", value = prefs.config["main"]["pos"])
            neg = gr.Textbox(label="Negative Prompt", value = prefs.config["main"]["neg"])

            with gr.Column():
                with gr.Row():
                    dimensions = gr.Dropdown(label = "Dimensions", value = prefs.config["main"]["dimensions"], multiselect= False, choices = ["1024x1024", "1152x896", "1216x832", "1344x768", "1536x640"])
                    direction = gr.Dropdown(label = "Direction", value = prefs.config["main"]["direction"], multiselect= False, choices = ["Portrait", "Landscape"])
                    batch_size = gr.Number(label="Batch Size", value = prefs.config["main"]["batch"], step = 1, minimum = 1, precision = 0)
                with gr.Row():
                    seed = gr.Number(label="Seed", value = prefs.config["main"]["seed"], step = 1, minimum = 0, maximum = 18446744073709551614, precision = 0, scale = 2)
                    rand_button = gr.Button("Randomize", size = 'sm', scale = 1, min_width = 0)
                    steps = gr.Number(label="Steps", value = prefs.config["main"]["steps"], step = 1, minimum = 1, maximum = 1000, precision = 0, scale = 1, min_width = 0)
                    cfg = gr.Number(label="cfg", value = prefs.config["main"]["cfg"], step = 0.1, minimum = 1, maximum = 20, precision = 1, scale = 1, min_width = 0)
                    rand_button.click(randomize_seed, outputs = [seed])

            with gr.Row():
                sampler_name = gr.Dropdown(label="sampler_name", value = prefs.config["main"]["sampler_name"], multiselect= False, choices=["euler", "euler_ancestral", "heun", "heunpp2","dpm_2", "dpm_2_ancestral", "lms", "dpm_fast", "dpm_adaptive", "dpmpp_2s_ancestral", "dpmpp_sde", "dpmpp_sde_gpu", "dpmpp_2m", "dpmpp_2m_sde", "dpmpp_2m_sde_gpu", "dpmpp_3m_sde", "dpmpp_3m_sde_gpu", "ddpm", "lcm", "ddim", "uni_pc", "uni_pc_bh2"])

                scheduler = gr.Dropdown(label="scheduler", value = prefs.config["main"]["scheduler"], multiselect= False, choices = ["normal", "karras", "exponential", "sgm_uniform","simple","ddim_uniform"])

                clip = gr.Number(label="clip", value = prefs.config["main"]["clip"], step = 1, minimum = -10, maximum = 10, precision = 1)

            with gr.Accordion(label = "FreeU & CFG Rescale", open = False):
                gr.Markdown("The standard FreeU values for XL models are b1=1.3, b2=1.4, s1=0.9, s2=0.2. Changing these values can affect the detail on the generated images.")
                with gr.Row():
                    b1 = gr.Number(label="B1", value = prefs.config["main"]["b1"], step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
                    b2 = gr.Number(label="B2", value = prefs.config["main"]["b2"], step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
                    s1 = gr.Number(label="S1", value = prefs.config["main"]["s1"], step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
                    s2 = gr.Number(label="S2", value = prefs.config["main"]["s2"], step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
                rescale = gr.Number(label="CFG Rescale", value = prefs.config["main"]["rescale"], step = 0.1, minimum = 0.1, maximum = 2.0, precision = 1, min_width = 0)
            btn = gr.Button("Generate")

        with gr.Column():
            generated_image = gr.Gallery(label="Generated Images")
            gr.Markdown(notes)
        
    btn.click(generate, inputs = [url, model, pos, neg, dimensions, direction, batch_size, seed, steps, cfg, sampler_name, scheduler, clip, b1, b2, s1, s2, rescale], outputs = [generated_image])
