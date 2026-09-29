# Doctor Patient Management API

A production-style REST API built with **FastAPI** for managing doctors, patients, and appointments.

The application includes JWT authentication, role-based authorization, database persistence, validation, appointment management, audit tracking, performance monitoring, rate limiting, centralized error handling, and automated testing.

---

## 1. Project Overview

The **Doctor Patient Management API** provides backend services for:

* User registration and authentication
* JWT-based authorization
* Doctor management
* Patient management
* Doctor-patient assignment
* Appointment management
* Role-based access control
* Database persistence using SQLAlchemy
* Data validation and integrity
* Audit tracking
* Performance monitoring
* API hardening
* Automated testing

---

## 2. Technologies Used

* **Python 3.9+**
* **FastAPI**
* **Pydantic**
* **SQLAlchemy**
* **SQLite**
* **JWT Authentication**
* **Uvicorn**
* **Pytest**
* **HTTPX**
* **Passlib / Password Hashing**
* **python-multipart**
* **python-dotenv**

---

## 3. Project Structure

```text
doctor-patient-api/
│
├── app/
│   ├── auth/
│   │   ├── router.py
│   │   └── utils.py
│   │
│   ├── routes/
│   │   ├── doctors.py
│   │   ├── patients.py
│   │   └── appointments.py
│   │
│   ├── services/
│   │   ├── doctor_service.py
│   │   ├── patient_service.py
│   │   └── appointment_service.py
│   │
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── tests/
│   ├── test_api.py
│   ├── test_services.py
│   └── test_auth.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── doctor_patient.db
```

---

## 4. Installation

Clone the repository or download the project files.

Create and activate a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

---

## 5. Environment Configuration

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=sqlite:///./doctor_patient.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The `.env` file should not be committed to GitHub if it contains real secrets.

---

## 6. Running the Application

Start the FastAPI application using Uvicorn:

