import scipy.io
import os
from os import path
from pathlib import Path
import sys
sys.path.insert(1, "../")
from dataset_reader import PolsarDatasetHandler

labels_path = '/media/barrachina/data/datasets/PolSar/Oberpfaffenhofen/Label_Germany.mat'
t_path = '/media/barrachina/data/datasets/PolSar/Oberpfaffenhofen/ESAR_Oberpfaffenhofen_T6/Master_Track_Slave_Track/T6'
s_path = '/media/barrachina/data/datasets/PolSar/Oberpfaffenhofen/ESAR_Oberpfaffenhofen'

if not os.path.exists(labels_path) or not os.path.exists(t_path) or not os.path.exists(s_path):
    raise FileNotFoundError("No path found for Oberpfaffenhofen dataset")


class OberpfaffenhofenDataset(PolsarDatasetHandler):

    def __init__(self, *args, **kwargs):
        super(OberpfaffenhofenDataset, self).__init__(root_path=os.path.dirname(labels_path),
                                                      name="OBER", mode="t", *args, **kwargs)

    def print_ground_truth(self, t=None, *args, **kwargs):
        if t is None:
            t = self.get_image()
        super(OberpfaffenhofenDataset, self).print_ground_truth(t=t,
                                                                path=Path(os.path.dirname(labels_path)) / "ground_truth.png",
                                                                *args, **kwargs)

    def get_image(self):
        return self.open_t_dataset_t3(t_path)

    def get_sparse_labels(self):
        return scipy.io.loadmat(labels_path)['label']


if __name__ == "__main__":
    print("First Test")
    OberpfaffenhofenDataset().get_dataset(method="random", size=128, stride=25, pad="same")
    print("First one done")
    OberpfaffenhofenDataset(classification=True).get_dataset(method="random", size=12, stride=1, pad="same")
    print("Second one done")
    OberpfaffenhofenDataset(classification=True).get_dataset(method="random", size=1, stride=1, pad="same")
