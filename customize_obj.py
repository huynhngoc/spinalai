import shutil
import h5py
import numpy as np
from deoxys.experiment.postprocessor import DefaultPostProcessor
# from deoxys.loaders import load_data
# from tensorflow.python.ops.gen_math_ops import square
# import tensorflow_addons as tfa
from deoxys.model.losses import Loss, loss_from_config
from deoxys.customize import custom_loss, custom_preprocessor
from deoxys.data import BasePreprocessor
import os


@custom_preprocessor
class ChannelRepeater(BasePreprocessor):
    def __init__(self, channel=0):
        if '__iter__' not in dir(channel):
            self.channel = [channel]
        else:
            self.channel = channel

    def transform(self, images, targets):
        return np.concatenate([images, images[..., self.channel]], axis=-1), targets


@custom_loss
class FusedLoss(Loss):
    """Used to sum two or more loss functions.
    """

    def __init__(
            self, loss_configs, loss_weights=None,
            reduction="auto", name="fused_loss"):
        super().__init__(reduction, name)
        self.losses = [loss_from_config(loss_config)
                       for loss_config in loss_configs]

        if loss_weights is None:
            loss_weights = [1] * len(self.losses)
        self.loss_weights = loss_weights

    def call(self, target, prediction):
        loss = None
        for loss_class, loss_weight in zip(self.losses, self.loss_weights):
            if loss is None:
                loss = loss_weight * loss_class(target, prediction)
            else:
                loss += loss_weight * loss_class(target, prediction)

        return loss


class EnsemblePostProcessor(DefaultPostProcessor):
    def __init__(self, log_base_path='logs',
                 log_path_list=None,
                 map_meta_data=None, **kwargs):

        self.log_base_path = log_base_path
        self.log_path_list = []
        for path in log_path_list:
            merge_file = path + self.TEST_OUTPUT_PATH + self.PREDICT_TEST_NAME
            if os.path.exists(merge_file):
                self.log_path_list.append(merge_file)
            else:
                print('Missing file from', path)

        # check if there are more than 1 to ensemble
        assert len(self.log_path_list) > 1, 'Cannot ensemble with 0 or 1 item'

        if map_meta_data:
            if type(map_meta_data) == str:
                self.map_meta_data = map_meta_data.split(',')
            else:
                self.map_meta_data = map_meta_data
        else:
            self.map_meta_data = ['patient_idx']

        # always run test
        self.run_test = True

    def ensemble_results(self):
        # initialize the folder
        if not os.path.exists(self.log_base_path):
            print('Creating output folder')
            os.makedirs(self.log_base_path)

        output_folder = self.log_base_path + self.TEST_OUTPUT_PATH
        if not os.path.exists(output_folder):
            print('Creating ensemble folder')
            os.makedirs(output_folder)

        output_file = output_folder + self.PREDICT_TEST_NAME
        if not os.path.exists(output_file):
            print('Copying template for output file')
            shutil.copy(self.log_path_list[0], output_folder)

        print('Creating ensemble results...')
        y_preds = []
        for file in self.log_path_list:
            with h5py.File(file, 'r') as hf:
                y_preds.append(hf['predicted'][:])

        with h5py.File(output_file, 'a') as mf:
            mf['predicted'][:] = np.mean(y_preds, axis=0)
        print('Ensembled results saved to file')

        return self

    def concat_results(self):
        # initialize the folder
        if not os.path.exists(self.log_base_path):
            print('Creating output folder')
            os.makedirs(self.log_base_path)

        output_folder = self.log_base_path + self.TEST_OUTPUT_PATH
        if not os.path.exists(output_folder):
            print('Creating ensemble folder')
            os.makedirs(output_folder)

        # first check the template
        with h5py.File(self.log_path_list[0], 'r') as f:
            ds_names = list(f.keys())
        ds = {name: [] for name in ds_names}

        # get the data
        for file in self.log_path_list:
            with h5py.File(file, 'r') as hf:
                for key in ds:
                    ds[key].append(hf[key][:])

        # now merge them
        print('creating merged file')
        output_file = output_folder + self.PREDICT_TEST_NAME
        with h5py.File(output_file, 'w') as mf:
            for key, val in ds.items():
                mf.create_dataset(key, data=np.concatenate(val, axis=0))
