import os

import joblib
from sklearn.linear_model import LogisticRegression
import argparse
import numpy as np
from sklearn.model_selection import train_test_split
from azureml.core.run import Run
from azureml.data.dataset_factory import TabularDatasetFactory


path = "https://raw.githubusercontent.com/TahreemArif/ML-Azure-Capstone-Project/master/heart_failure_clinical_records_dataset.csv"
ds = TabularDatasetFactory.from_delimited_files(path=path)
x = ds.to_pandas_dataframe().dropna()
y = x.pop("DEATH_EVENT")

# TODO: Split data into train and test sets.

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=23)

run = Run.get_context()


def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--C', type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")

    args = parser.parse_args()

    run.log("Regularization Strength:", np.float(args.C))
    run.log("Max iterations:", np.int(args.max_iter))

    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    run.log("Accuracy", np.float(accuracy))

    os.makedirs('outputs', exist_ok=True)

    joblib.dump(model, 'outputs/model.joblib')


if __name__ == '__main__':
    main()
