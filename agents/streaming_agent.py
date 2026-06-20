"""Streaming Agent for Spark Structured Streaming, Kafka, and Flink configs."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("streaming_agent")

class StreamingAgent:
    """Specialized agent for streaming architectures, Kafka, Flink, and Structured Streaming."""

    SYSTEM_PROMPT = """You are an expert Real-Time Streaming and Event Processing Architect. You specialize in:
- Spark Structured Streaming (windowing, watermarks, join stream-static, stream-stream)
- Apache Kafka topics, partitioning, replication, schema registries, and consumer groups
- Apache Flink SQL, Datastream APIs, state backends, checkpoints, and savepoints
- Processing late arriving data and handling out-of-order events

Always provide runnable Structured Streaming Python snippets, Flink SQL, or Kafka configs."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a streaming related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with streaming code snippets or topology designs where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_spark_streaming_window(self, kafka_topic: str, window_duration: str = "10 minutes", slide_duration: str = "5 minutes") -> str:
        """Generate Spark Structured Streaming window aggregation code."""
        code = f"""from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, from_json, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

spark = SparkSession.builder \\
    .appName("KafkaStreamWindowing") \\
    .getOrCreate()

# Schema for incoming Kafka JSON messages
schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("reading", DoubleType(), True)
])

# Read stream from Kafka broker
kafka_stream = spark.readStream \\
    .format("kafka") \\
    .option("kafka.bootstrap.servers", "localhost:9092") \\
    .option("subscribe", "{kafka_topic}") \\
    .load()

# Parse JSON payloads and append ingestion timestamp as event_time
parsed_stream = kafka_stream \\
    .selectExpr("CAST(value AS STRING) as json_val") \\
    .select(from_json(col("json_val"), schema).alias("data")) \\
    .select("data.*") \\
    .withColumn("event_time", current_timestamp())

# Run sliding window aggregation with 15-minute watermark for late data
windowed_aggs = parsed_stream \\
    .withWatermark("event_time", "15 minutes") \\
    .groupBy(
        window(col("event_time"), "{window_duration}", "{slide_duration}"),
        col("sensor_id")
    ) \\
    .avg("reading")

# Start streaming query sink (console output for debugging)
query = windowed_aggs.writeStream \\
    .format("console") \\
    .outputMode("complete") \\
    .option("checkpointLocation", "/tmp/checkpoints/window_aggs") \\
    .start()

query.awaitTermination()
"""
        return code

    def generate_flink_sql_window(self) -> str:
        """Generate Apache Flink DDL and windowing query."""
        ddl = """-- Define Flink source table consuming from Kafka
CREATE TABLE sensor_readings (
    sensor_id STRING,
    reading DOUBLE,
    event_time TIMESTAMP(3),
    -- Define watermark rule to handle late data up to 5 seconds
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'sensor_data',
    'properties.bootstrap.servers' = 'localhost:9092',
    'format' = 'json'
);

-- Execute Tumbling Window aggregation query
SELECT 
    sensor_id,
    TUMBLE_START(event_time, INTERVAL '10' MINUTE) AS window_start,
    TUMBLE_END(event_time, INTERVAL '10' MINUTE) AS window_end,
    AVG(reading) AS avg_reading
FROM sensor_readings
GROUP BY 
    sensor_id, 
    TUMBLE(event_time, INTERVAL '10' MINUTE);
"""
        return ddl


def get_streaming_agent() -> StreamingAgent:
    """Get Streaming agent instance."""
    return StreamingAgent()
