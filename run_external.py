from deoxys.experiment import Experiment, ExperimentPipeline, SegmentationExperimentPipeline
# from deoxys.utils import read_file
import argparse
import os
import shutil
# from pathlib import Path
# from comet_ml import Experiment as CometEx
import tensorflow as tf
import customize_obj

if __name__ == '__main__':
    gpus = tf.config.list_physical_devices('GPU')
    if not gpus:
        raise RuntimeError("GPU Unavailable")

    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_file")
    parser.add_argument("log_folder")
    parser.add_argument("--best_epoch", default=0, type=int)
    parser.add_argument("--temp_folder", default='', type=str)
    parser.add_argument("--analysis_folder",
                        default='', type=str)
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

    # copy to another location
    log_folder = args.log_folder + '_' + args.dataset_file[:-5].split('/')[-1]
    if not os.path.exists(log_folder):
        shutil.copytree(args.log_folder, log_folder)

    ex = SegmentationExperimentPipeline(
        log_base_path=log_folder,
        temp_base_path=args.temp_folder + '_' +
        args.dataset_file[:-5].split('/')[-1]
    )
    # if args.best_epoch == 0:
    #     try:
    #         ex = ex.load_best_model(
    #             monitor=args.monitor,
    #             recipe='2d',
    #             analysis_base_path=analysis_folder,
    #             map_meta_data=meta,
    #         )
    #     except Exception as e:
    #         print("Error while loading best model", e)
    #         print(e)
    # else:
    #     print(f'Loading model from epoch {args.best_epoch}')
    #     ex.from_file(args.log_folder +
    #                  f'/model/model.{args.best_epoch:03d}.h5')
    with open(args.log_folder + '/info.txt', 'r') as f:
        best_epoch = int(f.read()[-24:-21])
    print(f'Loading model from epoch {best_epoch}')
    ex.from_file(args.log_folder +
                 f'/model/model.{best_epoch:03d}.h5')
    ex.run_external(
        args.dataset_file
    ).apply_post_processors(
        recipe='2d',
        analysis_base_path=analysis_folder,
        map_meta_data=meta,
        run_test=True,
        metrics=['f1_score', 'precision', 'recall']
    ).plot_3d_test_images(best_num=2, worst_num=2)
