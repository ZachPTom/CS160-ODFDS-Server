# CS160-ODFDS-Server
On-Demand Food Delivery Service: server side


# Backend
## API instruction
#### Please request with empty string if a field is empty.

#### All request is passed by JSON

# Restaurant

## *Sign up for restaurants*

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

Return: a JSON contains restaurant info (like the dashboard).

## *Restaurant Logout*
#### http://127.0.0.1:8000/api/restaurant/r/logout/ (DELETE)
##### Request Body:
	{
		"key": "<string>"
	}
#### Responses:
Status: 200 SUCCESS

## *Restaurant Dashboard*
#### http://127.0.0.1:8000/api/restaurant/r/dashboard/ (POST)
##### Request Body:
	{
		"key": "<string>"
	}
#### Responses:
Status: 200 SUCCESS

Return: a JSON contains restaurant info

## *Restaurant Post an Order*
#### http://127.0.0.1:8000/api/restaurant/r/post/ (POST)
##### Request Body:
	{
		"lat": "<float>",
		"long" : "<float>",
		"price" : "<float>",
		"key": "<string>"
	}
#### Responses:
Satus: 200 SUCCESS

## *Restaurant Get its Orders*
#### http://127.0.0.1:8000/api/restaurant/r/order/ (POST)
##### Request Body:
	{
		"key": "<string>"
	}
#### Responses:
Satus: 200 SUCCESS

Return: JSON contains a list of orders from the restaurant


## *Restaurant check a route of the order*
#### http://127.0.0.1:8000/api/restaurant/r/route/ (POST)
##### Request Body:
	{
		"key": "<string>"
		"order_id": "<int>"
	}
#### Responses:
Satus: 200 SUCCESS
Return: JSON contains a list of locations

#### Example: 
"second" is an option, checking second exist before using map API
"first" always is delivered at first
	{
		"rest": [lat, lng],
		"driver": [lat, lng],
		"first" : [lat, lng],
		"second": [lat, lng]
	}



# Driver

## *Sign up for driver*

#### http://127.0.0.1:8000/api/driver/ (POST)
##### Request Body:

	{
		"email": "<string>",
		"password": "<string>",
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
		"email": "<string>",
		"password": "<string>"
	}
#### Responses:
Status: 200 SUCCESS

Return: a JSON contains the driver info (like the dashboard)

## *Driver Logout*
#### http://127.0.0.1:8000/api/driver/r/logout/ (DELETE)
##### Request Body:
	{
		"key": "<string>"
	}
#### Responses:
Status: 200 SUCCESS

## *Driver Dashboard*
#### http://127.0.0.1:8000/api/driver/r/dashboard/ (POST)
##### Request Body:
	{
		"key": "<string>"
	}

#### Responses:
Status: 200 SUCCESS

Return: a JSON contains the driver info

## *Driver Get 1st Order List*
#### http://127.0.0.1:8000/api/driver/r/order/ (POST)
##### Request Body:
	{
		"key": "<string>"
	}

#### Responses:
Status: 200 SUCCESS

Return: a JSON contains orders 

## *Driver 1st  order acceptation* 
#### http://127.0.0.1:8000/api/driver/r/first_acceptation/ (POST)
##### Request Body:
	{
		"key": "<string>"
		"order_id": "<int>"
	}
#### Responses:
Status: 200 SUCCESS
Return: a JSON contains second orders

#### Notice: 
It will be no the seond order if the list is empty 
(In the case, do not call Driver 2nd  order acceptation api)
Check it before go to next step

## *Driver 2nd  order acceptation* 
#### http://127.0.0.1:8000/api/driver/r/second_acceptation/ (POST)
##### Request Body:
	{
		"key": "<string>"
		"order_id": "<int>"
	}
#### Responses:
Status: 200 SUCCESS


## *Driver arrives the restaurant*
#### http://127.0.0.1:8000/api/driver/r/confirmation/ (POST)
##### Request Body:
	{
		"key": "<string>"
		"order_id": "<list of order id>" (int)
	}
#### Responses:
Status: 200 SUCCESS

## *Drivers see a route of orders*
#### http://127.0.0.1:8000/api/driver/r/route/ (POST)
##### Request Body:
	{
		"key": "<string>"
		"first_id": "<int>"
		"second_id": "<int> OR null" (must have somthing)
	}
#### Responses:
Satus: 200 SUCCESS

Return: JSON contains a list of locations

#### Example: 
"second" is an option, checking second exist before using map API
"first" always is delivered at first

	{
		"rest": [lat, lng],
		"driver": [lat, lng],
		"first" : [lat, lng],
		"second": [lat, lng]
	}

## *Driver update location*
#### http://127.0.0.1:8000/api/driver/r/update/ (POST)
##### Request Body:
	{
		"key": "<string>"
		"driver_lat":  <float>
		"driver_long":  <float>
	}
#### Responses:
Satus: 200 SUCCESS


## *Orders Delivered*
#### http://127.0.0.1:8000/api/driver/r/delivered/ (POST)
##### Request Body:
	{
		"order_id": "<int>"
		"key": "<string>"
	}
#### Responses:
Status: 200 SUCCESS
