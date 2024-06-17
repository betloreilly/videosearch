# Video Search App

This application allows users to search for specific content within videos using text descriptions or similar images. It leverages Google Cloud's Vertex AI for generating embeddings and Astra DB for data storage.

[![Video Search](/Users/betuloreilly/repo/videosearch/thumbnail.png)](/Users/betuloreilly/repo/videosearch/videosearch.mp4)


## Prerequisites

- Python 3.7 or higher
- Google Cloud SDK
- Astra DB account

## Setup Instructions

### 1. Create a Virtual Environment

1. **Install `virtualenv`** (if not already installed):
   ```sh
   pip install virtualenv

2. **Create a virtual environment**:
   ```sh
   python -m venv myenv

3. **Activate the virtual environment**:
    
    On Windows:

    myenv\Scripts\activate

    On macOS/Linux:

    source myenv/bin/activate

2. **Install Required Packages**
    ```sh
    pip install -r requirements.txt

3. **Set Up Google Authentication**
* Initialize Google Cloud SDK:
    ```sh
    gcloud init

* Authenticate: 
    ```sh
    gcloud auth application-default login

4. **Configure Environment Variables**

Create a `.streamlit/secrets.toml` file in the root directory of your project and add your configuration details:

```toml
PROJECT = "your-gcp-project-id"
REGION = "your-gcp-region"
ASTRA_TOKEN = "your-astra-db-token"
ASTRA_API_ENDPOINT = "your-astra-db-endpoint"
IMAGE_PATH = "path-to-save-uploaded-image.png"
PATH = "path-to-your-video-file.mp4"
```

5. **Run the Application**

* Prepare the embedding of the video:
    ```sh
    python videoembeddings.py

* Execute the Streamlit application:
    ```sh
    streamlit run app.py
