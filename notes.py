import gradio as gr

def update_notes(evt: gr.SelectData):
    if evt.value == "None":
        return "No notes selected"
    else:
        file = open("notes/sample.md", "r")
        note_text = file.read()
        file.close()
        return note_text

with gr.Blocks() as tab:
    with gr.Row():
        with gr.Column():
            gr.Markdown("This is intended to show notes from the notes folder, but is currently a placeholder.")
            with gr.Row():
                note_list = gr.Dropdown(multiselect = False, interactive = True, choices = ["None", "Test"], value = "None", scale = 4, label = "Note List")
                gr.Button(value = "Refresh List", scale = 1)
            notes = gr.Markdown("No notes selected")
            note_list.select(update_notes, outputs = [notes])
