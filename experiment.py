import customize_obj
# import h5py
# from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf
from deoxys.experiment import Experiment, ExperimentPipeline, SegmentationExperimentPipeline
from deoxys.model.callbacks import PredictionCheckpoint
# from deoxys.utils import read_file
import argparse
# import os
# import numpy as np
# from pathlib import Path
# from comet_ml import Experiment as CometEx


if __name__ == '__main__':
    gpus = tf.config.list_physical_devices('GPU')
    if not gpus:
        raise RuntimeError("GPU Unavailable")

    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    parser.add_argument("log_folder")
    parser.add_argument("--temp_folder", default='', type=str)
    parser.add_argument("--analysis_folder",
                        default='', type=str)
    parser.add_argument("--epochs", default=200, type=int)
    parser.add_argument("--model_checkpoint_period", default=5, type=int)
    parser.add_argument("--prediction_checkpoint_period", default=5, type=int)
    parser.add_argument("--meta", default='patient_idx,slice_idx', type=str)
    parser.add_argument("--monitor", default='f1_score', type=str)
    parser.add_argument("--memory_limit", default=0, type=int)

    args, unknown = parser.parse_known_args()

    if args.memory_limit:
        # Restrict TensorFlow to only allocate X-GB of memory on the first GPU
        try:
            tf.config.set_logical_device_configuration(
                gpus[0],
                [tf.config.LogicalDeviceConfiguration(
                    memory_limit=1024 * args.memory_limit)])
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(
                logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Virtual devices must be set before GPUs have been initialized
            print(e)

    analysis_folder = ''
    meta = args.meta

    print('training from configuration', args.config_file,
          'and saving log files to', args.log_folder)
    print('Unprocesssed prediciton are saved to', args.temp_folder)

    # PredictionCheckpoint._max_size = 0.5

    exp = SegmentationExperimentPipeline(
        log_base_path=args.log_folder,
        temp_base_path=args.temp_folder
    ).from_full_config(
        args.config_file
    ).run_experiment(
        train_history_log=True,
        model_checkpoint_period=args.model_checkpoint_period,
        prediction_checkpoint_period=args.prediction_checkpoint_period,
        epochs=args.epochs,
    ).apply_post_processors(
        recipe='2d',
        analysis_base_path=analysis_folder,
        map_meta_data=meta,
        metrics=['f1_score', 'precision', 'recall']
    ).plot_performance().load_best_model(
        monitor=args.monitor
    ).run_test(
    ).apply_post_processors(
        recipe='2d',
        analysis_base_path=analysis_folder,
        map_meta_data=meta,
        run_test=True,
        metrics=['f1_score', 'precision', 'recall']
    ).plot_3d_test_images(best_num=2, worst_num=2)