```powershell
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

## 7. API Documentation

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

Swagger provides:

* Endpoint documentation
* Request parameters
* Request examples
* Response schemas
* Authentication support
* Authorization testing
* Validation information

---

# 8. Authentication

The API uses **JWT Bearer Token authentication**.

### Register

```http
POST /api/v1/auth/register
```

Example request:

```json
{
  "name": "Lavanya Reddy",
  "email": "lavanya@gmail.com",
  "password": "password123",
  "role": "doctor"
}
```

Supported roles:

```text
admin
doctor
```

### Login

```http
POST /api/v1/auth/login
```

Login returns a JWT access token.

Example response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

Use the token in Swagger through the **Authorize** button:

```text
Bearer <access_token>
```

Protected endpoints require authentication.

---

# 9. Role-Based Authorization

The API supports two roles:

## Admin

Admins have full access to Doctor, Patient, and Appointment management.

Admin permissions include:

* Create doctors
* View doctors
* Update doctors
* Deactivate doctors
* Create patients
* View patients
* Update patients
* Delete patients
* Assign patients to doctors
* Manage appointments

## Doctor

Doctors have restricted access.

Doctor permissions include:

* View their assigned patients
* View their assigned patient details
* View their appointments

Doctors cannot:

* Create doctors
* Update doctors
* Delete/deactivate doctors
* Create or update patients
* Delete patients
* Access another doctor's assigned patients

Unauthorized access returns:

```http
403 Forbidden
```

---

# 10. Doctor APIs

### Create Doctor

```http
POST /api/v1/doctors/
```

Admin only.

Example:

```json
{
  "name": "Dr. Rathi",
  "specialization": "Cardiology",
  "email": "rathi@gmail.com",
  "is_active": true
}
```

### Get Doctors

```http
GET /api/v1/doctors/
```

Supports:

* Pagination
* Specialization filtering
* Active/inactive filtering

Example:

```text
/api/v1/doctors/?specialization=Cardiology&page=1&limit=10
```

### Get Doctor

```http
GET /api/v1/doctors/{doctor_id}
```

### Update Doctor

```http
PUT /api/v1/doctors/{doctor_id}
```

### Partially Update Doctor

```http
PATCH /api/v1/doctors/{doctor_id}
```

### Deactivate Doctor

```http
DELETE /api/v1/doctors/{doctor_id}
```

The delete operation performs a **soft delete** by setting:

```text
is_active = false
```

### Get Doctor's Patients

```http
GET /api/v1/doctors/{doctor_id}/patients
```

Admins can access any doctor's patients.

Doctors can access only their own assigned patients.

---

# 11. Patient APIs

### Create Patient

```http
POST /api/v1/patients/
```

Admin only.

Example:

```json
{
  "name": "Meena",
  "age": 25,
  "phone": "8688094563",
  "doctor_id": 1
}
```

### Get Patients

```http
GET /api/v1/patients/
```

Supports pagination and age filtering.

Example:

```text
/api/v1/patients/?age_gt=25&page=1&limit=10
```

Admins can view all patients.

Doctors can view only their assigned patients.

### Get Patient

```http
GET /api/v1/patients/{patient_id}
```

### Update Patient

```http
PUT /api/v1/patients/{patient_id}
```

Admin only.

### Partially Update Patient

```http
PATCH /api/v1/patients/{patient_id}
```

Admin only.

### Delete Patient

```http
DELETE /api/v1/patients/{patient_id}
```

Admin only.

### Assign Patient to Doctor

```http
PUT /api/v1/patients/{patient_id}/assign-doctor/{doctor_id}
```

Only active doctors can be assigned.

---

# 12. Appointment Module

The Appointment module manages appointments between doctors and patients.

## Appointment Fields

| Field            | Description                           |
| ---------------- | ------------------------------------- |
| id               | Unique appointment ID                 |
| doctor_id        | Assigned doctor                       |
| patient_id       | Assigned patient                      |
| appointment_date | Date and time of appointment          |
| status           | Appointment status                    |
| created_at       | Creation timestamp                    |
| updated_at       | Last update timestamp                 |
| created_by       | User who created the appointment      |
| updated_by       | User who last updated the appointment |

## Appointment Status

Supported statuses:

```text
scheduled
completed
cancelled
```

### Create Appointment

```http
POST /api/v1/appointments/
```

Example:

```json
{
  "doctor_id": 1,
  "patient_id": 1,
  "appointment_date": "2026-10-01T10:00:00",
  "status": "scheduled"
}
```

### Get Appointments

```http
GET /api/v1/appointments/
```

### Get Appointment

```http
GET /api/v1/appointments/{appointment_id}
```

### Update Appointment

```http
PUT /api/v1/appointments/{appointment_id}
```

### Partially Update Appointment

```http
PATCH /api/v1/appointments/{appointment_id}
```

### Delete Appointment

```http
DELETE /api/v1/appointments/{appointment_id}
```

### Get Doctor Appointments

```http
GET /api/v1/doctors/{doctor_id}/appointments
```

### Get Patient Appointments

```http
GET /api/v1/patients/{patient_id}/appointments
```

---

# 13. Appointment Validation

The application validates appointment data before saving it.

### Doctor Validation

* Doctor must exist.
* Doctor must be active.

### Patient Validation

* Patient must exist.

### Appointment Overlap

Overlapping scheduled appointments for the same doctor are prevented.

This protects the system from assigning multiple conflicting appointments to the same doctor.

---

# 14. Data Integrity

The application uses SQLAlchemy and database constraints to maintain data integrity.

Implemented constraints include:

* Unique doctor email
* Unique user email
* Foreign key relationships
* Required database fields
* Doctor-patient relationships
* Doctor-appointment relationships
* Patient-appointment relationships

SQLite foreign key enforcement is enabled.

Database integrity errors are handled centrally and returned using a consistent error response.

---

# 15. Validation

Pydantic validation is used for request data.

### Patient Age

Patient age must be greater than zero.

Example invalid value:

```json
{
  "age": 0
}
```

Returns:

```http
422 Unprocessable Entity
```

### Patient Phone

Phone number must contain exactly 10 digits.

Example:

```text
8688094563
```

### Email

Doctor and user email fields must contain valid email addresses.

### Appointment Status

Only the following values are accepted:

```text
scheduled
completed
cancelled
```

---

# 16. Pagination

List APIs support pagination.

Example:

```text
?page=1&limit=10
```

Pagination response:

```json
{
  "total": 25,
  "page": 1,
  "limit": 10,
  "data": []
}
```

The maximum page size is limited to 100 records.

---

# 17. Performance and Query Optimization

The application includes basic performance improvements.

### SQLAlchemy Optimization

`joinedload()` is used where appropriate to reduce unnecessary relationship queries.

### Database Indexes

Indexes are applied to frequently queried fields such as:

* User ID
* User email
* Doctor ID
* Doctor email
* Patient ID
* Patient doctor ID
* Appointment ID
* Appointment doctor ID
* Appointment patient ID
* Appointment date

### Response-Time Measurement

The API adds an `X-Process-Time` response header.

Example:

```text
X-Process-Time: 0.0042
```

This allows API response processing time to be observed during testing.

---

# 18. Audit Tracking

The application tracks creation and modification information.

Audit fields include:

```text
created_at
updated_at
created_by
updated_by
```

`created_by` and `updated_by` are populated using the authenticated user's JWT identity.

This provides basic traceability for database changes.

---

# 19. API Hardening and Reliability

The application includes centralized reliability features.

## Global Exception Handling

Unexpected server errors return a consistent response:

```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred."
}
```

## Validation Error Handling

Validation errors use a consistent structure:

```json
{
  "error": "Validation error",
  "message": "The request contains invalid data.",
  "details": []
}
```

## Database Error Handling

Database integrity errors return:

```json
{
  "error": "Database integrity error",
  "message": "The requested operation violates a database constraint."
}
```

## Rate Limiting

Basic IP-based rate limiting is implemented.

The current configuration allows:

```text
60 requests per minute per client IP
```

When the limit is exceeded:

```http
429 Too Many Requests
```

is returned.

---

# 20. Health Check

The application provides a health-check endpoint:

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

# 21. API Root

```http
GET /
```

Example response:

```json
{
  "message": "Doctor Patient API is running",
  "version": "2.0.0"
}
```

---

# 22. Testing

The project uses **Pytest** for automated testing.

Run all tests:

```powershell
pytest tests -v
```

The implemented test suite covers:

* Root endpoint
* Health check
* User registration
* Duplicate registration
* Invalid roles
* Login
* Invalid password
* JWT authentication
* Admin authorization
* Doctor authorization
* Doctor CRUD
* Patient CRUD
* Patient assignment
* Appointment CRUD
* Appointment validation
* Appointment overlap validation
* Service-layer validation
* Request validation
* Role restrictions

### Latest Test Result

```text
41 passed
```

The test suite verifies the main authentication, authorization, business logic, validation, and API behavior.

---

# 23. API Error Status Codes

| Status Code | Meaning                           |
| ----------- | --------------------------------- |
| 200         | Successful request                |
| 201         | Resource created                  |
| 400         | Bad request / database constraint |
| 401         | Authentication required           |
| 403         | Access denied                     |
| 404         | Resource not found                |
| 422         | Request validation error          |
| 429         | Rate limit exceeded               |
| 500         | Internal server error             |

---

# 24. Swagger Documentation

The API includes enhanced Swagger documentation with:

* Endpoint summaries
* Endpoint descriptions
* Authentication information
* Role-based access information
* Query parameter descriptions
* Request field descriptions
* Request examples
* Response schemas
* HTTP response codes
* Validation information

Swagger URL:

```text
http://127.0.0.1:8000/docs
```

---

# 25. Development Notes

The application follows a layered structure:

```text
Routes
   ↓
