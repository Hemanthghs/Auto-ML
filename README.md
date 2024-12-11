# Auto-ML Web Application

## Overview

Auto-ML is a web platform designed to automate the process of training machine learning models. The platform allows users, even those without a background in machine learning or data science, to upload datasets, select algorithms, train models, evaluate their performance, and deploy them. The platform simplifies the entire machine learning workflow, making it accessible to a wider audience.

### Key Features
- **Dataset Upload:** Users can upload datasets for training.
- **Algorithm Selection:** Choose from a variety of machine learning algorithms.
- **Model Training:** Automate the training of machine learning models.
- **Data Preprocessing & Visualization:** Built-in tools for data preprocessing, validation, and visualization.
- **Model Evaluation:** Evaluate model performance using key metrics.
- **Model Testing & Deployment:** Test models with inputs and deploy them for public access.
- **Model Download:** Users can download the trained model and use it elsewhere.

---

## Technologies Used

- **Backend:** Python, Flask
- **Database:** MongoDB
- **Machine Learning Libraries:** scikit-learn, pandas, matplotlib, etc.
- **Frontend:** HTML, CSS, JavaScript

---

## Installation Instructions

### Method 1: By Cloning the Git Repository

1. **Install Python 3.6 or later**
   Download and install Python from [here](https://www.python.org/downloads/).

2. **Clone the Git Repository**
   ```bash
   git clone https://github.com/Hemanthghs/Auto-ML
Navigate to the Project Directory

```bash
cd Auto-ML
Install Virtualenv
```

```bash
pip install virtualenv
Create a Virtual Environment
```

```bash
virtualenv env
Activate the Virtual Environment
```

Linux/Mac OS:
```bash
source env/Scripts/activate
```

Windows:
```bash
env/Scripts/activate
Install Required Dependencies
```

```bash
pip install -r requirements.txt
Start the Server
```

```bash
python app.py
```

Start App Using Docker Image
```
Install Docker Engine Follow the installation guide here.

Pull the Docker Image
```

```bash
docker pull hemanthghs/automl
Run the Docker Container
```

```bash
docker run -p 1234:1234 hemanthghs/auto-ml
Usage Instructions
Start the Web Server
```



