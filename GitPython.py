import os
import subprocess
import requests
from git import Repo

def create_github_repository(token, repo_name):
    create_repo_endpoint = 'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    repo_data = {
        'name': repo_name,
        'auto_init': False
    }
    response = requests.post(create_repo_endpoint, headers=headers, json=repo_data)

    if response.status_code == 201:
        print(f'Success: Repository {repo_name} created successfully!')
    else:
        print(f'Error: Failed to create repository. Status code: {response.status_code}, Response: {response.text}')
        exit()

def generate_github_workflow(repo_dir, script_name):
    workflow_dir = os.path.join(repo_dir, '.github', 'workflows')
    os.makedirs(workflow_dir, exist_ok=True)

    workflow_content = f"""\
name: Python Workflow

on:
  push:
    branches:
      - master

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Python script
      run: python {script_name}
"""

    workflow_file_path = os.path.join(workflow_dir, 'covid_workflow.yml')

    with open(workflow_file_path, 'w') as file:
        file.write(workflow_content)

    print("Success: GitHub Actions workflow file created.")
    subprocess.run('git add .', shell=True)
    subprocess.run('git commit -m "test"', shell=True)
    subprocess.run('git push', shell=True)

# Your actual details
repo_directory = r'C:\Users\serge\Desktop\GithubPython\covid'  # Directory where you want to clone the repo
repository_url = "https://github.com/CDCgov/wastewater-informed-covid-forecasting.git"  # Repository you want to clone
your_github_username = "sergenoumbet"  # Your GitHub username
your_repository_name = "wastewater-informed-covid"  # Your repository name
github_access_token = ""  # Reminder: Refresh or revoke this token since it's now public

# Create a new GitHub repository
create_github_repository(token=github_access_token, repo_name=your_repository_name)

# Clone the repository if not already cloned
if not os.path.exists(repo_directory):
    Repo.clone_from(repository_url, repo_directory)
    print(f"Success: Repository cloned into {repo_directory}")

cloned_repository = Repo(repo_directory)

# Set up remote
origin_remote_exists = 'origin' in [remote.name for remote in cloned_repository.remotes]
if origin_remote_exists:
    origin = cloned_repository.remotes.origin
    origin.set_url(f'https://{your_github_username}:{github_access_token}@github.com/{your_github_username}/{your_repository_name}.git')
else:
    cloned_repository.create_remote('origin', f'https://{your_github_username}:{github_access_token}@github.com/{your_github_username}/{your_repository_name}.git')

print("Success: Remote 'origin' is set up.")

# Generate and add GitHub Actions workflow
os.chdir(repo_directory)
generate_github_workflow(repo_dir=repo_directory, script_name=r'GitPythonUpdated.py')
