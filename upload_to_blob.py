from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from io import BytesIO
import io
from pyspark.sql import SparkSession
import pandas as pd
from datetime import datetime, timedelta

# Set JAVA_HOME in Python if it's not automatically detected


# Azure storage account credentials
account_name = "adlszeus"
account_key = "ksL9a2OZFCiKFYPn6hzTNJcY4WI2Nq2xSsRlUD8cDH3dBBEvePAhJqErSP6QKN27so/2ayW3DnO7O8s4uPtUZA=="
container_name = "data-validation-container"


# Replace with your Azure Blob Storage connection string
connection_string = 'DefaultEndpointsProtocol=https;AccountName=adlszeus;AccountKey=ksL9a2OZFCiKFYPn6hzTNJcY4WI2Nq2xSsRlUD8cDH3dBBEvePAhJqErSP6QKN27so/2ayW3DnO7O8s4uPtUZA==;EndpointSuffix=core.windows.net'

container_name = 'data-validation-container'
blob_service_client = BlobServiceClient.from_connection_string(
    connection_string)
container_client = blob_service_client.get_container_client(container_name)
blob_list = container_client.list_blobs()


# Define the function to upload portfolio data
def upload_portfolio_to_blob_storage(df: pd.DataFrame):
    if df.empty:
        print("DataFrame is empty.")
    else:
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)  # Reset buffer pointer
        blob_name = f"portfolio/user_portfolio.csv"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(csv_buffer, overwrite=True)
        print(f"CSV file for user uploaded successfully to {blob_name}.")

# Define the function to upload ticker data
def upload_ticker_record_to_blob_storage(df: pd.DataFrame, ticker: str):
    if df.empty:
        print(f"DataFrame for {ticker} is empty.")
    else:
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)  # Reset buffer pointer
        blob_name = f"data/{ticker}.csv"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(csv_buffer, overwrite=True)
        print(f"CSV file for ticker {ticker} uploaded successfully to {blob_name}.")