import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

def filter(path):
    DATA_PATH = path
    data = pd.read_csv(DATA_PATH)
    data.corr()
    cols = data.columns

    num_cols = data._get_numeric_data().columns

    categorical_cols = list(set(cols)-set(num_cols))

    for col in categorical_cols:
        unique = data[col].unique()
        print("Column: {} has {} unique values\n".format(col, unique))

    data['Sex'] = pd.get_dummies(data['Sex'], drop_first = True)
    data['ExerciseAngina'] = pd.get_dummies(data['ExerciseAngina'], drop_first = True)


    data.head(10)
    data = shuffle(data, random_state = 42)

    #only include the necessary features in the final dataframe, and seperate features from target
    features = data[['ExerciseAngina', 'Oldpeak', 'MaxHR', 'Sex']]
    target = data[['HeartDisease']]

    #normalize data between -2pi and 2pi to be compatible with Bloch Sphere
    scaler = MinMaxScaler(feature_range = (-2 * np.pi, 2 * np.pi))
    features = scaler.fit_transform(features)

    #Split the 918 datapoints into test and training sets for variational circuit
    features_train, features_test, target_train, target_test = train_test_split(features, target, test_size=0.3, random_state=42)

    # print(features)
    
    x_train = features_train.tolist()
    x_test = features_test.tolist()
    y_train = target_train.values.tolist()
    y_test = target_test.values.tolist()
    print("features_train", type(x_train))
    print("features_test", type(x_test))
    print("target_train", type(y_train))
    print("target_test", type(y_test))
    

    return x_train, x_test, y_train, y_test
filter('./Data/testHeart.csv')
