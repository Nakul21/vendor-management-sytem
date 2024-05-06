# Vendor Management System

The Vendor Management System is a Django application designed to manage vendors, purchase orders, and performance metrics for vendors.

## Setup Instructions

Follow these instructions to set up and run the Vendor Management System on your local machine.

### Prerequisites

- Python (3.6 or higher)
- Django (3.0 or higher)
- Django REST Framework

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Nakul21/vendor-management-sytem.git

2. Navigate to the project directory::

   ```bash
   cd vendor-management-system

3. Install the required Python packages using pip::

   ```bash
   pip install -r requirements.txt


### Running the Application

1. Make migrations to create the database schema:

   ```bash
   python manage.py makemigrations

2. Apply migrations to create the database schema:

   ```bash
   python manage.py migrate  

3. Start the Django development server:

   ```bash
   python manage.py runserver

4. Access the application in your web browser at http://localhost:8000/.


### ENDPOINTS

### NOTE: - All the endpoints other than vendor_profile/api/generate-token/ will require token for their execution 

- **POST - vendor_profile/api/vendors/:** Create a new vendor.
- **GET - vendor_profile/api/vendors/list:** List all vendors.
- **GET - vendor_profile/api/fetch_vendor_info:** Fetch specific vendor info
- **PUT - vendor_profile/api/vendors/<str:vendor_code>/** Update vendor info
- **DELETE - vendor_profile/api/vendors/delete/<str:vendor_code>/** Delete vendor info
- **GET - vendor_profile/api/vendors/{vendor_id}/:performance:** Retrieve performance metrics for a specific vendor.
- **POST - purchase_order/api/purchase_orders/:** Create a purchase order.
- **GET - purchase_order/api/purchase_orders/?vendor_id:** Get PO's of the passed vendor.
- **GET - purchase_order/api/purchase_orders/<str:po_id>:** Retrieve details of the passed PO number.
- **PUT - purchase_order/api/purchase_orders/<str:po_id>/:** Update a purchase order.
- **DELETE - purchase_order/api/purchase_orders/<str:po_id>/:** Delete a purchase order.
- **POST - purchase_order/api/purchase_orders/<str:po_id>/acknowledge:** Acknowledge a purchase order.

### Generating Authentication Token

- **POST - vendor_profile/api/generate-token/:** Generate an authentication token with expiration time.
