import io
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from insightface.app import FaceAnalysis

app = FastAPI()

# Load the InsightFace face analysis model
face_app = FaceAnalysis(det_name="retinaface_r50_v1", rec_name="arcface_r100_v1")
face_app.prepare(ctx_id=0, det_size=(640, 640))


@app.post("/detect_faces")
async def detect_face(file: UploadFile = File(...)):
    contents = await file.read()
    image = np.array(Image.open(io.BytesIO(contents)).convert("RGB"))

    # Run the face detection and landmark detection models on the image
    faces = face_app.get(image)
    face_dict = {}

    # Extract the face information and add it to the dictionary
    for idx, face in enumerate(faces):
        face_dict[idx] = {
            "bbox": face.bbox.tolist(),
            "kps": face.kps.tolist(),
            "det_score": str(face.det_score),
            "landmark_3d_68": face.landmark_3d_68.tolist(),
            "pose": face.pose.tolist(),
            "landmark_2d_106": face.landmark_2d_106.tolist(),
            "gender": str(face.gender),
            "age": str(face.age),
            "embedding": face.embedding.tolist(),
        }

    # Return the dictionary as a JSON object
    return face_dict
