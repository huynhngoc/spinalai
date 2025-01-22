import pandas as pd
import numpy as np
import os
import json
import h5py
import argparse

def f1_score(y_true, y_pred, threshold=0.5, beta=1):
    eps = 1e-8

    y_pred = (y_pred > threshold).astype(y_pred.dtype)

    true_positive = np.sum(y_pred * y_true)
    target_positive = np.sum(y_true)
    predicted_positive = np.sum(y_pred)

    fb_numerator = (1 + beta ** 2) * true_positive + eps
    fb_denominator = (
        (beta ** 2) * target_positive + predicted_positive + eps
    )

    return fb_numerator / fb_denominator

def precision(y_true, y_pred, threshold=0.5):
    eps = 1e-8

    y_pred = (y_pred > threshold).astype(y_pred.dtype)

    true_positive = np.sum(y_pred * y_true)
    # target_positive = np.sum(y_true, axis=reduce_ax)
    predicted_positive = np.sum(y_pred)

    fb_numerator = true_positive + eps
    fb_denominator = predicted_positive + eps

    return fb_numerator / fb_denominator


def recall(y_true, y_pred, threshold=0.5):
    eps = 1e-8

    y_pred = (y_pred > threshold).astype(y_pred.dtype)

    true_positive = np.sum(y_pred * y_true)
    target_positive = np.sum(y_true)
    # predicted_positive = np.sum(y_pred), axis=reduce_ax)

    fb_numerator = true_positive + eps
    fb_denominator = target_positive + eps

    return fb_numerator / fb_denominator


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str)
    experiment_name = parser.parse_args().name
    # experiment_name = 'soft_tissue_lr001_{folds}'

    # preparing the data
    # patient_folder = '../nifti'
    output_folder = f'../perf/{experiment_name.replace("{folds}", "all")}/'
    os.makedirs(output_folder, exist_ok=True)
    ensemble_info = []

    # list of experiments
    fold_list = ['f012', 'f102', 'f021', 'f201', 'f120', 'f210']

    # Initialize a dictionary to group the exps with the same test set
    groups = {}

    # Iterate through the fold_list and group by the last character
    for fold in fold_list:
        key = fold[-1]
        if key not in groups:
            groups[key] = []
        groups[key].append(fold)

    print('Creating the files for the ensemble results...')
    output_h5_file = output_folder + 'predictions.h5'
    with h5py.File(output_h5_file, 'w') as f:
        f.create_group('predicted')
        f.create_group('y')

    print('Start ensembling the rslts...')
    for group in groups.values():
        ensemble_prediction = {}
        targets = {}
        print('calculating the results from experiments:', group)
        for fold in group:
            experiment_info = []
            log_folder = '../perf/' + experiment_name.format(folds=fold)
            perf_info = pd.read_csv(log_folder + '/test/result.csv', index_col='patient_idx').rename_axis('pid')
            test_file = log_folder + '/test/prediction_test.h5'
            with h5py.File(test_file, 'r') as f:
                group = f['predicted']
                for pid in group.keys():
                    predicted = group[pid][:]
                    if not ensemble_prediction.get(pid):
                        ensemble_prediction[pid] = predicted
                        targets[pid] = f['y'][pid][:]
                    else:
                        ensemble_prediction[pid] = np.stack([ensemble_prediction[pid], predicted], axis=-1)

        with h5py.File(output_h5_file, 'a') as f:
            for pid in targets.keys():
                pred = np.mean(ensemble_prediction[pid], axis=-1)
                f['predicted'].create_dataset(pid, data=pred)
                f['y'].create_dataset(pid, data=targets)
                ensemble_info.append([pid, f1_score(targets[pid], pred), precision(targets[pid], pred), recall(targets[pid], pred)])

    df = pd.DataFrame(ensemble_info, columns=['pid', 'f1', 'precision', 'recall'])
    df.to_csv(os.path.join(output_folder, 'result.csv'), index=False)
