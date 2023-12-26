# Coupon Code Service
A service to mitigate fraud using "repeat counts" - the number of times a coupon can be used.

This service is built using Python with Flask as its framework. It uses an in-memory data storage for this project. 
The system enables users to create, manage, and redeem coupons with various features, including expiry dates and usage limits.

## Set up info:
### Prerequisites:
Python 3.6 or later
Flask library

### Installation Steps:
Clone the repository: git clone https://github.com/your-username/coupon-management-system.git
Navigate to the project directory: cd coupon-management-system
Install dependencies: pip install -r requirements.txt

### Project Structure:
views.py: Contains API endpoint definitions and logic.
models.py: Defines data models for coupons, users, and transactions.
init.py: Initializes the Flask application.


### Running the Application:
Execute the following command: python run.py
The application will be accessible at http://127.0.0.1:5001/ by default.

## API Usage and Endpoints
Refer to the [Postman Collection](https://github.com/anushmadubey/coupon_code_service/blob/main/docs/Coupon%20Code%20Service.postman_collection.json)


## Unit testing
to run the unit test cases, run the command: 
`pytest test_app.py`


### Assumptions made:
- The repeat counts can be updated anytime
- A daily background job will be configured to update the daily count and weekly count.






