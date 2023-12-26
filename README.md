# Coupon Code Service
A service to mitigate fraud using "repeat counts" - the number of times a coupon can be used.

This service is built using Python with Flask as its framework. It uses an in-memory data storage for this project. 
The system enables users to create, manage, and redeem coupons with various features, including expiry dates and usage limits.

## Set up info:
### Prerequisites:
Python 3.6 or later
Flask library

### Installation Steps:
Clone the repository: git clone [https://github.com/your-username/coupon-management-system.git](https://github.com/anushmadubey/coupon_code_service.git)
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

This covers a basic happy flow of the system: 
create coupon -> create user -> update counts -> apply coupon

In addition to that, it covers basic invalid user/coupon cases and counts.

### Assumptions:
- The repeat counts can be updated anytime (checks have been put into place to identify negative counts)
- A daily background job will be configured to update the daily count and weekly count.

Assumptions made on the counts:
- global_total_repeat_count (int): The total number of times the coupon can be used by all users.
- user_total_repeat_count (int): The maximum number of times the coupon can be used by a single user.
- user_daily_repeat_count (int): The maximum number of times the coupon can be used by a single user in a day.
- user_weekly_repeat_count (int): The maximum number of times the coupon can be used by a single user in a week.


## Future Scope
- cover more negative test cases that handle invalid coupon/user, application of invalid coupon, verifying invalid coupon etc.
    - Also adding more scale to it
- Linking it to a low-latency db such as Redis to store the repeat count config.
- Also using the above mentioned db to store transaction logs upto a week, and querying that instead of maintaining a single row per user per coupon count as it does now.
- Adding roles to user, to distinguish between admin and user. 





