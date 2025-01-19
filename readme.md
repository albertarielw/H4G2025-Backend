# H4G Welfare Home Minimart Backend

## Overview

This backend powers the H4G Welfare Home Minimart system, supporting residents and admins in managing transactions, tasks, inventory, and credits. It includes robust features such as user authentication, transaction management, and a gamified task and credit system.

---

## How to Set Up and Run

### **Database Setup**
1. Install PostgreSQL:
   ```bash
   brew install postgresql
   ```
2. Start the PostgreSQL service:
   ```bash
   brew services start postgresql
   ```
3. Access PostgreSQL:
   ```bash
   psql -U postgres
   ```
4. Create a user and database:
   ```sql
   CREATE USER h4g WITH PASSWORD 'h4g';
   CREATE DATABASE h4g OWNER h4g;
   ```
5. Connect to the database:
   ```bash
   psql -U h4g -d h4g -h localhost
   ```

### **Backend Setup**
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   python main.py
   ```

---

## User Stories

### Residents:
- View available products and make purchases.
- Check transaction history.
- Request specific items.
- Place pre-orders for out-of-stock items.
- Earn credits through task requests to trade for items.
- (Optional) Participate in auctions for items.

### Admins:
- Maintain an audit log of actions.
- Manage users (add, suspend, reset password).
- Oversee credit-earning tasks.
- Approve or reject transactions and item requests.
- Manage inventory (add, update, or remove items).
- Summarize audit logs into reports.

---

## API Documentation

### **Authentication**

#### **Login**
- **Endpoint**: `POST /login`
- **Request**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "jwt": "your.jwt.token",
    "message": "Login successful"
  }
  ```

#### **Reset Password**
- **Endpoint**: `POST /login/resetpassword`
- **Request**:
  ```json
  {
    "email": "user@example.com",
    "password": "newpassword123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Password reset successful"
  }
  ```

---

### **User Management**

#### **Retrieve User Details**
- **Endpoint**: `GET /users/${uid}`
- **Request**: (Empty request body)
  ```json
  {}
  ```
- **Response**:
  ```json
  {
    "user": {
      "uid": "user123",
      "name": "John Doe",
      "email": "johndoe@example.com",
      "credit": 50.0
    },
    "tasks": [],
    "transactions": []
  }
  ```

#### **Add a User**
- **Endpoint**: `POST /users/add`
- **Request**:
  ```json
  {
    "user": {
      "uid": "user123",
      "name": "John Doe",
      "email": "johndoe@example.com",
      "password": "securepassword",
      "cat": "USER",
      "credit": 0
    }
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "User added successfully"
  }
  ```

#### **Update a User**
- **Endpoint**: `PATCH /users/update`
- **Request**:
  ```json
  {
    "user": {
      "uid": "user123",
      "name": "John Smith",
      "email": "johnsmith@example.com",
      "credit": 100.0
    }
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "User updated successfully"
  }
  ```

#### **Suspend a User**
- **Endpoint**: `PATCH /users/suspend`
- **Request**:
  ```json
  {
    "uid": "user123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "User suspended successfully"
  }
  ```

#### **Delete a User**
- **Endpoint**: `DELETE /users/delete`
- **Request**:
  ```json
  {
    "uid": "user123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "User deleted successfully"
  }
  ```

---

### **Inventory Management**

#### **Retrieve All Items**
- **Endpoint**: `GET /items/all`
- **Request**: (Empty request body)
  ```json
  {}
  ```
- **Response**:
  ```json
  {
    "items": [
      {
        "id": "item123",
        "name": "Soap",
        "stock": 10,
        "price": 5
      },
      {
        "id": "item456",
        "name": "Shampoo",
        "stock": 5,
        "price": 15
      }
    ]
  }
  ```

#### **Retrieve Specific Item**
- **Endpoint**: `GET /items/${id}`
- **Request**: (Empty request body)
  ```json
  {}
  ```
