import gradio as gr
import main
import notes

with gr.Blocks(title = "Fluffy UI", theme = "gradio/glass") as demo:
    gr.Markdown("""
                ## Fluffy UI
                This is a simpler UI for generating images using the Comfy API. You'll need to have the Comfy API running, and put the server name/port in the "Server URL" field. "127.0.0.1:8188" is default if its running on your local computer.
                
                The model field should have the exact name of the model you want to use, including any subfolders. The text below the output on the main tab can be customized by editing notes.md.
                """)
    gr.TabbedInterface([main.tab, notes.tab], ["Main", "Notes"])

if __name__ == "__main__":
    demo.launch() 
