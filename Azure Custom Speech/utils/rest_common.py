import requests
import time
import json



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

def create_evaluation_dataset(base_url, headers, project_id, content_url, kind, display_name, description, locale):
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

def create_custom_model(base_url, headers, project_id, base_model_id, dataset_id, display_name, description, locale):
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
         "datasets": [
            {
            "self": f'{base_url}/v3.2/datasets/{dataset_id}'
            },
        ],
        "project": {
            "self": f'{base_url}/v3.2/projects/{project_id}'
        },
    }
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