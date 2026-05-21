import os
import tempfile

import streamlit as st
import torch
import clip
from PIL import Image

# ----------------------------
# Streamlit setup
# ----------------------------
st.set_page_config(page_title="Mini Visual Search", layout="wide")

st.title("🔍 Confidence-Aware Mini Visual Search")
st.write("Upload 6–12 images, enter a text query, and get the top 3 matches using CLIP.")

# ----------------------------
# Load CLIP model
# ----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

@st.cache_resource
def load_clip_model():
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess

clip_model, clip_preprocess = load_clip_model()

# ----------------------------
# Sidebar
# ----------------------------
confidence_threshold = st.sidebar.number_input(
    "Low-confidence threshold (%)",
    min_value=0,
    max_value=100,
    value=25,
    step=1
)

# ----------------------------
# Inputs
# ----------------------------
uploaded_files = st.file_uploader(
    "Upload 6–12 images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

user_prompt = st.text_input(
    "Search query",
    placeholder="Example: black car parked outside"
)

# ----------------------------
# CLIP analysis function
# ----------------------------
def analyze_images(image_paths, prompt):
    results = []

    text = clip.tokenize([prompt]).to(device)

    with torch.no_grad():
        text_features = clip_model.encode_text(text)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    for image_path in image_paths:
        try:
            image = Image.open(image_path).convert("RGB")
            image_input = clip_preprocess(image).unsqueeze(0).to(device)

            with torch.no_grad():
                image_features = clip_model.encode_image(image_input)
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)

                similarity = torch.nn.functional.cosine_similarity(
                    image_features,
                    text_features
                )

            confidence = similarity.item() * 100

            results.append({
                "path": image_path,
                "confidence": confidence
            })

        except Exception:
            continue

    return results

# ----------------------------
# Search button
# ----------------------------
if st.button("Search"):
    if not uploaded_files:
        st.error("Please upload images first.")
    elif len(uploaded_files) < 6 or len(uploaded_files) > 12:
        st.error("Please upload between 6 and 12 images.")
    elif not user_prompt:
        st.error("Please enter a search query.")
    else:
        temp_paths = []

        with st.spinner("Analyzing images with CLIP..."):
            for file in uploaded_files:
                suffix = os.path.splitext(file.name)[1]

                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_file.write(file.read())
                    temp_paths.append(temp_file.name)

            results = analyze_images(temp_paths, user_prompt)
            results.sort(key=lambda x: x["confidence"], reverse=True)

        top_3 = results[:3]

        st.subheader("Top 3 Matches")

        if top_3[0]["confidence"] < confidence_threshold:
            st.warning(
                "Low confidence: results may not match well. "
                "Try a more specific query, like 'black car parked outside' instead of just 'car'."
            )

        cols = st.columns(3)

        for i, result in enumerate(top_3):
            with cols[i]:
                st.image(Image.open(result["path"]), use_container_width=True)
                st.write(f"Confidence: `{result['confidence']:.2f}%`")
                st.caption("CLIP + cosine similarity")

        st.info(
            f"Threshold used: {confidence_threshold}%. "
            "If the best match is below this, the app warns the user."
        )

        for path in temp_paths:
            if os.path.exists(path):
                os.unlink(path)