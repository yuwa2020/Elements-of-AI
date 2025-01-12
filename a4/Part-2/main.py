import json
import argparse
import math
from collections import Counter

def calculate_distance(x1, x2, distance_metric):
    """ Calculates the distance between two points

    Args:
        x1 (list): coordinates of the first point
        x2 (list): coordinates of the second point
        distance_metric (str): distance metric to be used

    Returns:
        float: distance between the two points
    """
    if distance_metric == "euclidean":
        distance = math.sqrt((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2)
    elif distance_metric == "manhattan":
        distance = abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])
    elif distance_metric == "minkowski":
        # if p = 1, it is Manhattan distance, if p = 2, it is Euclidean distance
        distance = (abs(x1[0] - x2[0]) ** 3 + abs(x1[1] - x2[1]) ** 3) ** (1/3)
    else:
        raise ValueError("Invalid distance metric")

    return distance

def K_Nearest_Neighbors(file: str, k: int, distance_metric: str):
    """ Implements K-Nearest Neighbors Algorithm

    Args:
        file (str): path to the dataset file
        k (int): number of nearest Neighbors considered in the analysis
        distance_metric (str): distance metric for K-NN algorithm

    Returns:
        float: accuracy on the test set
    """

    with open(file, 'r') as f:
        data = json.load(f)
        X_train, y_train, X_test, y_test = data['X_train'], data['y_train'], data['X_test'], data['y_test']
    
    # Implement K_Nearest_Neghbors Algorithm here.
    predicted_classes = []
    i=1
    # Calculate distance between each test point and all training points.
    for x_test_coordinate, y_test_class in zip(X_test, y_test):
        distances = []
        for x_train_coordinate, y_train_class in zip(X_train, y_train):
            distance = calculate_distance(x_test_coordinate, x_train_coordinate, distance_metric)
            distances.append((distance, y_train_class))

        # print(distances)
        
        # Sort the distances
        # idea from https://levelup.gitconnected.com/sorting-in-python-using-keys-d2622edd7a92?gi=9cedea628424
        distances.sort(key=lambda x: x[0])

        # Select the k-nearest neighbors
        k_nearest = distances[:k]

        # Count each class among the k-nearest neighbors
        # idea from https://docs.python.org/3/library/collections.html
        cnt = Counter()
        for _, y_class in k_nearest:
            cnt[y_class] += 1
        print(i)
        i+=1
        print(cnt)
        # most_common return a list of the n most common elements and if elements with equal counts are ordered in the order first encountered.
        predicted_class = cnt.most_common(1)[0][0]
        print(predicted_class)
        predicted_classes.append(predicted_class)
        # print(f"Predicted class: {predicted_class}, True class: {y_test_class}")

    # Calculate accuracy for test set.

    accuracy_test_set = 0 # between 0 and 100

    for predicted_class, true_class in zip(predicted_classes, y_test):
        if predicted_class == true_class:
            accuracy_test_set += 1

    accuracy_test_set = (accuracy_test_set / len(y_test)) * 100

    return accuracy_test_set

def main():
    parser = argparse.ArgumentParser(description='KNN Classification with Synthetic Data')
    parser.add_argument('--dataset_path', type=str, help="path to the json file containing data")
    parser.add_argument('--k', type=int, help="k for k-NN algorithm")
    parser.add_argument('--distance_metric', type=str, help="distance metric for K-NN")
    args = parser.parse_args()
    
    accuracy = K_Nearest_Neighbors(args.dataset_path, args.k, args.distance_metric)
    print(f"Test set accuracy for {args.dataset_path} - {accuracy}.")

if __name__ == '__main__':
    main()