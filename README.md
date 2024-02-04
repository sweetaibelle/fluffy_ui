## Fluffy UI

This is just a gradio interface that controls ComfyUI, and is a bit easier to deal with than nodes, though more limited.

It's pretty much what you see is what you get, and it's a person project, so if you are using it, I'm just going to assume you know what you are doing. :P

You need to have already installed [ComfyUI](https://github.com/comfyanonymous/ComfyUI) and have it working. 

For this to work, in the same folder as this program, do something like this (I'm assuming Linux):
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run it:
```
source venv/bin/activate
python app.py
```

Then go to http://127.0.0.1:7860/?__theme=dark

Technically, if you already installed the two packages listed in requirement.txt, you could probably run it outside of a venv.

Once you have it open, put the correct address in the Server URL field. That's probably the one already there if you are running it locally. Model is what model in ComfyUI's model folder to load, including subfolder. I'm just assuming you have an XL folder in there with the pony v6 XL model in there.

Then fiddle with the settings, hit generate, and wait for pictures!

It doesn't actually save any of the settings yet or anything. Maybe later.
