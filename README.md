# 📜resume-ranker

## API Endpoint

The endpoint is built with the blazingly fast Python web framework FastAPI, and is hosted on AWS serverless Lambda function, via Elastic Container Registry (ECR) and Lambda's function URL. You can find the endpoint [here](https://rtqf5s4ihfoirzcpugpvcddoqy0obhrj.lambda-url.us-east-1.on.aws/).

If you are interested, you can find the steps to deploy the FastAPI app in this [article](https://medium.com/analytics-vidhya/python-fastapi-and-aws-lambda-container-3e524c586f01).

## How to Use?

You have two options, to use it via streamlit interface or use it as a backend service, which is FastAPI. 


**If you wish to run the FastAPI backend service with docker:**
```bash
docker--compose up --build
#or 
docker--compose up -d

#OR
cd app
docker build . -t resume-ranker
docker run -i -p 8000:8000 resume-ranker
```

**If you wish to install and run the whole project manually:**

Install all the dependencies:

```bash
./install.sh
```

Run the Streamlit with:

```bash
cd app
streamlit run streamlit_app.py
```

Or run the FastAPI backend with:
```bash
cd app
uvicorn main:app --reload
```

Or run the demo with:

```bash
cd app
python demo.py
```
  