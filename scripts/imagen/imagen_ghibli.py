import os
from google import genai
from google.genai import types
from PIL import Image as PILImage
from io import BytesIO

# 1. Init GenAI client
client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
)

# 2. Load your base avatar
base_image_path = "assets/images/avatar/avatar.jpg"
input_img = PILImage.open(base_image_path)

# 3. Define your edit prompt
prompt = (
    "Transform this image into the style of a Studio Ghibli film. "
    "Use a hand-painted watercolor aesthetic with a soft, vibrant palette. "
    "Lighting should be warm and golden, creating a nostalgic, whimsical atmosphere."
)

# 4. Call the Imagen 3 edit model by its published ID
response = client.models.generate_content(
    model="image_edit_auto",  # Imagen 3 editing endpoint :contentReference[oaicite:0]{index=0}
    contents=[prompt, input_img],
    config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
)

# 5. Extract & save the edited image
for part in response.candidates[0].content.parts:
    if part.inline_data:
        edited = PILImage.open(BytesIO(part.inline_data.data))
        edited.save("ghibli_style_output.png")
        print("✅ Saved Ghibli-style output to ghibli_style_output.png")
