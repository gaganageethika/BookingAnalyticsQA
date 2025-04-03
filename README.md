# Booking Analytics Q&A System

## Author: Gaganageethika Seerlancha 
## Project: Solvei8 AI/ML Internship Assignment  

## 📌 Description  
This project builds a **Booking Analytics Q&A System** that processes hotel booking data, creates a FAISS-based similarity search, generates revenue insights, and serves an API for querying data.

---

## 📂 Project Structure  

```
📁 BookingAnalyticsQA
│── 📁 data
│   ├── hotel_bookings.csv          # Raw dataset
│   ├── cleaned_bookings.csv        # Processed dataset
│   ├── faiss_index.bin             # FAISS index for similarity search
│   ├── revenue_trends.png          # Revenue trends visualization
│── 📁 notebooks
│   ├── datapreprocessing.ipynb     # Data cleaning and preprocessing
│── vector_store.py                 # FAISS vector storage creation
│── analytics.py                     # Revenue trend analysis
│── api.py                           # FastAPI server for Q&A & analytics
│── requirements.txt                 # Dependencies
│── README.md                        # Project documentation (this file)
```

---

## 🔧 Setup & Installation  

### 1️⃣ Install Dependencies  
Ensure Python (>=3.8) is installed and set up a virtual environment using **Anaconda**:

```bash
conda create --name booking_env python=3.8
conda activate booking_env
pip install -r requirements.txt
```

---

## 📊 Data Preprocessing (`datapreprocessing.ipynb`)
- Reads **hotel_bookings.csv**
- Cleans missing values
- Converts date formats
- Saves processed data as **cleaned_bookings.csv**

---

## 🔍 FAISS Vector Store (`vector_store.py`)
- Loads **cleaned_bookings.csv**
- Converts text data (hotel names) into embeddings using **Sentence Transformers**
- Stores embeddings in a **FAISS index**
- Saves the index to **faiss_index.bin**

Run the script:  
```bash
python vector_store.py
```

---

## 📈 Revenue Analytics (`analytics.py`)
- Reads **cleaned_bookings.csv**
- Calculates **monthly revenue trends**
- Saves the **revenue_trends.png** visualization
- Generates a **JSON insights report**

Run the script:  
```bash
python analytics.py
```

---

## 🌐 API (`api.py`)
Runs a FastAPI server with three endpoints:

### 1️⃣ Ask a Question (FAISS Search)
- **URL:** `http://127.0.0.1:8000/ask?query=What is the revenue trend?`
- **Response:** Retrieves the most relevant data match.

### 2️⃣ Analytics Data (JSON Format)
- **URL:** `http://127.0.0.1:8000/analytics`
- **Response:** Returns monthly revenue insights in JSON format.

### 3️⃣ Revenue Trends Visualization (Image)
- **URL:** `http://127.0.0.1:8000/analytics/plot`
- **Response:** Returns the revenue trends **PNG plot**.

Run the API server:  
```bash
uvicorn api:app --host 127.0.0.1 --port 8000
```
