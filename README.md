###  `README.md`

# Customer Order Management API

A Django REST API to manage customer orders, track status changes, and log events. Built with Django and Django REST Framework using SQLite as the database.

---

## Features

- Create, retrieve, update, and delete customer orders
- Status transitions with validation (CREATED → PICKED → DELIVERED)
- Search/filter orders by status and customer name
- Track order status changes using `OrderTrackingEvent`
- Pagination support on list endpoints
- Clean, modular, and testable code using class-based views

---

## Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite (local database)

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/customer-order-api.git
cd customer-order-api
````

### 2. Create a virtual environment

```bash
python -m venv venv
# Activate it:
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` doesn't exist yet:

```bash
pip install django djangorestframework
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/api/orders/` to test the API.

---

## API Overview

### Create a New Order

**POST** `/api/orders/`

```json
{
  "tracking_number": "ABC123456",
  "status": "CREATED",
  "customer": {
    "name": "John Doe",
    "phone_number": "01012345678"
  }
}
```

### List All Orders

**GET** `/api/orders/`
Supports optional filters:

* `?search=CREATED`
* `?search=John`

### Retrieve Single Order

**GET** `/api/orders/<id>/`

### Update Order Status

**PUT** `/api/orders/<id>/`

```json
{
  "tracking_number": "ABC123456",
  "status": "PICKED",
  "customer": {
    "name": "John Doe",
    "phone_number": "01012345678"
  }
}
```

>  Invalid status transitions (e.g., CREATED → DELIVERED) will return an error.

### Delete an Order

**DELETE** `/api/orders/<id>/`

---

## Example cURL Requests

**Create Order**

```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{"tracking_number": "ORD0001", "status": "CREATED", "customer": {"name": "Ali Hassan", "phone_number": "01012345678"}}'
```

**Update Order**

```bash
curl -X PUT http://127.0.0.1:8000/api/orders/1/ \
  -H "Content-Type: application/json" \
  -d '{"tracking_number": "ORD0001", "status": "PICKED", "customer": {"name": "Ali Hassan", "phone_number": "01012345678"}}'
```

**Search by Status**

```bash
curl "http://127.0.0.1:8000/api/orders/?search=DELIVERED"
```

---

## Assumptions

* Customer is created or fetched during order creation.
* Only valid status transitions are allowed:

  * CREATED → PICKED
  * PICKED → DELIVERED
* Tracking numbers must be unique across all orders.
* OrderTrackingEvent is automatically created for every valid status change.
* Pagination is applied with 10 results per page.

---

## Optional Enhancements (Implemented)

*  Tracking status history using `OrderTrackingEvent`
*  Search by customer name and status
*  Pagination support

---

## Project Structure

```
orders_api/
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── orders_api/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── README.md
```
