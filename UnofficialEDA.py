# implementing Rodnoy Osodo's Exploratory Data Analysis and Cleaning

# imports
from itertools import groupby
from matplotlib import pyplot
from matplotlib.pyplot import xlabel, ylabel
import numpy as np
import matplotlib
import seaborn
import pandas as pd
from pandas_profiling import profile_report

# loading data
data = pd.read_csv("/Users/grantsackmann/MIT_BWSI/fruse/heart.csv")

# creating data frame
df = pd.DataFrame(data)
pd.options.display.max_rows = 918

# print(data.columns)

#  ____Output____  #
# 'Age': age of the patient [years]
# 'Sex': sex of the patient [M: Male, F: Female]
# 'ChestPainType': chest pain type [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]
# 'RestingBP': resting blood pressure [mm Hg]
# 'Cholesterol': serum cholesterol [mm/dl]
# 'FastingBS': fasting blood sugar [1: if FastingBS > 120 mg/dl, 0: otherwise]
# 'RestingECG': resting electrocardiogram results [Normal: Normal, ST: having ST-T wave abnormality, 
#       LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]
# 'MaxHR': maximum heart rate achieved [Numeric value between 60 and 202]
# 'ExerciseAngina': exercise-induced angina [Y: Yes, N: No]
# 'Oldpeak': oldpeak = ST [Numeric value measured in depression]
# 'ST_Slope': the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]

# 'HeartDisease':<TARGET> output class [1: heart disease, 0: Normal]

# Additional INFO

# RangeIndex: 918 entries, 0 to 917
# Data columns (total 12 columns):

#  #   Column          Non-Null Count  Dtype  
# ---  ------          --------------  -----  
#  0   Age             918 non-null    int64  
#  1   Sex             918 non-null    object 
#  2   ChestPainType   918 non-null    object 
#  3   RestingBP       918 non-null    int64  
#  4   Cholesterol     918 non-null    int64  
#  5   FastingBS       918 non-null    int64  
#  6   RestingECG      918 non-null    object 
#  7   MaxHR           918 non-null    int64  
#  8   ExerciseAngina  918 non-null    object 
#  9   Oldpeak         918 non-null    float64
#  10  ST_Slope        918 non-null    object 
#  11  HeartDisease    918 non-null    int64  

# dtypes: float64(1), int64(6), object(5)
# memory usage: 86.2+ KB

# checks for unique values in each culumn
def check_Uniques(df):
    for col in df.columns:
        print("Column: {} has {} unique values\n".format(col,df[col].unique()))

# we find that 
# Sex, ChestPainType, Resting ECG, Exercise Angine, 
# and ST_Slope are categorial

# cleaning data types

# converting String to floats
def Sex_to_int(df):
    # 0 - Male
    # 1 - Female
    sex_dict = {"M": 0, "F":1}
    df["Sex"]=df["Sex"].map(sex_dict)

def CPT_to_int(df):
    #      String                 Int Val
    # TA: Typical Angina              0
    # ATA: Atypical Angina            1
    # NAP: Non-Anginal Pain           2
    # ASY: Asymptomatic               3 
    CPT_dict ={"TA": 0, "ATA": 1, "NAP": 2, "ASY": 3}
    df["ChestPainType"]=df["ChestPainType"].map(CPT_dict)

def RestingECG_int(df):
    #        String                           Int Val                       
    # Normal: Normal                               0
    # ST: having ST-T wave abnormality             1 

    # LVH: showing probable or definite            
    # left ventricular hypertrophy                 2 
    # by Estes' criteria
   ECG_dict ={"Normal": 0, "ST": 1, "LVH": 2}
   df["RestingECG"]=df["RestingECG"].map(ECG_dict)

def ExerciseAngina(df): 
    #  Y: Yes -- 1
    #  N: No -- 0
    ExerciseAngina_dict ={"Y": 1, "N": 0}
    df["ExerciseAngina"]=df["ExerciseAngina"].map(ExerciseAngina_dict)

def ST_Slope(df):
    #  String               Int
    # Up: upsloping          0
    # Flat: flat             1
    # Down: downsloping      2
    ST_Slope_dict ={"Up": 0, "Flat": 1, "Down": 2}
    df["ST_Slope"]=df["ST_Slope"].map(ST_Slope_dict)

# Calling String to Int functions
Sex_to_int(df)
CPT_to_int(df)
RestingECG_int(df)
ExerciseAngina(df)
ST_Slope(df)

# checking correlation with target
# KEEP IN MIND ChestPainType, Resting ECG, Exercise Angine, 
# and ST_Slope ARE CATEGORIAL

# corr_series = df.corrwith(df["HeartDisease"])
print(df.corrwith(df["HeartDisease"]))