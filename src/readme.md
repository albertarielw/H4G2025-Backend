python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
curl -X POST -H "Content-Type: application/json" -d '{"user":{"uid":"u0010","name":"Greg","cat":"USER","email":"greg@example.com","password":"secret"}}' http://localhost:5123/users/add