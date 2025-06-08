Here’s your updated **README** with a **License** section and your **Contact Information** included at the bottom:

---

# 🏦 Credit Approval System

A Django-based backend system for managing customer loan approvals, checking eligibility, and tracking loan data. This project includes APIs for customer registration, loan eligibility checks, and loan creation, along with a PostgreSQL database and Dockerized infrastructure.

> 📌 *This project was developed as part of a backend engineering assignment for a company evaluation.*

---

## 🚀 Features

* Register new customers with automatic approved limit calculation.
* Check loan eligibility based on credit score, income, and other factors.
* Create and view individual or all loans for a customer.
* Ingest sample loan and customer data via Excel.
* Background processing using Celery (for advanced tasks).
* Fully containerized with Docker and Docker Compose.
* Unit tests for key API endpoints (bonus point-ready 💡).

---

## 🧰 Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL
* **Task Queue:** Celery with Redis
* **Containerization:** Docker, Docker Compose
* **Testing:** Django TestCase / DRF’s APITestCase
* **Data Ingestion:** Pandas with Excel files

---

## 🛠️ Setup Instructions

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-username/credit-approval-system.git
   cd credit-approval-system
   ```

2. **Run the project**

   ```bash
   docker-compose up --build
   ```

3. **Run unit tests (optional/bonus)**

   ```bash
   docker-compose exec web python manage.py test loan
   ```

4. **Access the API**
   Visit `http://localhost:8000/`

---

## 📁 Project Structure (Simplified)

```
credit_approval_project/
├── credit_approval/          # Django project settings & core config
├── loan/                     # Main app: views, models, serializers, urls
│   ├── sample_data/          # Excel files for initial data
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Compose config for app + db + redis
```

---

## ✅ Sample Endpoints

* `POST /register` – Register new customer
* `POST /check-eligibility` – Check loan eligibility
* `POST /create-loan` – Create a new loan
* `GET /view-loan/<loan_id>` – View a specific loan
* `GET /view-loans/<customer_id>` – View all loans for a customer

---

## 🧪 Testing

Includes unit tests using Django’s built-in test framework:

```bash
docker-compose exec web python manage.py test loan
```

---
## Live Demo (working) video
https://drive.google.com/file/d/1rwzndC8cxJpu-4r7leM59kR-MnMCWaoI/view

## 📄 License

This project was developed as part of a private company assignment.
**For evaluation and educational use only.**
Please do not distribute or use for commercial purposes without permission.

---

## 📬 Contact

* **LinkedIn:** [https://www.linkedin.com/in/utkarshsingh1702](https://www.linkedin.com/in/utkarshsingh1702)
* **Email:** [utkarshthakur17022002@gmail.com](mailto:utkarshthakur17022002@gmail.com)
* **Phone:** +91-6387463741

---
