python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py


Test:

(1) /users 

/users/${uid}
curl -X GET -H "Content-Type: application/json" -d '{}' http://localhost:5123/users/u0001

/users/add
curl -X POST -H "Content-Type: application/json" -d '{"user":{"uid":"u0010","name":"Greg","cat":"USER","email":"greg@example.com","password":"secret"}}' http://localhost:5123/users/add

/users/update
curl -X PATCH -H "Content-Type: application/json" -d '{"user":{"uid":"u0010","name":"Greg","cat":"USER","email":"greg@example.com","password":"secret"}}' http://localhost:5123/users/update

/users/suspend
curl -X PATCH -H "Content-Type: application/json" -d '{"uid":"u0010"}' http://localhost:5123/users/suspend

/users/delete
curl -X DELETE -H "Content-Type: application/json" -d '{"uid":"u0010"}' http://localhost:5123/users/delete