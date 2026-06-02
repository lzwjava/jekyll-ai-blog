FROM ubuntu:latest

# Update package lists
RUN apt-get update

# Install necessary packages
RUN apt-get install -y \
    python3 \
    python3-pip \
    git \
    ffmpeg \
    ttf-mscorefonts-installer \
    fonts-noto \
    fonts-noto-cjk \
    fonts-dejavu \
    texlive-latex-extra \
    pandoc \
    wget \
    unzip

# Accept the Microsoft fonts license
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections

# Install texlive packages
RUN apt-get update && apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-recommended texlive-pictures cm-super

# Clean up apt cache
RUN apt-get clean

# Set working directory
WORKDIR /app

# Copy the entire repository
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Download and install fonts (if needed)
# This is an example, adjust as necessary
# RUN wget -q -O /tmp/fonts.zip "https://example.com/path/to/fonts.zip" && \
#     unzip /tmp/fonts.zip -d /usr/share/fonts/ && \
#     fc-cache -f -v

# Make scripts executable (if needed)
RUN chmod +x /app/scripts/*.py

# Set environment variables (if needed)
# ENV DEEPSEEK_API_KEY=your_deepseek_api_key
# ENV GITHUB_TOKEN=your_github_token
# ENV MISTRAL_API_KEY=your_mistral_api_key
# ENV GEMINI_API_KEY=your_gemini_api_key
# ENV GCP_SA_KEY=your_gcp_sa_key

# Command to run (if needed, adjust as necessary)
# CMD ["python3", "/app/your_script.py"]
