# Flask + Vite React Starter 🚀

A lightweight full-stack boilerplate using:
- **Flask** (Python backend API)
- **React with Vite** (Fast frontend tooling)
- **CORS enabled** for development

---

## 📦 Project Structure

```
flask-react-app/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── venv/
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── src/
    └── dist/
```

---

## 🛠️ Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <repo-url>
cd flask-react-app
```

---

## 🐍 Backend Setup (Flask)

### Create Virtual Environment

**For Windows:**

```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**For Mac/Linux:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Flask Server

```bash
python app.py
```

✅ **Backend running at:** `http://127.0.0.1:5000`

---

## ⚛️ Frontend Setup (React + Vite)

From your project root directory:

```bash
cd frontend
npm install
npm run dev
```

✅ **Frontend running at:** `http://localhost:5173`

---

## 🔌 API Connection

### Option 1: Direct API Calls

```javascript
// src/App.jsx
import axios from 'axios';

axios.get('http://127.0.0.1:5000/api/data')
  .then(res => console.log(res.data))
  .catch(err => console.error(err));
```

### Option 2: Using Vite Proxy (Recommended)

Update `vite.config.js`:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    }
  }
})
```

Then call API from React:

```javascript
axios.get('/api/data')
  .then(res => console.log(res.data))
  .catch(err => console.error(err));
```

---

## 📦 Build for Production

```bash
cd frontend
npm run build
```

✅ **Production files:** `frontend/dist/`

---

## ⚙️ Backend Configuration (Flask)

### `backend/app.py` Example

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/api/data', methods=['GET'])
def get_data():
    return {'message': 'Hello from Flask!'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### `backend/requirements.txt`

```
Flask==2.3.2
Flask-CORS==4.0.0
python-dotenv==1.0.0
```

---

## 📝 Important Notes

- ✅ Start **backend first**, then frontend
- ✅ Backend runs on `http://127.0.0.1:5000`
- ✅ Frontend runs on `http://localhost:5173`
- ✅ Use `deactivate` to exit virtual environment
- ✅ Requires Python 3.8+ and Node.js 18+
- ✅ CORS is enabled for development

---

## 🚀 Development Workflow

1. Open terminal, go to `backend/` folder
2. Activate virtual environment
3. Run `python app.py`
4. Open another terminal, go to `frontend/` folder
5. Run `npm run dev`
6. Open `http://localhost:5173` in browser

---

## 📂 Serving Frontend from Flask (Optional)

To serve React build from Flask:

```python
import os
from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
CORS(app)

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    return {'message': 'Hello from Flask!'}

if __name__ == '__main__':
    app.run(debug=False, port=5000)
```

Then run `npm run build` in frontend before deploying.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `npm: command not found` | Install Node.js from nodejs.org |
| `CORS error` | Ensure `CORS(app)` is in Flask app |
| `Port 5000 already in use` | Change port: `app.run(port=5001)` |
| `Port 5173 already in use` | Vite will use next available port |

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
