from itertools import groupby
from matplotlib import pyplot
from matplotlib.pyplot import xlabel, ylabel
import numpy as np
import matplotlib
import seaborn
import pandas as pd
from pandas_profiling import profile_report

# loading data
data = pd.read_csv("/Users/grantsackmann/MIT_BWSI/fruse/Data/orginialHeartData.csv")

# creating data frame
df = pd.DataFrame(data)
pd.options.display.max_rows = 100

#                                                ///Column Data Breakdown///
# 'Age': age of the patient [years]
# 'Sex': sex of the patient [M: Male, F: Female]
# 'ChestPainType': chest pain type 
#       [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]
# 
# 'RestingBP': resting blood pressure [mm Hg]
# 'Cholesterol': serum cholesterol [mm/dl]
# 'FastingBS': fasting blood sugar [1: if FastingBS > 120 mg/dl, 0: otherwise]
# 'RestingECG': resting electrocardiogram results [Normal: Normal, ST: having ST-T wave abnormality, 
#       LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]
# 
# 'MaxHR': maximum heart rate achieved [Numeric value between 60 and 202]
# 'ExerciseAngina': exercise-induced angina [Y: Yes, N: No]
# 'Oldpeak': oldpeak = ST [Numeric value measured in depression]
# 'ST_Slope': the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]
# 
# 'HeartDisease':<TARGET> output class [1: heart disease, 0: Normal]
# 
# 
#                                           ///Additional INFO///
# 
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

#                                       ///cleaning data///

# --converting Strings to floats
def Sex_to_float(df):
    # 0 - Male
    # 1 - Female
    sex_dict = {"M": 0.0, "F":1.0}
    df["Sex"]=df["Sex"].map(sex_dict)

def CPT_to_float(df):
    #      String                 float Val
    # TA: Typical Angina              0.0
    # ATA: Atypical Angina            1.0
    # NAP: Non-Anginal Pain           2.0
    # ASY: Asymptomatic               3.0 
    CPT_dict ={"TA": 0.0, "ATA": 1.0, "NAP": 2.0, "ASY": 3.0}
    df["ChestPainType"]=df["ChestPainType"].map(CPT_dict)

def RestingECG_to_float(df):
    #        String                           float Val                       
    # Normal: Normal                               0.0
    # ST: having ST-T wave abnormality             1.0 

    # LVH: showing probable or definite            
    # left ventricular hypertrophy                 2.0 
    # by Estes' criteria
   ECG_dict ={"Normal": 0.0, "ST": 1.0, "LVH": 2.0}
   df["RestingECG"]=df["RestingECG"].map(ECG_dict)

def ExerciseAngina_to_float(df): 
    #  Y: Yes -- 1.0
    #  N: No -- 0.0
    ExerciseAngina_dict ={"Y": 1.0, "N": 0.0}
    df["ExerciseAngina"]=df["ExerciseAngina"].map(ExerciseAngina_dict)

def ST_Slope_to_float(df):
    #  String               Int
    # Up: upsloping          0.0
    # Flat: flat             1.0
    # Down: downsloping      2.0
    ST_Slope_dict ={"Up": 0.0, "Flat": 1.0, "Down": 2.0}
    df["ST_Slope"]=df["ST_Slope"].map(ST_Slope_dict)

# Calling String to float functions
Sex_to_float(df)
ExerciseAngina_to_float(df)

# skiping these because they are non-binary categorical
# and assigning arbitrary values to them
# wont help in finding correlation to our target
# 
# CPT_to_float(df)
# RestingECG_to_float(df)
# ST_Slope_to_float(df)

# converts num values to float64
def convert_to_flaot(df):
    for col in df.columns:
        df[col]=df[col].astype(np.float64, errors="ignore")

# converting categorical variables to binary columns
def categorials_to_binary(df):
    for col in df.columns:
        # categorical data wil be objects
        if df[col].dtype == object:
            df_of_binarys = pd.get_dummies(df[col])
            df = pd.concat((df,df_of_binarys), axis=1)
            df = df.drop([col],axis=1)
    return df

# updating dataframe 
df = categorials_to_binary(df)
# converting all types to float64
convert_to_flaot(df)

# displaying correlation with HeartDisease target against all variables
# print(df.corrwith(["HeartDisease"]))

# 
df.to_csv('Data/cleanedHeartData.csv', index=False)

#                 ///Corelation Analysis///
# 
# Absolute value of r coefficient 	  Correlation Strength
# .90 to 1.00                            	Very high 
# .70 to .90 	                              High  
# .50 to .70 	                            Moderate  
# .30 to .50                        	      Low  
# .00 to .30                               Negligible 
# 
#  Citation https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3576830/
# 
# 
# parameters with the highest correlation to Heart Disease target
# 
# 
#  Parameter           r coefficient        Corelation Strength
# ExerciseAngina          0.494282                  Low
# ASY                     0.516716                Moderate
# Flat                    0.554134                Moderate
# Up                     -0.622164                Moderate

# filtering out remaining negligible-low correlation data 
df = df.filter(["ExerciseAngina","ASY","Flat","Up","HeartDisease"])