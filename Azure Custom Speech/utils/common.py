import requests
import time
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, BlobSasPermissions
import os
import datetime


def create_project(base_url, headers, name, description, locale):
    """
    Retrieves the model ID of the Vietnamese base model.
    """
    project_url = f'{base_url}/v3.2/projects'
    data = {
        "displayName": name,
        "locale": locale,
        "description": description
    }
    response = requests.post(project_url, headers=headers, json=data)
    response.raise_for_status()
    project = response.json()
    project_id = project['self'].split('/')[-1]
    print(f'Project created with ID: {project_id}')
    return project_id

def create_dataset(base_url, headers, project_id, content_url, kind, display_name, description, locale):
    """
    Creates a new evaluation dataset.
    """
    dataset_url = f'{base_url}/v3.2/datasets'
    dataset_body = {
        "displayName": display_name,
        "description": description,
        "kind": kind,
        "contentUrl": content_url,
        "locale": locale,
        "project": {
            "self": f'{base_url}/v3.2/projects/{project_id}'
        },

    }

    response = requests.post(dataset_url, headers=headers, json=dataset_body)
    response.raise_for_status()
    dataset = response.json()
    dataset_id = dataset['self'].split('/')[-1]
    print(f'Dataset created with ID: {dataset_id}')
    return dataset_id

def get_dataset_content_url(base_url, headers, dataset_id):
    """
    Retrieves the SAS URI (contentUrl) for uploading the dataset.
    """
    dataset_info_url = f'{base_url}/v3.2/datasets/{dataset_id}'
    response = requests.get(dataset_info_url, headers=headers)
    response.raise_for_status()
    dataset_info = response.json()
    print(dataset_info)
    content_url = dataset_info['contentUrl']
    print(f'Content URL retrieved: {content_url}')
    return content_url

def get_base_model(base_url, headers, base_model_id):
    """
    Retrieves the base model.
    """
    models_url = f'{base_url}/v3.2/models/base/{base_model_id}'
    response = requests.get(models_url, headers=headers)
    response.raise_for_status()
    model = response.json()
    return model     

def get_custom_model_status(base_url, headers, model_id):
    """
    Retrieves the custom model.
    """
    models_url = f'{base_url}/v3.2/models/{model_id}'
    response = requests.get(models_url, headers=headers)
    response.raise_for_status()
    model = response.json()
    return model['status']

def create_custom_model(base_url, headers, project_id, base_model_id, datasets, display_name, description, locale):
    """
    Creates an evaluation job using the dataset and Vietnamese base model.
    """
    custom_model_url = f'{base_url}/v3.2/models'
    
    custom_model_body = {
        "displayName": display_name,
        "description": description,
        "locale": locale,
        "baseModel": {
            "self": f'{base_url}/v3.2/models/base/{base_model_id}'
        },
        "datasets": [],
        "project": {
            "self": f'{base_url}/v3.2/projects/{project_id}'
        },
    }
    for dataset in datasets:
            custom_model_body["datasets"].append({
                "self": f'{base_url}/v3.2/datasets/{dataset}'
            })
    print(custom_model_body)

    response = requests.post(custom_model_url, headers=headers, json=custom_model_body)
    response.raise_for_status()
    custom_model = response.json()
    custom_model_id = custom_model['self'].split('/')[-1]
    print(f'custom model job created with ID: {custom_model_id}')
    return custom_model_id

def create_evaluation(base_url, headers, project_id, dataset_id, model1_id, model2_id, display_name, description, locale):
    """
    Creates an evaluation job using the dataset and Vietnamese base model.
    """
    evaluations_url = f'{base_url}/v3.2/evaluations'
    print(evaluations_url)
    print(project_id, dataset_id, model1_id, model2_id)

    evaluation_body = {
        "model1": {
            "self": f'{base_url}/v3.2/models/{model1_id}'
        },
        "model2": {
            "self": f'{base_url}/v3.2/models/{model2_id}'
        },
        "dataset": {
            "self": f'{base_url}/v3.2/datasets/{dataset_id}'
        },
        "project": {
            "self": f'{base_url}/v3.2/projects/{project_id}'
        },
        "displayName": display_name,
        "description": description,
        "locale": locale,
        
    }
    
    print(evaluation_body)

    response = requests.post(evaluations_url, headers=headers, json=evaluation_body)
    response.raise_for_status()
    evaluation = response.json()
    evaluation_id = evaluation['self'].split('/')[-1]
    print(f'Evaluation job created with ID: {evaluation_id}')
    return evaluation_id

