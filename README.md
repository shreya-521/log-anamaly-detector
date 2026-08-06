# log-anamaly-detector

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shreya-521/log-anamaly-detector)

FastAPI microservice that flags suspicious logs using ML.

## Features
- FastAPI Backend with Scikit-learn Isolation Forest ML model
- Beautiful, real-time "Red & Black" UI for monitoring logs
- Instantly runnable in the cloud via GitHub Codespaces

## Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Then visit http://localhost:8000/static/index.html
