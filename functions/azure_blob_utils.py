from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from io import BytesIO
import io
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
# Set JAVA_HOME in Python if it's not automatically detected

# Load the environment variables from the .env file
load_dotenv()

# Azure storage account credentials
account_name = "adlszeus"
account_key = os.getenv("AZURE_ACCOUNT_KEY")
container_name = "data-validation-container"


# Replace with your Azure Blob Storage connection string
connection_string = 'DefaultEndpointsProtocol=https;AccountName=adlszeus;AccountKey=ksL9a2OZFCiKFYPn6hzTNJcY4WI2Nq2xSsRlUD8cDH3dBBEvePAhJqErSP6QKN27so/2ayW3DnO7O8s4uPtUZA==;EndpointSuffix=core.windows.net'

container_name = 'data-validation-container'
blob_service_client = BlobServiceClient.from_connection_string(
    connection_string)
container_client = blob_service_client.get_container_client(container_name)
blob_list = container_client.list_blobs()


# Define the function to upload portfolio data
def upload_user_portfolio(df: pd.DataFrame):
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
def upload_stocks_data(df: pd.DataFrame):
    if df.empty:
        print(f"DataFrame is empty.")
    else:
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)  # Reset buffer pointer
        blob_name = f"data/stocks_data.csv"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(csv_buffer, overwrite=True)
        print(f"CSV file for stocks data uploaded successfully to {blob_name}.")
    
def read_output_blob():
    portfolio_returns_blob_name = "output/portfolio_returns.csv"
    portfolio_returns_blob_client = container_client.get_blob_client(portfolio_returns_blob_name)
    download_stream = portfolio_returns_blob_client.download_blob()
    portfolio_df = pd.read_csv(io.BytesIO(download_stream.readall()))  # Read CSV content into a DataFrame

    # Read VaR result text
    var_result_blob_name = "output/var_result.txt"
    var_result_blob_client = container_client.get_blob_client(var_result_blob_name)
    download_stream = var_result_blob_client.download_blob()
    var_result = download_stream.readall().decode('utf-8')  # Decode text content

    return portfolio_df, var_result
        