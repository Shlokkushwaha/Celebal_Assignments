# 🛒 Shopping Dataset Data Cleaning Project

## 📌 Project Overview

This project focuses on cleaning and preprocessing a shopping dataset using **Python** and **Pandas**. The notebook demonstrates important data cleaning operations such as handling missing values, removing duplicates, creating new columns, and exporting the cleaned dataset.

The main objective of this project is to prepare raw data for further analysis and machine learning tasks.

---

## 🚀 Features

* Load and inspect dataset
* Handle missing values
* Remove duplicate records
* Create derived columns
* Perform basic data analysis
* Export cleaned dataset

---

## 🛠️ Technologies Used

* Python
* Pandas
* Jupyter Notebook

---

## 📂 Project Structure

```bash
├── Combined_dataset.csv
├── cleaned_dataset.csv
├── data_cleaning.ipynb
└── README.md
```

---

## 📊 Data Cleaning Steps

### 1. Load Dataset

```python
import pandas as pd

df = pd.read_csv("Combined_dataset.csv")
```

### 2. Check Missing Values

```python
df.isnull().sum()
```

### 3. Fill Missing Values

```python
df['rating'] = df['rating'].fillna(df['rating'].mean())
```

```python
df['discount'] = df['discount'].fillna(df['discount'].mean())
```

### 4. Remove Duplicate Rows

```python
df.drop_duplicates(inplace=True)
```

### 5. Create New Columns

```python
df['quantity'] = 1

df['total_amount'] = df['final_price'] * df['quantity']
```

### 6. Save Cleaned Dataset

```python
df.to_csv("cleaned_dataset.csv", index=False)
```

---

## 📈 Output

* Cleaned dataset without duplicates
* Missing values handled successfully
* Added `total_amount` column
* Exported final cleaned dataset as CSV

---

## ▶️ How to Run the Project

1. Clone the repository

```bash
git clone <your-github-repo-link>
```

2. Install dependencies

```bash
pip install pandas
```

3. Run the Jupyter Notebook

```bash
jupyter notebook
```

---

## 📚 Learning Outcomes

Through this project, I learned:

* Data cleaning using Pandas
* Handling null values
* Removing duplicates
* Feature engineering basics
* Working with CSV files in Python

---

## 🤝 Contributing

Contributions are welcome. Feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

Shlok Kushwaha
