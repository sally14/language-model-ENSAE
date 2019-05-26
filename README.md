# Language Modeling with deep learning

This repository contains the work done for ENSAE NLP 2019 spring course. 

We implemented with Tensorflow some deep learning models for language modeling. 


## Getting started 

To get started, first clone the repository:

```shell
git clone https://github.com/sally14/language-model-ENSAE.git
cd language-model-ENSAE
```
Then install the conda environment (might be compatible with pip, but not tested) :

```shell
conda env create -f environment.yml
```
Validate conda's options (might have reproductibility issues with tensorflow-gpu on OSX, use a tensorflow-gpu docker if so) and activate the environment:
```shell
conda activate nlp-ensae
```
Then train the 6 models in the report :
```shell
bash train.sh
```
During training, you can visualize metrics in tensorboard, launch a tensorboard server:
```shell
tensorboard --logdir logs/logs_wiki_LSTM --port=6006
```
And then just go to ```localhost:6006``` to see tensorboard. 

## Repository composition
The repository is composed of the following scripts:

### train.sh
This is the main shell script, that launches the training of our 6 models, creating a directory *logs* containing the logs of the 6 models.

Usage :
```shell
bash train.sh
```

### train.py
Scripts that trains a model. Must be used from the command line. 

Basic usage : 
```shell
python train.py <filepath> <log_dir>
```
Where ```<filepath>``` is the path to a directory containing the training ```*.train.txt```, ```*.test.txt``` files, and ```<log_dir>``` the directory where logs must be written.

To see all parameters options, type: 
```shell
python train.py -h
```
Example : 
```shell
python train.py taoteba  logs/logs_taoteba_LSTM \
             --optimizer=rmsprop \
             --learning_rate=0.001 \
             --add_char_emb=False \
             --weighted_loss=False \
             --add_encoder=False \
             --deepness_finish=3 \
             --n_epochs=6 \
             --batch_size=252 \
             --add_n_grams_deps=True \
             --checkpoints=2000 
```

### predict.py
A prediction script. It has almost the same usage as train.py, but must take the same hyperparameters in options as the train.py options that were used to generate models. 

Usage : 
```shell
python predict.py log_dir 'sentence to continue' <nb tokens to be predicted> 
```

Example : 
```shell
python predict.py logs/logs_taoteba_LSTM \
             "why don 't  you just"  10\
             --optimizer=rmsprop \
             --learning_rate=0.001 \
             --add_char_emb=False \
             --weighted_loss=False \
             --add_encoder=False \
             --deepness_finish=3 \
             --n_epochs=6 \
             --batch_size=252 \
             --add_n_grams_deps=True \
             --checkpoints=2000 
```

**WARNING** : must have the same parameters options as the train.py run used to generate the model in ```log_dir```, otherwise Tensorflow will not be able to re-build the graph and will not run.

### model.py 
Defines the main model function as a "model_fn" function for the tf.Estimator API.

### submodels.py
Defines tf.keras.layers.Layer subclasses representing the main blocks (character-level word embedding, multilayer LSTM, Encoder) of the model.

### utils.py
Defines various utils helpers to generate sentence-level and cross-sentence examples etc. 

### reader.py 
Defines the "input_fn" function for tf.Estimator. Reads and formats as a tf.data.Dataset the files generated by utils.py. Optimized and parallelized.
