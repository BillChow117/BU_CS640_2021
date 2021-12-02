# Naive Bayes
## Clean Data

After loaded dataset, I used 
  * regular expressions to filter **URLs**, **@usernames**, **#topics** out of texts
  * dropped colums where label == 2 in test set
  * stop words vectorizer to remove some meanless words in texts

## Performance
|               |precision  |recall |f1-score   |support    |
|---------------|:---------:|:-----:|:---------:|:---------:|
|0              | 0.80      | 0.81  | 0.81      | 177       |
|4              | 0.81      | 0.81  | 0.81      | 182       |
|accuracy       |           |       | 0.81      | 359       |
|macro avg      | 0.81      | 0.81  | 0.81      | 359       |
|weighted avg   | 0.81      | 0.81  | 0.81      | 359       |


# BERT
## Clean Data

After loaded dataset, I used 
  * regular expressions to filter **URLs**, **@usernames**, **#topics** out of texts
  * dropped colums where label == 2 in test set
  * changed in labels from 4 to 1, so that there are two classes, 0 and 1, in labels
  * splited trainning data into trainning set and validation set

## Fine-tune
`Model`: | `BERT` | `Linear(768,512)` | `Relu` | `Dropout` | `Linear(512,128)` | `Relu` | `Dropout` | `Linear(128,2)` | `Softmax` |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|

  + Optimizer: Adam. Adam is versatile, and works in a large number of scenarios.
  + Learning rate: 1e-5. In order to converge the model, I set a small learning rate. Adam keeps it adaptive anyway.
  + Batch size: 32. To fit in most GPUs.
  + Loss Function: NLLLoss.


## Performance
|               |precision  |recall |f1-score   |support    |
|---------------|:---------:|:-----:|:---------:|:---------:|
|0              | 0.86      | 0.83  | 0.84      | 177       |
|1              | 0.84      | 0.87  | 0.85      | 182       |
|accuracy       |           |       | 0.85      | 359       |
|macro avg      | 0.85      | 0.85  | 0.85      | 359       |
|weighted avg   | 0.85      | 0.85  | 0.85      | 359       |

# Code
Notebooks of two methods are following, some outputs have been removed since they are tedious and meaningless.

For the complete files, [BERT.ipynb](https://github.com/BillChow117/BU_CS640_2021/blob/main/Programmings/PA3/BERT.ipynb) and [NB.ipynb](https://github.com/BillChow117/BU_CS640_2021/blob/main/Programmings/PA3/DataSetLoading_and_Preprocessing.ipynb).