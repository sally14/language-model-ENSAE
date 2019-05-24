"""

                        Utils

Utils, helps generating dataset, etc.

"""

import os

# import sys

import numpy as np
# import gensim
from glob import glob
from nltk import FreqDist
# sys.path.append(os.path.expanduser('~/nlp'))


def generate_dataset(filedir, logdir, mode="mlm", **kwargs):
    """
    Generates dataset for the Masked Language / LM task.
    Args
        filedir : a directory of files on which datasets must be
                    generated
        mode : masked language model (mlm) or classical language model (lm)
        n : the number of token which must be masked per sentence (mlm mode
            only)
    Returns
        None

    Writes new file.sent, file.labels in a subdir 'mlm_dataset'.
    """
    if mode == "mlm":
        n = kwargs["n"]
    # Retrieving list of filenames with glob:
    filenames = glob(os.path.join(filedir, "*"))
    # Getting dirname for writing operations:
    # dirname = os.path.dirname(os.path.dirname(filenames[0]))
    # Creating new subdir in which files will be written
    write_path = logdir

    if not os.path.exists(write_path):
        os.makedirs(write_path)

    # Start iterating on files:
    for file in filenames:
        basename = os.path.basename(file)
        with open(file, "r", encoding="utf-8") as f:
            sents = f.readlines()  # In f, there is 1 sent per line
            if mode == "mlm":
                write_mlm(write_path, basename, sents, n)
            else:
                write_lm(write_path, basename, sents)
    return None


# generate_dataset('/Users/salome/Documents/ENSAE/S6/nlp/dataset', mode="mlm", n=3)


def write_mlm(write_path, basename, sents, n):
    sent_basename = os.path.join(write_path, basename + ".sents")
    label_basename = os.path.join(write_path, basename + ".labels")
    # Now that we have sents, mask n random words / generate lm model
    with open(sent_basename, "w", encoding="utf-8") as s_write:
        with open(label_basename, "w", encoding="utf-8") as l_write:
            for s in sents:
                tokens = s.rstrip("\n").split(" ")
                m = len(tokens)
                if m <= n:
                    print("m<n, passing.")
                    pass
                else:
                    mask = np.random.choice(range(m), size=n, replace=False)
                    for i in range(m):
                        if i in mask:
                            s_write.write("<MASK> ")
                            l_write.write(str(tokens[i]) + " ")
                        else:
                            s_write.write(str(tokens[i]) + " ")
                    s_write.write("\n")
                    l_write.write("\n")
    return None


def write_lm(write_path, basename, sents):
    sent_basename = os.path.join(write_path, basename + ".sents")
    label_basename = os.path.join(write_path, basename + ".labels")
    # Now that we have sents, mask n random words / generate lm model
    with open(sent_basename, "w", encoding="utf-8") as s_write:
        with open(label_basename, "w", encoding="utf-8") as l_write:
            for s in sents:
                tokens = s.rstrip("\n").split(" ")
                # Start and stop chars
                tokens = ["<s>"] + tokens + ["</s>"]
                m = len(tokens)
                for i in range(1, m):
                    s_write.write(" ".join(tokens[:i]))
                    l_write.write(tokens[i])
                    s_write.write("\n")
                    l_write.write("\n")
    return None


def create_full_vocab(train, emb):
    with open(train, 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', '')
    tokens = text.split(' ')
    vocab_words = FreqDist(tokens)
    vocab_chars = set(list(text))
    count = len(tokens)
    with open(os.path.join(emb, 'vocab.txt'), 'w', encoding='utf-8') as f:
        with open(os.path.join(emb, 'freq.txt'), 'w', encoding='utf-8') as freq:
            for i in vocab_words.keys():
                f.write(i + '\n')
                #print(vocab_words[i])
                freq.write(str(int(vocab_words[i])/count)+'\n')
    with open(os.path.join(emb, 'chars.txt'), 'w', encoding='utf-8') as c:
        for i in vocab_chars:
            c.write(i+'\n')



