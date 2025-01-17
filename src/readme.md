python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

Tests:

Admin Test

(1) Login as admin, save admin jwt token as bearer token for any admin test request
Req:
curl --location --request POST 'http://127.0.0.1:5123/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "bob@example.com",
    "password": "bobpass"
}'

Resp:
{
  "message": "Login successful",
  "success": true,
  "token": "..."
}

(2)
Req:
curl --location --request GET 'http://127.0.0.1:5123/items/all' \
--header 'Content-Type: application/json' \
--data-raw '{}'

Resp:
{
  "items": [
    {
      "description": "High-end laptop",
      "id": "i0001",
      "image": "https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg",
      "name": "Laptop",
      "price": 1200,
      "stock": 5
    },
    {
      "description": "Latest smartphone",
      "id": "i0002",
      "image": "https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg",
      "name": "Phone",
      "price": 800,
      "stock": 10
    },
    {
      "description": "4K monitor",
      "id": "i0003",
      "image": "https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg",
      "name": "Monitor",
      "price": 300,
      "stock": 3
    },
    {
      "description": "Noise-cancelling headset",
      "id": "i0004",
      "image": "https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg",
      "name": "Headset",
      "price": 50,
      "stock": 20
    },
    {
      "description": "Mechanical keyboard",
      "id": "i0005",
      "image": "https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg",
      "name": "Keyboard",
      "price": 90,
      "stock": 15
    }
  ]
}

(3)
Req:
curl --location --request GET 'http://127.0.0.1:5123/items/i0001' \
--header 'Content-Type: application/json' \
--data-raw '{}'

Resp:
{
  "item": {
    "description": "High-end laptop",
    "id": "i0001",
    "image": "https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg",
    "name": "Laptop",
    "price": 1200,
    "stock": 5
  }
}

(4)
curl --location --request POST 'http://127.0.0.1:5123/items/create' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczNzA4MTYyMSwianRpIjoiNTU4NjJkMTgtOWViNS00Yjg4LTgwNTItODlkYTMwOTZhMTkzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InUwMDAyIiwibmJmIjoxNzM3MDgxNjIxLCJjc3JmIjoiMmZjZTNlYTAtYWZjMC00MGQ2LWIzYmUtNmQ2OTc2NTc5ZDdjIiwiZXhwIjoxNzM3MTY4MDIxfQ.LQXcNZGwZNZ41u3-Wl8pVl7v8DomziYXis3X0n3bh20' \
--data-raw '{
    "item": {
        "description": "This is a test item.",
        "image": "...",
        "name": "Test Item",
        "price": 1,
        "stock": 1000000
    }
}'

{
  "id": "79dda043baac443383e76a2d9f226a5e",
  "message": "Item created",
  "success": true
}

(5)
curl --location --request PATCH 'http://127.0.0.1:5123/items/79dda043baac443383e76a2d9f226a5e/update' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczNzA4MTYyMSwianRpIjoiNTU4NjJkMTgtOWViNS00Yjg4LTgwNTItODlkYTMwOTZhMTkzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InUwMDAyIiwibmJmIjoxNzM3MDgxNjIxLCJjc3JmIjoiMmZjZTNlYTAtYWZjMC00MGQ2LWIzYmUtNmQ2OTc2NTc5ZDdjIiwiZXhwIjoxNzM3MTY4MDIxfQ.LQXcNZGwZNZ41u3-Wl8pVl7v8DomziYXis3X0n3bh20' \
--data-raw '{
    "item": {
        "name": "Test Item 2"
    }
}'

{
  "message": "Item updated",
  "success": true
}

(6)
curl --location --request DELETE 'http://127.0.0.1:5123/items/79dda043baac443383e76a2d9f226a5e/delete' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczNzA4MTYyMSwianRpIjoiNTU4NjJkMTgtOWViNS00Yjg4LTgwNTItODlkYTMwOTZhMTkzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InUwMDAyIiwibmJmIjoxNzM3MDgxNjIxLCJjc3JmIjoiMmZjZTNlYTAtYWZjMC00MGQ2LWIzYmUtNmQ2OTc2NTc5ZDdjIiwiZXhwIjoxNzM3MTY4MDIxfQ.LQXcNZGwZNZ41u3-Wl8pVl7v8DomziYXis3X0n3bh20' \
--data-raw '{}'

{
  "message": "Item deleted",
  "success": true
}