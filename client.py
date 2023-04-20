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
