# WEB-BASED REAL-TIME CROWD ANALYSIS FOR RETAIL

**Note:** This project was my Final Year Project for my Bachelor's in Computer Science.

## Introduction

We live in a world that is undergoing constant transformation and innovation. As technology advances, businesses must adapt to stay competitive. In the retail industry, providing exceptional customer experiences is key to success. Retail stores must not only understand customer preferences but also optimize their point of sale (POS) operations. 

This project addresses these challenges by introducing a real-time video analytics solution, focusing on **crowd analytics** in the retail environment. Crowd analytics involves gathering and interpreting data from the movement of customers within a store. By analyzing this data, retailers can gain valuable insights into customer behavior, such as:

- People count
- Gender classification
- Shoplifting detection
- Parking space detection

Traditional methods of data collection and analysis suffer from delays and limited scope. This project proposes a solution to overcome these limitations, using **real-time video analytics**, **computer vision**, **machine learning**, and **deep learning** models.

## Objective

The goal of this project is to develop a **dashboard** capable of:

- Detecting **shoplifting**.
- Performing **object tracking** to count people.
- Classifying customers by **gender**.
- Detecting **parking space availability**.

The system will use **AI-based models** to perform real-time video analytics for retail environments.

## Problem Description

In today's world, retail stores require advanced solutions to help improve efficiency, sales, and customer experience. The objective of this project is to create a dashboard that can analyze CCTV video feeds in real-time, providing insights that retail stores can use for decision-making. This will not only enhance the customer experience but also optimize store operations.

### Key Features:

- **People Counting**: Automatically count the number of people in a specific area of the store.
- **Gender Classification**: Classify the gender of individuals in the store.
- **Shoplifting Detection**: Detect suspicious behavior related to shoplifting.
- **Parking Space Detection**: Analyze and detect available parking spaces in real-time.

### Goals:

- Develop models for **people counting**.
- Develop models for **gender classification**.
- Develop models for **shoplifting detection**.
- Develop models for **parking space detection**.


### Architecture Diagram
![Architecture Diagram](images/architecture.png)

## Methodology

This project utilizes **Python** as the primary language for backend development and **Flask** for the frontend. The core of the system leverages **Machine Learning** and **Deep Learning** techniques for real-time video analytics. Additionally, **Firebase Database** will be used for storing and retrieving data.

### Key Technologies Used:

- **Python** (Backend)
- **Flask** (Frontend)
- **Machine Learning** and **Deep Learning** (Analytics)
- **Firebase** (Database)
- **YOLO (You Only Look Once)** for object detection, including shoplifting detection, people counting, gender classification, and parking space detection.

### Key AI Techniques:

- **Object Tracking**: Used for detecting and tracking objects in a video stream, allowing for people counting and behavior analysis.
- **Image Recognition**: Helps in detecting and classifying objects, such as people and vehicles.
- **Machine Learning & Deep Learning Models**: Applied to analyze video data and identify patterns or anomalies, such as potential shoplifting.

### Exclusion of `yolov3.weights`

Due to GitHub's file size limitations, the `yolov3.weights` file (which is essential for YOLO-based object detection in this project) has been excluded from the repository. The file exceeds GitHub's 100MB size limit, and as such, it could not be uploaded.
You can download the `yolov3.weights` file from [this link](<https://drive.google.com/file/d/1hZq_EHyWnApqI4LphZHT-2gQoVubMaKs/view?usp=sharing>).

## Dashboard Screenshots

### 1. Login GUI
![Login GUI](images/loginGUI.png)


### 2. Dashboard GUI
![Dashboard GUI](images/dashboardGUInew.png)

### 3. Dashboard GUI 
![Dashboard GUI (Alternate)](images/dashboardGUInew2.png)

### 4. People Count
![People Count GUI](images/peopleCountGUI.png)

### 5. Parking Space Detection
![Parking Space Detection](images/parkingSpaceDetectionGUI.png)

### 6. Tabular Description
![Tabular Description GUI](images/TabularDescriptionGUI.png)

### 7. Design Methodology
![Design Methodology](images/designMethadology.png)

### 8. UDB1
![UDB1](images/UDB1.png)

### 9. UDB2
![UDB2](images/UDB2.png)














