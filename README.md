# Reconnaissance

This project is leveraging [Insightface](https://github.com/deepinsight/insightface) and [FastAPI](https://github.com/tiangolo/fastapi) to create a simple face detection API. You can use it to extract bounding boxes, landmarks and some other pieces of information.

# Install

There are three ways of running the project: locally, on docker building from source, on docker pulled from the hub.

## Running locally

```bash
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000
```

## Running via a locally built image

```bash
docker build -t reconnaissance .
docker run -p 8000:8000 reconnaissance
```

## Running via the official image from the hub

```bash
docker pull rfrenoy/reconnaissance:0.1.0
docker run -p 8000:8000 rfrenoy/reconnaissance:0.1.0
```

## Making requests
Once your server is running, you can run a request on a picture with:
```bash
curl -X POST -F "file=@<path-to-image>" http://localhost:8000/detect_faces
```

It will return a JSON object with all informations for all detected faces.

Here is an example of a client in python that runs the request on a `test.png` file
and display the image with bounding boxes and landmarks:

```python
# client.py
import requests
from PIL import Image
import io
import matplotlib.pyplot as plt
import numpy as np

# Define the API endpoint URL
url = 'http://localhost:8000/detect_faces'

# Load the image as a PIL Image object
pil_image = Image.open('test.png')

# Convert the PIL Image object to bytes
with io.BytesIO() as output:
    pil_image.save(output, format="JPEG")
    image_bytes = output.getvalue()

# Send the POST request to the API endpoint
response = requests.post(url, files={'file': image_bytes}, timeout=60)

# Convert the PIL Image object to a NumPy array
image_array = np.array(pil_image)

# Create a Matplotlib figure and axis object
fig, ax = plt.subplots()

# Plot the image array
ax.imshow(image_array)

# Extract the bounding box and landmarks data from all faces in the JSON response
response_data = response.json()
for key in response_data:
    face = response_data[key]
    bounding_box = face['bbox']
    landmarks = face['landmark_2d_106']

    # Add the bounding box to the plot
    xmin, ymin, xmax, ymax = bounding_box
    ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                           fill=False, linewidth=1, color='g'))

    # Add the landmarks to the plot
    for landmark in landmarks:
        x, y = landmark
        ax.plot(x, y, 'ro', markersize=1)

# Display the plot
plt.show()
```
