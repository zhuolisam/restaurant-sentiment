# 📜resume-ranker

## How to Use?

For running the FastAPI backend server, you can do:
```bash
docker--compose up --build
#or 
docker--compose up -d

#OR
cd app
docker build . -t resume-ranker
docker run -i -p 8000:8000 resume-ranker
```

If you wish to install and run the whole project manually: 

Install all the dependencies:

```bash
./install.sh
```

Run the Streamlilt with:

```bash
cd app
streamlit run streamlit_app.py
```

Or run the demo with:

```bash
cd app
python demo.py
```
  