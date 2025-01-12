# import json
# import argparse


# def K_Nearest_Neighbors(file: str, k: int, distance_metric: str):
#     """ Implements K-Nearest Neighbors Algorithm

#     Args:
#         file (str): path to the dataset file
#         k (int): number of nearest Neighbors considered in the analysis
#         distance_metric (str): distance metric for K-NN algorithm

#     Returns:
#         float: accuracy on the test set
#     """

#     with open(file, 'r') as f:
#         data = json.load(f)
#         X_train, y_train, X_test, y_test = data['X_train'], data['y_train'], data['X_test'], data['y_test']
    
#     # Implement K_Nearest_Neghbors Algorithm here.
#     # Calculate accuracy for test set.

#     accuracy_test_set = 0 # between 0 and 100

#     return accuracy_test_set

# def main():
#     parser = argparse.ArgumentParser(description='KNN Classification with Synthetic Data')
#     parser.add_argument('--dataset_path', type=str, help="path to the json file containing data")
#     parser.add_argument('--k', type=int, help="k for k-NN algorithm")
#     parser.add_argument('--distance_metric', type=str, help="distance metric for K-NN")
#     args = parser.parse_args()
    
#     accuracy = K_Nearest_Neighbors(args.dataset_path, args.k, args.distance_metric)
#     print(f"Test set accuracy for {args.dataset_path} - {accuracy}.")

# if __name__ == '__main__':
#     main()


#Main Code 
import numpy as np
from scipy.spatial.distance import cdist
import json
import argparse

def K_Nearest_Neighbors(file: str, k: int, distance_metric: str):
    """ Implements K-Nearest Neighbors Algorithm

    Args:
        file (str): path to the dataset file
        k (int): number of nearest Neighbors considered in the analysis
        distance_metric (str): distance metric for K-NN algorithm

    Returns:
        float: accuracy on the test set
    """
    # Load the data from JSON file
    with open(file, 'r') as f:
        data = json.load(f)
        X_train, y_train, X_test, y_test = data['X_train'], data['y_train'], data['X_test'], data['y_test']
    
    # Convert to numpy arrays for easier manipulation
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)

    # Calculate distances between test points and all training points
    distances = cdist(X_test, X_train, metric=distance_metric)
    # distances = cdist(X_test, X_train, metric=distance_metric, p=3) # Minkowski distance with p=3
    
    # Get k nearest neighbors for each test point
    nearest_neighbors = np.argsort(distances, axis=1)[:, :k]
    
    # Predict the class by majority vote from nearest neighbors
    predictions = []
    for neighbors in nearest_neighbors:
        neighbor_labels = [y_train[i] for i in neighbors]
        predicted_label = np.bincount(neighbor_labels).argmax()  # Majority vote
        predictions.append(predicted_label)
    
    # Calculate accuracy
    correct_predictions = sum(np.array(predictions) == np.array(y_test))
    accuracy = correct_predictions / len(y_test)
    
    return accuracy

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='K-Nearest Neighbors Classification')
    parser.add_argument('--dataset_path', type=str, required=True, help='Path to the dataset file')
    parser.add_argument('--k', type=int, required=True, help='Number of nearest neighbors')
    parser.add_argument('--distance_metric', type=str, required=True, help='Distance metric for K-NN algorithm')

    # Parse arguments
    args = parser.parse_args()

    # Run the K-NN algorithm with parsed arguments
    accuracy = K_Nearest_Neighbors(args.dataset_path, args.k, args.distance_metric)
    
    # Print accuracy
    print(f'Test set accuracy: {accuracy * 100:.2f}%')

if __name__ == '__main__':
    main()



## Additional Part 
# import numpy as np
# import json
# import argparse
# from scipy.spatial.distance import cdist
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score

# def load_data(dataset_path):
#     with open(dataset_path) as f:
#         data = json.load(f)
#     return np.array(data["X_train"]), np.array(data["y_train"]), np.array(data["X_test"]), np.array(data["y_test"])

# def calculate_accuracy(X_train, y_train, X_test, y_test, k, distance_metric):
#     # Compute pairwise distances
#     distances = cdist(X_test, X_train, metric=distance_metric)

#     # Get the k nearest neighbors for each test point
#     neighbors = np.argsort(distances, axis=1)[:, :k]

#     # Predict the label by majority vote
#     predictions = []
#     for i in range(len(X_test)):
#         neighbor_labels = y_train[neighbors[i]]
#         predicted_label = np.bincount(neighbor_labels.astype(int)).argmax()
#         predictions.append(predicted_label)
    
#     accuracy = accuracy_score(y_test, predictions)
#     return accuracy

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--dataset_path', type=str, required=True, help="Path to the dataset")
#     parser.add_argument('--k_values', type=str, default="3,6,9", help="Comma-separated list of k values to evaluate")
#     parser.add_argument('--distance_metrics', type=str, default="euclidean,manhattan", help="Comma-separated list of distance metrics to evaluate")
    
#     args = parser.parse_args()
    
#     # Load dataset
#     X_train, y_train, X_test, y_test = load_data(args.dataset_path)
    
#     # Parse k values and distance metrics
#     k_values = [int(k) for k in args.k_values.split(',')]
#     distance_metrics = args.distance_metrics.split(',')

#     # Run ablation study
#     results = []
#     for k in k_values:
#         for metric in distance_metrics:
#             accuracy = calculate_accuracy(X_train, y_train, X_test, y_test, k, metric)
#             results.append((k, metric, accuracy))
#             print(f"Accuracy for k={k}, metric={metric}: {accuracy:.4f}")

#     # You can modify this to save results in a table format if needed
#     # e.g., save to a CSV or update the README file programmatically
#     # Results format example: (dataset_name, k, metric, accuracy)

# if __name__ == "__main__":
#     main()