def get_evaluation_status(base_url, headers, evaluation_id):
    """
    Polls the evaluation job until it completes.
    """
    evaluation_url = f'{base_url}/v3.2/evaluations/{evaluation_id}'
    response = requests.get(evaluation_url, headers=headers)
    response.raise_for_status()
    evaluation_info = response.json()
    return evaluation_info['status']

def get_evaluation_results(base_url, headers, evaluation_id):
    """
    Prints the Word Error Rate (WER) and other evaluation metrics.
    """
    evaluation_url = f'{base_url}/v3.2/evaluations/{evaluation_id}'
    response = requests.get(evaluation_url, headers=headers)
    response.raise_for_status()
    return response.json() 


def upload_dataset_to_storage(data_folder, container_name, account_name, account_key):
    """
    Uploads datasets to Azure Blob Storage and generates SAS URLs.

    Parameters:
    - data_folder: The folder containing the evaluation datasets.
    - container_name: The name of the Azure Blob Storage container.
    - account_name: The Azure Storage account name.
    - account_key: The Azure Storage account key.

    Returns:
    - uploaded_files: A list of uploaded file names without extensions.
    - url: A dictionary mapping file names without extensions to their SAS URLs.
    """
    connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_client = blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        container_client.create_container()

    uploaded_files = []
    url = {}

    for file_name in os.listdir(data_folder):
        if file_name.endswith(".zip") or file_name.endswith(".txt"):
            file_path = os.path.join(data_folder, file_name)
            blob_name = file_name
            blob_client = container_client.get_blob_client(blob_name)

            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)

            sas_url = blob_client.url + "?" + generate_blob_sas(
                account_name=blob_service_client.account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=account_key,  
                permission=BlobSasPermissions(read=True),
                expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            )
            if(file_name.endswith(".zip")):
                uploaded_files.append(file_name.replace(".zip", ""))
                url[file_name.replace(".zip", "")] = sas_url
            else:
                uploaded_files.append(file_name.replace(".txt", ""))
                url[file_name.replace(".txt", "")] = sas_url


    print("Files uploaded successfully.")
    print("uploaded_files:", uploaded_files)
    print("url:", url)
    
    return uploaded_files, url


def create_endpoint(base_url, headers, project_id, model_id, display_name, description, locale):
    """
    Creates an endpoint using the model.
    """
    endpoint_url = f'{base_url}/v3.2/endpoints'
    print(endpoint_url)
    print(project_id, model_id)

    endpoint_body = {
        "model": {
            "self": f'{base_url}/v3.2/models/{model_id}'
        },
        "project": {
            "self": f'{base_url}/v3.2/projects/{project_id}'
        },
        "displayName": display_name,
        "description": description,
        "locale": locale,
        
    }
    
    print(endpoint_body)

    response = requests.post(endpoint_url, headers=headers, json=endpoint_body)
    response.raise_for_status()
    endpoint = response.json()
    endpoint_id = endpoint['self'].split('/')[-1]
    print(f'Create Endpoint and deploy job finished with ID: {endpoint_id}')
    return endpoint_id

def get_endpoint_status(base_url, headers, endpoint_id):
    """
    Polls the endpoint job until it completes.
    """
    endpoint_url = f'{base_url}/v3.2/endpoints/{endpoint_id}'
    response = requests.get(endpoint_url, headers=headers)
    response.raise_for_status()
    endpoint_info = response.json()
    return endpoint_info['status']


def delete_endpoint(base_url, headers, endpoint_id):
    """
    Deletes the endpoint identified by the given ID.
    """
    endpoint_url = f'{base_url}/v3.2/endpoints/{endpoint_id}'
    response = requests.delete(endpoint_url, headers=headers)
    status = response.raise_for_status()
    print(f'The endpoint deleted: {endpoint_id}, {status}')



def delete_project(base_url, headers, project_id):
    """
    Deletes the project_id identified by the given ID.
    """
    project_url = f'{base_url}/v3.2/projects/{project_id}'
    response = requests.delete(project_url, headers=headers)
    status = response.raise_for_status()
    print(f'The project deleted: {project_id}, {status}')    