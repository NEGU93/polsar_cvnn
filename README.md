# PolSAR CVNN

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5821229.svg)](https://doi.org/10.5281/zenodo.5821229)
[![PyPI version](https://badge.fury.io/py/cvnn.svg)](https://badge.fury.io/py/cvnn)

PolSAR classification / segmentation using complex-valued neural networks.

## Cite

To cite the code please use Zenodo:

"J Agustin Barrachina. (2022). NEGU93/polsar_cvnn: Antology of CVNN for PolSAR applications (1.0.0). Zenodo. https://doi.org/10.5281/zenodo.5821229"

``` 
@software{j_agustin_barrachina_2022_5821229,
  author       = {J Agustin Barrachina},
  title        = {{NEGU93/polsar\_cvnn: Antology of CVNN for PolSAR 
                   applications}},
  month        = jan,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.5821229},
  url          = {https://doi.org/10.5281/zenodo.5821229}
}
```

## Code usage

1. Install all dependencies including [cvnn](https://pypi.org/project/cvnn/).
2. Clone this repository
3. Run the file `principal_simulation.py`. Optional parameters go as follows:
```
usage: principal_simulation.py [-h] [--dataset_method DATASET_METHOD]
                               [--tensorflow] [--epochs EPOCHS]
                               [--model MODEL] [--early_stop [EARLY_STOP]]
                               [--balance BALANCE] [--real_mode [REAL_MODE]]
                               [--dropout DROPOUT DROPOUT DROPOUT]
                               [--coherency] [--dataset DATASET]

optional arguments:
  -h, --help            show this help message and exit
  --dataset_method DATASET_METHOD
                        One of:
                        	- random (default): randomly select the train and val set
                        	- separate: split first the image into sections and select the sets from there
                        	- single_separated_image: as separate, but do not apply the slinding window operation 
                        		(no batches, only one image per set). 
                        		Only possible with segmentation models
  --tensorflow          Use tensorflow library
  --epochs EPOCHS       (int) epochs to be done
  --model MODEL         deep model to be used. Options:
                        	- fcnn
                        	- cnn
                        	- mlp
                        	- 3d-cnn
  --early_stop [EARLY_STOP]
                        Apply early stopping to training
  --balance BALANCE     Deal with unbalanced dataset by:
                        	- loss: weighted loss
                        	- dataset: balance dataset by randomly remove pixels of predominant classes
                        	- any other string will be considered as not balanced
  --real_mode [REAL_MODE]
                        run real model instead of complex.
                        If [REAL_MODE] is used it should be one of:
                        	- real_imag
                        	- amplitude_phase
                        	- amplitude_only
                        	- real_only
  --dropout DROPOUT DROPOUT DROPOUT
                        dropout rate to be used on downsampling, bottle neck, upsampling sections (in order). Example: `python main.py --dropout 0.1 None 0.3` will use 10% dropout on the downsampling part and 30% on the upsamlpling part and no dropout on the bottle neck.
  --coherency           Use coherency matrix instead of s
  --dataset DATASET     dataset to be used. Available options:
                        	- SF-AIRSAR
                        	- SF-RS2
                        	- OBER

Process finished with exit code 0

```
4. Once simulations are done the program will create a folder inside `log/<date>/run-<time>/` that will contain the following information:
    - `tensorboard`: Files to be visualized with [tensorboard](https://www.tensorflow.org/tensorboard).
    - `checkpoints`: Saved model weights of the lowest validation loss obtained.
    - `prediction.png`: Image with the predicted image of the best model.
    - `model_summary.txt`: Information about the simulation done.
    - `history_dict.csv`: The dictionary of all loss and metrics over epoch obtained as a return of [`Model.fit()`](https://www.tensorflow.org/api_docs/python/tf/keras/Model#fit).
    - `<dataset>_confusion_matrix.csv`: Confusion matrices for different datasets.
    - `evaluate.csv`: Loss and all metrics for all datasets and full image.


## Datasets

### San Francisco

1. Download the San Francisco dataset. The labels and images are well described in [this](https://arxiv.org/abs/1912.07259) paper. It is important that the format of the folder copies the structure of [this](https://github.com/liuxuvip/PolSF) repository.
2. Change the `root_path` whith the path where the dataset was downloaded on the file `San Francisco/sf_data_reader.py`

### Oberpfaffenhofen

1. Download labels from [this repository](https://github.com/fudanxu/CV-CNN/blob/master/Label_Germany.mat) 
2. Download image from the [European Space Agency (esa) website](https://step.esa.int/main/toolboxes/polsarpro-v6-0-biomass-edition-toolbox/)
3. Change the `root_path` whith the path where the dataset was downloaded on the file `Oberpfaffenhofen/oberpfaffenhofen_dataset.py`

### Own dataset

For using your own dataset:

1. create a new class that inherits from `PolsarDatasetHandler`. Two methods (at least) should be created.
    - `get_image`: Return a numpy array of the 3D image (height, width, channels), channels are usually complex-valued and in the form of coherency matrix or pauli vector representation.
    - `get_sparse_labels`: Returns an array with the labels in sparse mode (NOT one-hot encoded).
2. Inside `principal_simulation.py`
    - Import your class.
    - Add your dataset metadata into `DATASET_META`.
    - Add your dataset into `_get_dataset_handler`.

## Models

Currently, the following models are supported:

- FCNN from [Cao et al.](https://www.mdpi.com/2072-4292/11/22/2653)
- CNN from [Zhang et al.](https://ieeexplore.ieee.org/abstract/document/8039431) and then used (to some extent) and present to some extent in [Sun et al.](https://ieeexplore.ieee.org/abstract/document/8809406); [Zhao et al.](https://ieeexplore.ieee.org/abstract/document/8900150); [Qin et al.](https://ieeexplore.ieee.org/abstract/document/9296798)
- MLP from Hansh et al. present in all these papers: [1](https://www.ingentaconnect.com/content/asprs/pers/2010/00000076/00000009/art00008); [2](https://ieeexplore.ieee.org/abstract/document/5758871); [3](https://www.isprs.org/proceedings/xxxviii/1_4_7-W5/paper/Haensch-147.pdf)
- 3D-CNN from [Tan et al.](https://ieeexplore.ieee.org/abstract/document/8864110)

To create your own model it sufice to:

1. Create your own `Tensorflow` model (using `cvnn` if needed) and create a function or class that returns it (already compiled).
2. Add it to `_get_model` inside `principal_simulation.py`
3. Add your model name to `MODEL_META` to be able to call the script with your new model parameter.
