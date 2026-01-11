# Inventory Management System

A robust and efficient Inventory Management System built with Django (Python). This application helps businesses manage their stock, track sales and purchases, maintain supplier and customer records, and visualize performance through an analytical dashboard.

## 🚀 Features

*   **Dashboard Analytics:** Get real-time insights into total sales, product counts, and performance metrics.
*   **🌟 Smart Stock Alerts:** Automatic notifications when stock levels fall below 5 units, ensuring you never run out of inventory.
*   **🌟 Expiry Tracking:** Proactive alerts for products nearing their expiry date to prevent wastage.
*   **🌟 Sales Prediction:** Intelligent forecasting based on last week's sales data to help plan future inventory.
*   **Product Management:** Add, edit, and delete products with image support and detailed categorization.
*   **Sales & Purchase Recording:** Keep a digital ledger of all transactions.
*   **Supplier & Customer Database:** Manage contact details and history.
*   **User Authentication:** Secure login and registration system.

## 🛠 Technologies Used

*   **Backend:** Python 3, Django 5
*   **Frontend:** HTML5, CSS3, Bootstrap 5
*   **Database:** SQLite (default) / PostgreSQL (production ready)
*   **Styling:** Custom CSS for a clean, modern UI

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

1. pip install django
2. django-admin start project projectname
3. django-admin start app appname

4.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

5.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Apply Migrations**
   write tables fields in models.py
    then
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

8.  **Create a Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

9.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

10.  **Access the App**
    Open your browser and go to `http://127.0.0.1:8000/`


## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

