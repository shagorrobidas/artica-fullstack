# Artica Fullstack - Multimedia Educational Platform

Artica Fullstack is a production-ready, dynamic multimedia educational platform built with Python and Django. It provides a robust Content Management System (CMS) designed for rich interactivity, featuring a hierarchical category system, an intelligent glossary, and a versatile media manager.

## 🚀 Key Features

- **Hierarchical content Discovery**: Organize articles through a 3-level hierarchy (Category > Subcategory > Sub-subcategory) for intuitive navigation.
- **Interactive Glossary**: Automatic term highlighting within article bodies. Clicking a term opens a modal with detailed explanations, images, and resources without leaving the page.
- **Rich Media Management**: Attach diverse media types to articles, including:
  - High-resolution Images
  - Hosted Video and Audio
  - YouTube Embeds
  - Supplementary Text blocks
- **Deep-Dive Sections**: Structured article content using responsive accordion sections for better readability.
- **Full-Text Search**: Robust search capabilities across articles and metadata.
- **Modern UI/UX**: Built with Bootstrap 5 and Boxicons, featuring a sleek, responsive design with glassmorphism elements and smooth transitions.

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, Django 4.2+
- **Frontend**: HTML5, JavaScript (ES6+), Bootstrap 5, Boxicons
- **Rich Text**: Django CKEditor
- **Styling**: Custom Vanilla CSS
- **Database**: SQLite (Development), PostgreSQL ready (Production)
- **Asset Management**: WhiteNoise

## 📥 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/shagorrobidas/artica-fullstack.git
cd artica-fullstack
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements/development.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory based on `.env.example`:
```bash
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to view the platform.

## 📂 Project Structure

```text
├── apps/
│   ├── api/            # REST API endpoints
│   ├── articles/       # Core article logic and models
│   ├── categories/     # Hierarchical category management
│   ├── glossary/       # Term mapping and highlighting logic
│   ├── media_manager/  # Multimedia attachment handling
│   └── search/         # Search indexing and views
├── config/             # Project settings (split for dev/prod)
├── static/             # CSS, JS, and global assets
├── templates/          # Django HTML templates (split into partials)
└── manage.py
```

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---
Built with ❤️ for advanced digital learning.