Services
   ↓
Database Models
   ↓
SQLite Database
```

Authentication is separated into the `auth` module.

Pydantic schemas are separated from SQLAlchemy database models.

Business validation is handled through service functions where appropriate.

This structure improves maintainability and makes the application easier to extend.

---

# 26. Project Enhancements

The project was enhanced with the following backend capabilities:

### Level 11

* Role-based authorization
* Admin and Doctor roles
* Restricted doctor access
* Protected delete operations

### Level 12

* Appointment module
* Appointment CRUD
* Doctor/patient appointment lists
* Appointment validation
* Overlap prevention

### Level 13

* Database integrity constraints
* Unique email validation
* Foreign key constraints
* Database exception handling

### Level 14

* SQLAlchemy query optimization
* `joinedload`
* Pagination
* Database indexes
* Response-time measurement

### Level 15

* Creation and update timestamps
* Created-by tracking
* Updated-by tracking
* JWT-based audit information

### Level 16

* Global exception handling
* Uniform validation errors
* Database error handling
* Basic rate limiting

### Level 17

* Unit tests
* API tests
* Authentication tests
* Authorization tests
* Business-logic tests
* Automated test coverage

### Level 18

* Enhanced Swagger documentation
* Endpoint descriptions
* Request field descriptions
* Request examples
* Response schemas
* Error response documentation

---

# 27. Conclusion

The **Doctor Patient Management API** provides a structured FastAPI backend for doctor, patient, and appointment management with authentication, authorization, validation, database persistence, performance considerations, audit tracking, reliability features, testing, and API documentation.

The application is designed with maintainability and future extensibility in mind.
