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

(2) /items

/items/all
curl -X GET -H "Content-Type: application/json" -d '{}' http://localhost:5123/items/all

/items/${id}
curl -X GET -H "Content-Type: application/json" -d '{}' http://localhost:5123/items/i0001

/items/create
curl -X POST -H "Content-Type: application/json" -d '{"item":{"description":"This is an item.","id":"i0010","image":"https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664_IvFsQeHjBzfE6sD4VHdO8u5OHUSc6yHF.jpg","name":"Sword","price":1200,"stock": 5}}' http://localhost:5123/items/create

/items/update
curl -X PATCH -H "Content-Type: application/json" -d '{"item":{"description":"This is an item.","id":"i0010","image":"https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664_IvFsQeHjBzfE6sD4VHdO8u5OHUSc6yHF.jpg","name":"Sword2","price":1200,"stock": 5}}' http://localhost:5123/items/update

/items/delete
curl -X DELETE -H "Content-Type: application/json" -d '{"id":"i0010"}' http://localhost:5123/items/delete

/items/buy
curl -X POST -H "Content-Type: application/json" -d '{"id":"i0004","uid":"u0002","quantity":1}' http://localhost:5123/items/buy

/items/preorder
curl -X POST -H "Content-Type: application/json" -d '{"id":"i0004","uid":"u0002","quantity":1}' http://localhost:5123/items/preorder