- **Response**:
  ```json
  {
    "item": {
      "id": "item123",
      "name": "Soap",
      "stock": 10,
      "price": 5
    }
  }
  ```

#### **Add an Item**
- **Endpoint**: `POST /items/create`
- **Request**:
  ```json
  {
    "item": {
      "name": "Toothpaste",
      "stock": 20,
      "price": 8
    }
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "id": "item789",
    "message": "Item created successfully"
  }
  ```

#### **Update an Item**
- **Endpoint**: `PATCH /items/update`
- **Request**:
  ```json
  {
    "item": {
      "id": "item123",
      "stock": 15,
      "price": 6
    }
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Item updated successfully"
  }
  ```

#### **Delete an Item**
- **Endpoint**: `DELETE /items/delete`
- **Request**:
  ```json
  {
    "id": "item123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Item deleted successfully"
  }
  ```

---

### **Task Management**

#### **Retrieve All Tasks**
- **Endpoint**: `GET /tasks/all`
- **Request**: (Empty request body)
  ```json
  {}
  ```
- **Response**:
  ```json
  {
    "tasks": [
      {
        "id": "task123",
        "name": "Clean the garden",
        "reward": 10,
        "deadline": "2025-01-31T00:00:00Z"
      }
    ]
  }
  ```

#### **Create a Task**
- **Endpoint**: `POST /tasks/create`
- **Request**:
  ```json
  {
    "task": {
      "name": "Organize the library",
      "reward": 20,
      "deadline": "2025-02-01T00:00:00Z",
      "require_review": true,
      "require_proof": false,
      "private": false
    }
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "id": "task456",
    "message": "Task created successfully"
  }
  ```

#### **Update a Task**
- **Endpoint**: `PATCH /tasks/update`
- **Request**:
  ```json
  {
    "task": {
      "id": "task123",
      "reward": 15
    }
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Task updated successfully"
  }
  ```

#### **Delete a Task**
- **Endpoint**: `DELETE /tasks/delete`
- **Request**:
  ```json
  {
    "id": "task123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Task deleted successfully"
  }
  ```

#### **Apply for a Task**
- **Endpoint**: `POST /tasks/apply`
- **Request**:
  ```json
  {
    "id": "task123",
    "uid": "user123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Task application submitted"
  }
  ```

#### **Cancel Task Application**
- **Endpoint**: `POST /tasks/cancel`
- **Request**:
  ```json
  {
    "id": "usertask456"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Task application canceled"
  }
  ```

---

## Data Model

### **1. Users**
Stores information about residents and admins.

| Column       | Type            | Description                                                                 |
|--------------|-----------------|-----------------------------------------------------------------------------|
| `uid`        | `VARCHAR(36)`   | Unique identifier for each user. Primary key.                              |
| `name`       | `VARCHAR(255)`  | Name of the user.                                                          |
| `cat`        | `VARCHAR(50)`   | Category of the user (`USER` or `ADMIN`).                                  |
| `email`      | `VARCHAR(255)`  | Unique email address for each user.                                        |
| `password`   | `VARCHAR(255)`  | Encrypted password for authentication.                                     |
| `credit`     | `DECIMAL(10,2)` | Credits available for the user. Defaults to `0.00`.                        |
| `is_active`  | `BOOLEAN`       | Indicates if the user account is active. Defaults to `TRUE`.               |

### **2. Items**
Stores information about products available in the minimart.

| Column       | Type           | Description                                                                 |
|--------------|----------------|-----------------------------------------------------------------------------|
| `id`         | `VARCHAR(36)`  | Unique identifier for each item. Primary key.                              |
| `name`       | `VARCHAR(255)` | Name of the item.                                                          |
| `image`      | `TEXT`         | Image of the item, stored as a blob or bytea.                              |
| `stock`      | `INT`          | Quantity of the item available in stock. Must be `>= 0`.                   |
| `price`      | `INT`          | Price of the item in credits. Must be `>= 0`.                              |
| `description`| `TEXT`         | Additional description of the item.                                        |

