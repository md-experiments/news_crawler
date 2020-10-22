import os
import requests

model_type = "mega"

model_dir = os.path.join('/content/grover/models', model_type)
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

#gsutil cp gs://grover-models/discrimination/generator=medium~discriminator=grover~discsize=medium~dataset=p=0.96/model.ckpt-1562.data-00000-of-00001
#gsutil cp gs://grover-models/discrimination/generator=medium~discriminator=grover~discsize=medium~dataset=p=0.96/model.ckpt-1562.index
#gsutil cp gs://grover-models/discrimination/generator=medium~discriminator=grover~discsize=medium~dataset=p=0.96/model.ckpt-1562.meta

for ext in ['data-00000-of-00001', 'index', 'meta']:
    r = requests.get(f'https://storage.googleapis.com/grover-models/{model_type}/model.ckpt.{ext}', stream=True)
    with open(os.path.join(model_dir, f'model.ckpt.{ext}'), 'wb') as f:
        file_size = int(r.headers["content-length"])
        if file_size < 1000:
            raise ValueError("File doesn't exist? idk")
        chunk_size = 1000
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
    print(f"Just downloaded {model_type}/model.ckpt.{ext}!", flush=True)

