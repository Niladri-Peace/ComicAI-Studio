## 🎨 ComicCrafter AI

**ComicCrafter AI** is a generative AI-powered comic story creator. It uses cutting-edge language and image generation tools to turn text prompts into structured comic stories — designed to run locally on edge devices.

---

### 🚀 Features

* ✍️ Story generation using Large Language Models (LLMs)
* 🖼️ Comic-style image generation (Stable Diffusion-ready)
* 🧠 Four-part structure: *Introduction → Storyline → Climax → Moral*
* 💻 Local-first deployment (privacy-friendly)
* 🌐 Simple and interactive web interface (HTML templates)

---

### ⚙️ Requirements

* Python 3.8+
* 8GB+ RAM
* CUDA-compatible GPU (for image generation)
* Intel-based edge device (for deployment)

---

### 📦 Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/ComicAI-Studio.git
   cd ComicAI-Studio
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

### 📂 Project Structure

```
ComicAI-Studio/
├── app.py              # Main app entrypoint
├── server.py           # Flask server (API handler)
├── minimal_server.py   # Lightweight server (optional)
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates for UI
├── vercel.json         # Vercel deployment config
└── README.md           # Project documentation
```

---

### ▶️ Usage

**To run locally:**

```bash
python server.py
```

Then open your browser at `http://localhost:5000`

---

### ☁️ Deployment (Vercel)

1. Push to GitHub with `vercel.json` in root.
2. Connect to [Vercel](https://vercel.com/) and import the GitHub repo.
3. Set up Python build and deploy.

---

### 📖 License

This project is released under the [MIT License](LICENSE).

---

### 🤝 Contributing

Pull requests are welcome! Please fork the repo and open a PR.
