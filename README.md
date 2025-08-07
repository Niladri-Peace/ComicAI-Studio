
# ComicCrafter AI

ComicCrafter AI is a generative AI-based comic generator that runs locally on edge devices. It creates comic-style stories based on user prompts, leveraging state-of-the-art language and image generation models.

## Features

- Story generation using Large Language Models
- AI-powered comic-style image generation
- Four-part story structure: introduction, storyline, climax, and moral
- Local deployment on edge devices
- User-friendly web interface

## Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended)
- 8GB+ RAM
- Intel-based edge device for deployment

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/comiccrafter-ai.git
cd comiccrafter-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the required model weights (instructions in setup guide)

## Project Structure

```
comiccrafter-ai/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── modules/
│   ├── story_generator/  # LLM-based story generation
│   ├── image_generator/  # Image generation using Stable Diffusion
│   └── comic_composer/   # Comic composition and layout
├── models/               # Model weights and configurations
└── utils/               # Utility functions
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`
3. Enter your story prompt and click "Generate Comic"

## Technical Details

- Story Generation: Uses open-weight LLMs (Llama/Mistral) for coherent story generation
- Image Generation: Implements Stable Diffusion for comic-style image creation
- Web Interface: Built with Streamlit for easy interaction
- Edge Deployment: Optimized for Intel-based edge devices

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
