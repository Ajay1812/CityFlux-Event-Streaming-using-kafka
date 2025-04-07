# 🚦 CityFlux: Real-Time Event Streaming using Apache Kafka

CityFlux is a ⚡ real-time data streaming pipeline built to collect, process, and analyze urban mobility data such as 🚗 vehicle telemetry, 📍 GPS locations, 🌧️ weather conditions, 📷 traffic camera feeds, and 🚨 emergency alerts.

---

## 🧠 Architecture Overview



---

## 🔄 ETL Workflow

CityFlux leverages a modern, scalable ETL architecture:

1. **📥 Data Ingestion**  
   Simulated vehicle and environmental data is streamed into Apache Kafka topics in real time 🛰️.

2. **⚙️ Data Processing**  
   Apache Spark reads the Kafka streams, performs necessary transformations (ETL), and writes structured data into Amazon S3 📂.

3. **🗃️ Data Cataloging**  
   AWS Glue Crawlers automatically scan raw and transformed S3 buckets and update the Glue Data Catalog for downstream querying.

4. **📊 Querying & Warehousing**  
   - **Amazon Athena** allows SQL-based querying directly on the S3 data lake.
   - **Amazon Redshift Serverless** ingests curated data for high-performance analytics and dashboarding.

---

## 🧰 Tech Stack

| 🔗 Layer                  | ⚙️ Technology                         |
|--------------------------|--------------------------------------|
| 💬 Streaming Engine       | Apache Kafka, Apache ZooKeeper       |
| 🔄 Stream Processing      | Apache Spark                         |
| 🌊 Data Lake              | Amazon S3                            |
| 🗂️ Metadata Catalog       | AWS Glue                             |
| 🧠 Query Engine           | Amazon Athena, Amazon Redshift       |
| 📈 Visualization Tools    | Power BI, AWS QuickSight             |
| 🐳 Containerization       | Docker                               |

---

## 🚀 Getting Started

### ✅ Prerequisites
- 🐳 Docker & Docker Compose  
- 🔥 Apache Spark  
- ☁️ AWS CLI configured  
- 🔐 AWS access to S3, Glue, Athena, Redshift  

---

### 📥 1. Clone the Repository
```bash
git clone https://github.com/Ajay1812/CityFlux-Event-Streaming-using-kafka.git
cd CityFlux-Event-Streaming-using-kafka
```

### 🐍 2. Set Up Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 📦 3. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 🔐 4. Configure AWS Credentials
Set up your AWS credentials in `config.py` 🔐.

```py
configuration = {
    "AWS_ACCESS_KEY" : "YOUR_ACCESS_KEY",
    "AWS_SECRET_KEY" : "YOUR_SECRET_KEY",
    "S3_BUCKET"      : "YOUR_SECRET_KEY" 
    }
```


### 🐳 5. Start docker-compose
```bash
docker-compose up -d
```

### 📡 6. Simulate Raltime Data
Run the main script to simulate vehicle movements and stream data to Kafka:
```bash
python job/main.py
```

### 💥 7. Submit Spark Streaming Job
```bash
docker exec -it cityflux-event-streaming-using-kafka_spark-master_1 spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.469 jobs/spark-job.py
```
## 🤝 Contributing

Contributions are welcome! If you find a bug or want to enhance a project, feel free to submit a pull request.


## 📬 Contact

Got questions or want to contribute? Feel free to reach out!

- 📧 **Email**: [a.kumar01c@gmail.com](mailto:a.kumar01c@gmail.com)  
- 🔗 **GitHub**: [Ajay1812](https://github.com/Ajay1812)
- 🌐 **LinkedIn**: [nf-analyst](https://www.linkedin.com/in/nf-analyst/)
