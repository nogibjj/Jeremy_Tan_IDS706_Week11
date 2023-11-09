"""
query and viz file
"""
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import requests
import json
import base64

# sample query
def query_transform():
    """
    Run a predefined SQL query on a Spark DataFrame.

    Returns:
        DataFrame: Result of the SQL query.
    """
    spark = SparkSession.builder.appName("Query").getOrCreate()
    query = """
        SELECT 
            t1.id, t1.server, t1.seconds_before_next_point, t1.day, t1.opponent, t1.game_score, t1.set, t1.game,
            t2.tournament, t2.surface, t2.seconds_added_per_point, t2.years,
            COUNT(*) as total_rows
        FROM 
            serve_times_delta t1
        JOIN 
            event_times_delta t2 
            ON t1.id = t2.id
        GROUP BY 
            t1.id, t1.server, t1.seconds_before_next_point, t1.day, t1.opponent, t1.game_score, t1.set, t1.game,
            t2.tournament, t2.surface, t2.seconds_added_per_point, t2.years
        ORDER BY 
            t1.id, t2.years DESC, t1.seconds_before_next_point
    """
    query_result = spark.sql(query)
    return query_result

# sample viz for project
def viz():
    query = query_transform()
    plt.figure(figsize=(15, 8))  # Adjusted figure size
    boxplot = query.select('seconds_before_next_point', 'server').toPandas().boxplot(column='seconds_before_next_point', by='server')
    plt.xlabel('Server')
    plt.ylabel('Seconds Before Next Point')
    plt.suptitle('')
    plt.title('Seconds Before Next Point by Server')
    # Adjust the rotation and spacing of x-axis labels
    plt.xticks(rotation=30, ha='right')  # ha='right' aligns the labels to the right
    plt.tight_layout()  # Ensures proper spacing
    plt.savefig('server.png')  
    average_seconds_by_surface = query.groupBy('surface').avg('seconds_before_next_point')

    df_surface_avg = average_seconds_by_surface.toPandas()

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df_surface_avg['surface'], df_surface_avg['avg(seconds_before_next_point)'], color='blue')
    plt.xlabel('Surface Type')
    plt.ylabel('Average Seconds Before Next Point')
    plt.title('Average Seconds Before Next Point by Surface Type')
    plt.xticks(rotation=45)
    plt.show('surface.png')
