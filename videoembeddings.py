import vertexai
import astrapy
import streamlit as st
from vertexai.vision_models import MultiModalEmbeddingModel, Video
from astrapy import DataAPIClient


# Initialize Vertex AI
vertexai.init(project=st.secrets['PROJECT'], location=st.secrets['REGION'])

# Initialize the client
client = DataAPIClient(st.secrets['ASTRA_TOKEN'])
database = client.get_database(st.secrets['ASTRA_API_ENDPOINT'])

my_collection = database.create_collection(
    "videodemo",
    dimension=1408,
    metric=astrapy.constants.VectorMetric.COSINE,
)

collectiondb = database.videodemo

# Load the pre-trained model and video
model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
video = Video.load_from_file(st.secrets['PATH'])

# Get embeddings with the specified contextual text
embeddings = model.get_embeddings(
    video=video,
    contextual_text="Mixed Content",
   # dimension=1408,
)

# Video Embeddings are segmented based on the video_segment_config.
#print("Video Embeddings:")
for video_embedding in embeddings.video_embeddings:
    # Check if embedding is a numpy array or a tensor and convert accordingly
    if isinstance(video_embedding.embedding, (list, tuple)):
        embedding_list = video_embedding.embedding
    else:
        embedding_list = video_embedding.embedding.tolist()

    embedding_data = {
     "metadata": {
        "start_offset_sec": video_embedding.start_offset_sec,
        "end_offset_sec": video_embedding.end_offset_sec
    },
    "$vector": embedding_list  # Ensure embedding is in list format
    }

    # Directly pass the dictionary to the insert_one method
    response = collectiondb.insert_one(embedding_data)
    print(response)
    