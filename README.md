# 🛡️ Disaster Severity Detector (Backend)

A production-ready, AI-powered backend designed to detect, categorize, and manage natural disaster reports in real-time. Built with **FastAPI**, **PyTorch**, and **Firebase**.

## 🏗️ Project Structure

```text
disaster_backend/
├── app/
│   ├── api/            # Route Controllers (Users, Reports, Admin, Webhooks)
│   ├── core/           # Security, Auth, and Firebase Config
│   ├── models/         # AI/ML Model Logic (PyTorch)
│   ├── schemas/        # Pydantic Data Validation
│   └── services/       # Database & Storage Operations
├── .env                # Secrets (Bucket names, API keys)
├── resnet_model.pth    # Trained PyTorch Weights
└── main.py             # App Entry Point

```

## 🚀 Getting Started

1. **Clone & Install**
```bash
git clone <your-repo-url>
python -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

```


2. **Environment Setup (`.env`)**
Create a `.env` file in the root:
```env
FIREBASE_BUCKET=your-app-id.appspot.com
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

```


3. **Firebase Credentials**
Place your `firebase-service-account.json` in the root folder.
4. **Run Server**
```bash
uvicorn app.main:app --reload

```



---

## 📡 API Endpoints Documentation

### 🔑 Authentication

All protected routes require a **Firebase ID Token** passed in the Header:
`Authorization: Bearer <ID_TOKEN>`

| Endpoint | Method | Role Required | Description |
| --- | --- | --- | --- |
| `/users/register` | `POST` | Any (Auth) | Links Firebase UID to a role (Citizen/NGO/Admin). |
| `/reports/create` | `POST` | **Citizen** | Uploads image, triggers AI analysis, saves to Firestore. |
| `/admin/reports` | `GET` | **Admin** | Fetches all global reports for oversight. |
| `/webhooks/stripe` | `POST` | Public | Receives payment confirmation events from Stripe. |

---

## 🛠️ Usage Examples

### 1. Register a User

**Request:**

```bash
curl -X POST "http://localhost:8000/users/register" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"role": "Citizen"}'

```

### 2. Upload Disaster Photo (AI Analysis)

**Request:** (Using `multipart/form-data`)

```bash
curl -X POST "http://localhost:8000/reports/create" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "file=@disaster_image.jpg"

```

**AI Response:**

```json
{
  "report_id": "8xKj29...",
  "disaster_type": "Flood",
  "severity": 94.2,
  "media_url": "https://storage.googleapis.com/...",
  "status": "Pending"
}

```

### 3. Stripe Webhook (Local Testing)

To test the webhook locally, use the Stripe CLI:

```bash
stripe listen --forward-to localhost:8000/webhooks/stripe

```

---

## 🤖 AI Model Logic

The backend utilizes a **ResNet50** architecture.

* **Input:** 224x224 RGB Image.
* **Classes:** `Flood`, `Fire`, `Earthquake`, `Accident`.
* **Logic:** Images are processed via `torchvision.transforms`, passed through the model, and the softmax highest-probability class is returned as the severity score.

