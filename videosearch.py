import vertexai
from vertexai.vision_models import MultiModalEmbeddingModel, Video
from vertexai.vision_models import Image as img
from astrapy import DataAPIClient
import streamlit as st
from PIL import Image

st.title("Video Search App")

# Text input
user_input_placeholder = st.empty()
user_input = user_input_placeholder.text_input(
    "Describe the content you're looking for:", key="user_input"
)

uploaded_file = st.file_uploader("Choose an image file that is similar you're looking for", type="png")

if uploaded_file is not None:
    # Read the uploaded PNG file
    image = Image.open(uploaded_file)

    # Define the path to save the file locally
    image_path = "/Users/betuloreilly/repo/vertexvideo/saved_image.png"

    # Save the image locally
    image.save(image_path)

    # Open and display the saved image to verify
    saved_image = Image.open(image_path)
    st.image(saved_image, caption='', use_column_width=True)
     

# Initialize Vertex AI
vertexai.init(project=st.secrets['PROJECT'], location=st.secrets['REGION'])


# Initialize the client
client = DataAPIClient(st.secrets['ASTRA_TOKEN'])
database = client.get_database(st.secrets['ASTRA_API_ENDPOINT'])
collectiondb = database.videosearch

# Load the pre-trained model and video
model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
video = Video.load_from_file(st.secrets['PATH'])

# Search action trigger
if st.button("Search"):
    if user_input:
        embeddings = model.get_embeddings(
            contextual_text=user_input
        )
        result = collectiondb.find_one({}, vector=embeddings.text_embedding)
        start_offset_value = result['metadata']['start_offset_sec']
        end_offset_value = result['metadata']['end_offset_sec']
        st.write("Text input result found between: " + str(start_offset_value) + "-" + str(end_offset_value))
        
        video_file = open(st.secrets['PATH'], 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes, start_time=start_offset_value)
        
    if uploaded_file is not None:
        embimage = img.load_from_file(image_path)
        embeddingsimg = model.get_embeddings(
            image=embimage
        )
        imgresult = collectiondb.find_one({}, vector=embeddingsimg.image_embedding)
        start_offset_value = imgresult['metadata']['start_offset_sec']
        end_offset_value = imgresult['metadata']['end_offset_sec']
        st.write("Image input result found between: " + str(start_offset_value) + "-" + str(end_offset_value))
        
        video_file = open(st.secrets['PATH'], 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes, start_time=start_offset_value)