### **3. Tasks**
Defines tasks that residents can perform to earn credits.

| Column              | Type             | Description                                                                 |
|---------------------|------------------|-----------------------------------------------------------------------------|
| `id`                | `VARCHAR(36)`    | Unique identifier for each task. Primary key.                               |
| `name`              | `VARCHAR(255)`   | Name or title of the task.                                                  |
| `created_by`        | `VARCHAR(36)`    | Admin who created the task. Foreign key referencing `users(uid)`.           |
| `reward`            | `DECIMAL(10,2)`  | Credits rewarded for completing the task. Defaults to `0.00`.               |
| `start_time`        | `TIMESTAMP`      | Start time of the task.                                                     |
| `deadline`          | `TIMESTAMP`      | Deadline for completing the task.                                           |
| `is_recurring`      | `BOOLEAN`        | Indicates if the task recurs periodically.                                  |
| `recurrence_interval`| `INT`           | Interval in days for recurring tasks. `NULL` if the task is one-off.        |
| `description`       | `TEXT`           | Detailed description of the task.                                           |

### **4. UserTasks**
Tracks individual user participation in tasks.

| Column         | Type             | Description                                                                 |
|----------------|------------------|-----------------------------------------------------------------------------|
| `id`           | `VARCHAR(36)`    | Unique identifier for the user-task record. Primary key.                    |
| `uid`          | `VARCHAR(36)`    | User participating in the task. Foreign key referencing `users(uid)`.       |
| `task`         | `VARCHAR(36)`    | Task being performed. Foreign key referencing `tasks(id)`.                  |
| `start_time`   | `TIMESTAMP`      | When the user started the task.                                             |
| `end_time`     | `TIMESTAMP`      | When the user completed the task.                                           |
| `status`       | `VARCHAR(50)`    | Current status of the task (`APPLIED`, `ONGOING`, `COMPLETED`, etc.).        |
| `admin_comment`| `TEXT`           | Comments or feedback provided by the admin.                                 |

### **5. Transactions**
Tracks purchases or preorders made by users.

| Column    | Type           | Description                                                                 |
|-----------|----------------|-----------------------------------------------------------------------------|
| `id`      | `VARCHAR(36)`  | Unique identifier for each transaction. Primary key.                       |
| `item`    | `VARCHAR(36)`  | Item being purchased. Foreign key referencing `items(id)`.                 |
| `uid`     | `VARCHAR(36)`  | User making the transaction. Foreign key referencing `users(uid)`.         |
| `quantity`| `INT`          | Number of items being purchased.                                           |
| `status`  | `VARCHAR(50)`  | Current status of the transaction (`PREORDER`, `CONFIRMED`, `CLAIMED`, etc.).|

### **6. ItemRequests**
Records requests made by residents for specific items.

| Column         | Type           | Description                                                                 |
|----------------|----------------|-----------------------------------------------------------------------------|
| `id`           | `VARCHAR(36)`  | Unique identifier for each item request. Primary key.                      |
| `requested_by` | `VARCHAR(36)`  | User making the request. Foreign key referencing `users(uid)`.             |
| `description`  | `TEXT`         | Description of the requested item.                                         |

### **7. Logs**
Stores audit logs for system actions.

| Column        | Type           | Description                                                                 |
|---------------|----------------|-----------------------------------------------------------------------------|
| `id`          | `VARCHAR(36)`  | Unique identifier for each log entry. Primary key.                         |
| `cat`         | `VARCHAR(50)`  | Category of the log (`USER`, `TRANSACTION`, etc.).                         |
| `uid`         | `VARCHAR(36)`  | User associated with the action. Foreign key referencing `users(uid)`.     |
| `timestamp`   | `TIMESTAMP`    | Time the action occurred. Defaults to the current timestamp.               |
| `description` | `TEXT`         | Description of the logged action.                                          |

---

This README consolidates all setup instructions, API details, and database model descriptions for ease of use.

