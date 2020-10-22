
# Commented out IPython magic to ensure Python compatibility.
# %cd /content
#!git clone https://github.com/rowanz/grover.git
# %cd /content/grover
#!python3 -m pip install regex jsonlines twitter-text-python feedparser

"""### Step 3: Download Grover Pre-Trained 'Mega' Model"""

"""import tensorflow as tf
import numpy as np
import sys
import feedparser
import time
from datetime import datetime, timedelta
import requests
import base64
from ttp import ttp

sys.path.append('../')
from lm.modeling import GroverConfig, sample
from sample.encoder import get_encoder, _tokenize_article_pieces, extract_generated_target
import random
"""
import os
import requests

model_type = "base" # "large" #"mega" 

model_dir = './'

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


'''
def generate_article_attribute(sess, encoder, tokens, probs, article, target='article'):

    """
    Given attributes about an article (title, author, etc), use that context to generate
    a replacement for one of those attributes using the Grover model.
    This function is based on the Grover examples distributed with the Grover code.
    """

    # Tokenize the raw article text
    article_pieces = _tokenize_article_pieces(encoder, article)

    # Grab the article elements the model careas about - domain, date, title, etc.
    context_formatted = []
    for key in ['domain', 'date', 'authors', 'title', 'article']:
        if key != target:
            context_formatted.extend(article_pieces.pop(key, []))

    # Start formatting the tokens in the way the model expects them, starting with
    # which article attribute we want to generate.
    context_formatted.append(encoder.__dict__['begin_{}'.format(target)])
    # Tell the model which special tokens (such as the end token) aren't part of the text
    ignore_ids_np = np.array(encoder.special_tokens_onehot)
    ignore_ids_np[encoder.__dict__['end_{}'.format(target)]] = 0

    # We are only going to generate one article attribute with a fixed
    # top_ps cut-off of 95%. This simple example isn't processing in batches.
    gens = []
    article['top_ps'] = [0.95]

    # Run the input through the TensorFlow model and grab the generated output
    tokens_out, probs_out = sess.run(
        [tokens, probs],
        feed_dict={
            # Pass real values for the inputs that the
            # model needs to be able to run.
            initial_context: [context_formatted],
            eos_token: encoder.__dict__['end_{}'.format(target)],
            ignore_ids: ignore_ids_np,
            p_for_topp: np.array([0.95]),
        }
    )

    # The model is done! Grab the results it generated and format the results into normal text.
    for t_i, p_i in zip(tokens_out, probs_out):
        extraction = extract_generated_target(output_tokens=t_i, encoder=encoder, target=target)
        gens.append(extraction['extraction'])

    # Return the generated text.
    return gens[-1]
'''
