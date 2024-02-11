import gradio as gr
import os

note_choices = ["None"]

def scan_notes():
    global note_choices
    note_choices = ["None"]
    for root, dirs, files in os.walk(r"notes"):
        for file in files:
            if file.endswith(".txt") or file.endswith(".md"):
                note_choices.append(os.path.join(root,file))

scan_notes()

def refresh():
    scan_notes()
    note_list.value = "None"
    return note_choices

def update_notes(evt: gr.SelectData):
    if evt.value == "None":
        return "No notes selected"
    else:
        file = open(evt.value, "r")
        note_text = file.read()
        file.close()
        return note_text

with gr.Blocks() as tab:
    with gr.Row():
        with gr.Column():
            gr.Markdown("Choose 'None' from the dropdown, to not show notes, or pick a note from the list. Any txt or md files in the notes folder will appear in the list.")
            with gr.Row():
                note_list = gr.Dropdown(multiselect = False, interactive = True, choices = note_choices, value = "None", scale = 4, label = "Note List")
                refresh_btn = gr.Button(value = "Refresh List", scale = 1)
            notes = gr.Markdown("No notes selected")
            note_list.select(update_notes, outputs = [notes])
            refresh_btn.click(refresh, outputs = [note_list])
