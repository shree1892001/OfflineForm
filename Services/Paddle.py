import os
import json
from IPython.display import Image as IPImage
import google.generativeai as genai



def flatten_json(nested_json, parent_key='', sep='_'):
    items = []
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        new_key = new_key.replace(" ", "_").replace("'", "")
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.append((new_key, json.dumps(v)))
        else:
            items.append((new_key, str(v)))
    return dict(items)
