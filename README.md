# CS160-ODFDS-Server
On-Demand Food Delivery Service: server side


# Backend
##API instruction
#### Please request with empty string if a field is empty.

#### All request is passed by JSON

## *Sign up for restaurant*

#### http://127.0.0.1:8000/api/restaurant/ (POST)
##### Request Body:

	{
		"email": "<string>",
		"password": "<string>",
		"phone": <int>,
		"restaurant_name": "<string>",
		"income": int,
		"address": "<string>"
	}

#### Responses:
Status: 200 CREATED

## *Sign up for driver*

#### http://127.0.0.1:8000/api/driver/ (POST)
##### Request Body:

	{
		"email": "<>",
		"password": "",
		"phone": null,
		"ssn": null,
		"date_of_birth": null,
		"first_name": "",
		"last_name": "",
		"income": null,
		"car_plate": "",
		"car_model": "",
		"location": ""
	}

#### Responses:
Status: 200 CREATED

## *Restaurant Login*
#### http://127.0.0.1:8000/api/restaurant/r/login/ (POST)
##### Request Body:
	{
		"email": "<string>"
		"password" : "<string>"
	}
#### Responses:
Status: 200 SUCCESS
