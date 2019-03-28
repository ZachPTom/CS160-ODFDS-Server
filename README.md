# CS160-ODFDS-Server
On-Demand Food Delivery Service: server side


# Backend
##API instruction
#### Please request with empty string if a field is empty.

#### All request is passed by JSON

# Restaurant

## *Sign up for a restaurant*

#### http://127.0.0.1:8000/api/restaurant/ (POST)
##### Request Body:

	{
		"email": "<string>",
		"password": "<string>",
		"restaurant_name": "<string>",
		"rest_lat": "<float>",
        	"rest_long": "<float>"
	}

#### Responses:
Status: 201 CREATED


## *Restaurant Login*
#### http://127.0.0.1:8000/api/restaurant/r/login/ (POST)
##### Request Body:
	{
		"email": "<string>",
		"password" : "<string>"
	}
#### Responses:
Satus: 200 SUCCESS

Return: a JSON contains restaurant info.

## *Restaurant Logout*
#### http://127.0.0.1:8000/api/restaurant/r/logout/ (DELETE)

#### Responses:
Status: 200 SUCCESS

## *Restaurant Dashboard*
#### http://127.0.0.1:8000/api/restaurant/r/dashboard/ (GET)

#### Responses:
Status: 200 SUCCESS

Return: a JSON contains restaurant info

## *Restaurant Post an Order*
#### http://127.0.0.1:8000/api/restaurant/r/post/ (POST)
##### Request Body:
	{
		"lat": "<float>",
		"long" : "<float>",
		"price" : "<float>"
	}
#### Responses:
Satus: 200 SUCCESS

## *Restaurant Get its Orders
#### http://127.0.0.1:8000/api/restaurant/r/order/ (GET)
##### Request Body:
	{
		"lat": "<float>",
		"long" : "<float>",
		"price" : "<float>"
	}
#### Responses:
Satus: 200 SUCCESS

Return: a list of JSON contains orders of the restaurant



# Driver

## *Sign up for driver*

#### http://127.0.0.1:8000/api/driver/ (POST)
##### Request Body:

	{
		"email": "<string>",
		"first_name": "<string>",
		"last_name": "<sting>",
		"driver_lat": "<float>",
		"driver_long": "<float>"
	}

#### Responses:
Status: 201 CREATED

## *Driver Login*
#### http://127.0.0.1:8000/api/driver/r/login/ (POST)
##### Request Body:
	{
		"email": "<string>"
		"password" : "<string>"
	}
#### Responses:
Status: 200 SUCCESS

Return: a JSON contains driver's info

## *Driver Logout*
#### http://127.0.0.1:8000/api/driver/r/logout/ (DELETE)

#### Responses:
Status: 200 SUCCESS

## *Driver Dashboard*
#### http://127.0.0.1:8000/api/driver/r/dashboard/ (GET)

#### Responses:
Status: 200 SUCCESS

Return: a JSON contains driver's info

## *Driver Get 1st Order*
#### http://127.0.0.1:8000/api/driver/r/order/ (GET)

#### Responses:
Status: 200 SUCCESS

Return: a JSON contains a chosen order 

## *Driver's acceptation*
#### http://127.0.0.1:8000/api/driver/r/login/ (POST)
##### Request Body:
	{
		"order_id": "<int>"
	}
#### Responses:
Status: 200 SUCCESS

Return: a JSON contains second order 

Notice: 

It no the seond order if JSON is empty.
         
Call the api again if drivers accept the 2nd order.

In frontend, at most calling the api twice in single delivery (TWO orders policy). 


## *Driver Pick Orders Up*
#### http://127.0.0.1:8000/api/driver/r/confirmation/ (POST)
##### Request Body:
	{
		"order_id": "<list of order id>"

	}
#### Responses:
Status: 200 SUCCESS

Return: a JSON contains at most two address and driver's location at index 0


## *Orders Delivered*
#### http://127.0.0.1:8000/api/driver/r/delivered/ (POST)
##### Request Body:
	{
		"order_id": "<int>"
	}
#### Responses:
Status: 200 SUCCESS
