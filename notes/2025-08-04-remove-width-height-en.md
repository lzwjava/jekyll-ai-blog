---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remove `width` and `height`
translated: false
type: note
---

The error you're seeing:

```
Extra inputs are not permitted [type=extra_forbidden, input_value=1200, input_type=int]
```

is caused by passing `width` and `height` into `GenerateImagesConfig`, which does **not support** those fields. According to the error message and Gemini's API design, `image_size` must be one of the **predefined enum values**, and `CUSTOM` is **not** supported for the public Gemini API (as of now).

---

### ✅ Fix

You should **remove** `width` and `height`, and use a valid `image_size` enum such as `"1024x1024"` or `"512x512"`.

Here’s the corrected version:

```python
from google import genai
from google.genai.types import GenerateImagesConfig
import os

# Set up Vertex AI client
client = genai.Client(
    vertexai=True,
    project=os.getenv('GOOGLE_CLOUD_PROJECT'),
    location=os.getenv('GOOGLE_CLOUD_LOCATION')
)

image = client.models.generate_images(
    model="imagen-4.0-generate-preview-06-06",
    prompt="A dog reading a newspaper",
    config=GenerateImagesConfig(
        image_size="1024x1024",  # use allowed value instead of CUSTOM
        number_of_images=1,
        safety_filter_level="BLOCK_LOW_AND_ABOVE",
        person_generation="ALLOW_ADULT",
    ),
)

print(f"Created OG image using {len(image.generated_images[0].image.image_bytes)} bytes")
```

---

### 🔍 To generate a **custom-sized image** like `1200x630`

The current Gemini/Imagen public APIs **do not support** arbitrary image sizes. If you need 1200×630 (e.g., for OG images), your options are:

1. **Post-process the image** after generation to resize/crop to your desired dimensions.
2. Use **a different model/API** that supports custom dimensions (e.g., Stability AI's SDXL, Midjourney, or private endpoints).
3. If you're using internal access (e.g., inside Google), confirm with the internal docs or your Vertex AI account manager.

Let me know if you want help resizing the image after it's generated.
