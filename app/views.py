from flask import Flask, request, jsonify
from app import models  # Import the Coupon model and coupons list
import copy
import datetime


app = Flask(__name__)

def validateCoupon(coupon: models.Coupon) :
    if coupon.code in models.coupon_dict:
        return 'Coupon Code already exists',400
    if coupon.expiry_date < datetime.datetime.today():
        return "Expiry date cannot be less than today",400
    if coupon.discount_percentage < 0:
        return "Discount Percentage cannot be less than 0", 400
        
    return None, 200

@app.route('/coupon', methods=['GET'])
def getCoupon():
    try:
        coupon_data = [coupon.__dict__ for coupon in models.coupon_dict.values()]
        return jsonify(message=coupon_data),200
    except Exception as e:
        return jsonify(message='Uncaught Expection' ,error=e.__cause__, statusCode=500), 500

@app.route('/coupon', methods=['POST'])
def createCoupon():
    try:
        code = request.form['code']
        discount_percentage = float(request.form['discount_percentage'])
        expiry_date = datetime.datetime.strptime(request.form['expiry_date'], "%Y-%m-%d")

        coupon = models.Coupon(code=code, discount_percentage=discount_percentage, expiry_date=expiry_date)
        
        msg, statusCode = validateCoupon(coupon)
        if statusCode != 200:
            return jsonify(message=str(msg)), statusCode
        models.coupon_dict[coupon.code] = coupon
        return jsonify(message="Coupon created successfully"),200
    except Exception as e:
        return jsonify(message='Uncaught Expection' ,error=e.__cause__, statusCode=500), 500

def validateUser(user: models.User): # basic user validation
    for u in models.user_dict.values():
        if u.email_id == user.email_id:
            return jsonify("User with the same email id exists"),400
    return None, 200
    
@app.route('/user', methods=['GET'])
def getUser():
    try:
        user_data = [user.__dict__ for user in models.user_dict.values()]
        return jsonify(message=user_data)
    except Exception as e:
        return jsonify(message='Uncaught Expection' ,error=e.__cause__, statusCode=500), 500


@app.route('/user', methods=['POST'])
def createUser():
    try:
        name = request.form['name']
        email_id = request.form['email_id']

        user = models.User(name=name, email_id=email_id)
        msg,statusCode = validateUser(user=user)
        if statusCode != 200:
            return msg,statusCode

        models.user_dict[user.id] = user
        return jsonify(message="User created successfully"),200
    except Exception as e:
        return jsonify(message='Uncaught Expection' ,error=e.__cause__, statusCode=500), 500


@app.route('/coupon/<coupon_code>/repeat_count', methods=['GET'])
def getCouponRepeatCounts(coupon_code: str):
    try:
        if coupon_code not in models.coupon_dict:
            return jsonify(message="Coupon not found"), 404
        coupon = models.coupon_dict[coupon_code]

        return jsonify(coupon=coupon.code,
                global_total_repeat_count=coupon.global_total_repeat_count,
                user_total_repeat_count=coupon.user_total_repeat_count,
                user_daily_repeat_count=coupon.user_daily_repeat_count,
                user_weekly_repeat_count=coupon.user_weekly_repeat_count),200
    except Exception as e:
        return jsonify(message='Uncaught Expection' ,error=e.__cause_, statusCode=500), 500

@app.route('/coupon/<coupon_code>/repeat_count', methods=['PUT'])
def addCouponRepeatCounts(coupon_code: str):
    try:
        if coupon_code not in models.coupon_dict:
            return jsonify(message="Coupon not found"), 404
        coupon = models.coupon_dict[coupon_code]

        old_coupon_data = copy.deepcopy(coupon)

        if 'global_total_repeat_count' in request.form:
            coupon.global_total_repeat_count = int(request.form['global_total_repeat_count'] )
            coupon.coupons_left = int(request.form['global_total_repeat_count'])

        if 'user_total_repeat_count' in request.form:
            coupon.user_total_repeat_count = int(request.form['user_total_repeat_count'])

        if 'user_daily_repeat_count' in request.form:
            coupon.user_daily_repeat_count = int(request.form['user_daily_repeat_count'])

        if 'user_weekly_repeat_count' in request.form:
            coupon.user_weekly_repeat_count = int(request.form['user_weekly_repeat_count'])

        msg, statusCode=updateRepeatCountsInUserTxn(oldcoupon=old_coupon_data,coupon=coupon)
        if statusCode != 200:
            return msg, statusCode

        return jsonify(message='Coupon repeat counts updated'),200

    except Exception as e:
        print(e.with_traceback())
        return jsonify(message='Uncaught Expection' ,error=e, statusCode=500), 500

@app.route('/coupon/<coupon_code>/status', methods=['GET'])
def verifyCoupon(coupon_code: str):
    try:
        if coupon_code not in models.coupon_dict:
            return jsonify("Coupon not found"), 404
        coupon = models.coupon_dict[coupon_code]
        if coupon.coupons_left < 1:
            return jsonify(message="Coupon exists, but global count is zero."), 403
        if coupon.expiry_date < datetime.datetime.today():
            return jsonify(message="Coupon expired."), 403
        return jsonify(message="Valid coupon"),200
    except Exception as e:
        return jsonify(message='Uncaught Expection' ,error=e,statusCode=500), 500

def verifyUserCounts(coupon_txn: models.CouponTxn):
    try:
        if coupon_txn.user_total < 1:
            return False,jsonify(message='User total redemption count reached.'),400

        if coupon_txn.user_weekly < 1:
            return False,jsonify(message='User weekly redemption count reached.'),400
        
        if coupon_txn.user_daily < 1:
            return False,jsonify(message='User daily redemption count reached.'),400
        return True,None,200

    except Exception as e:
        return False,jsonify(message='Uncaught Expection' ,error=e.__cause__, statusCode=500), 500


@app.route('/coupon/apply', methods=['POST'])
def applyCoupon():
    try:

        user_id = int(request.form['user_id'])
        coupon_code = request.form['coupon_code']
        coupon = None
        msg, statusCode = verifyCoupon(coupon_code)
        if statusCode != 200:
            return jsonify(message=msg),statusCode
        coupon = models.coupon_dict[coupon_code]

        user = models.user_dict[user_id]
        if not user:
            return jsonify(message="User not found"), 404

        user_txn=None
        if user_id in models.user_coupon_txn and coupon_code in models.user_coupon_txn[user_id] :
            user_txn = models.user_coupon_txn[user_id][coupon_code]
        else:
            user_txn= models.CouponTxn(user_id=user_id,
                                    coupon_code=coupon_code,
                                    user_total=coupon.user_total_repeat_count,
                                    user_daily=coupon.user_daily_repeat_count,
                                    user_weekly=coupon.user_weekly_repeat_count)
            models.user_coupon_txn[user_id] = {}
            models.user_coupon_txn[user_id][coupon_code] = user_txn

        isValid,msg,statusCode = verifyUserCounts(coupon_txn=user_txn)
        if not isValid:
            return msg, statusCode
        # reduce all the counts
        user_txn.user_daily -= 1
        user_txn.user_weekly -= 1
        user_txn.user_total -=1 
        coupon.coupons_left -= 1

        return jsonify(message="Successfully coupon applied."),200
    except Exception as e:
        return jsonify(message='Uncaught Expection' ,error=e.__cause__, statusCode=500), 500


def updateRepeatCountsInUserTxn(oldcoupon: models.Coupon, coupon: models.Coupon):
    try:
        if models.user_coupon_txn:
            for user_coupon_map in models.user_coupon_txn.values():
                if coupon.code in user_coupon_map:
                    user_txn = user_coupon_map[coupon.code]
                    diff = coupon.user_total_repeat_count - oldcoupon.user_total_repeat_count
                    user_txn.user_total = user_txn.user_total + diff if user_txn.user_total + diff >= 0 else 0

                    diff = coupon.user_daily_repeat_count - oldcoupon.user_daily_repeat_count
                    user_txn.user_daily = user_txn.user_daily + diff if user_txn.user_daily + diff >= 0 else 0

                    diff = coupon.user_weekly_repeat_count - oldcoupon.user_weekly_repeat_count
                    user_txn.user_weekly = user_txn.user_weekly + diff if user_txn.user_weekly + diff >= 0 else 0

                    diff = coupon.global_total_repeat_count - oldcoupon.global_total_repeat_count
                    coupon.coupons_left = coupon.coupons_left + diff if coupon.coupons_left + diff >= 0 else 0
        return None, 200            
    except Exception as e: 
        return jsonify(message='Uncaught Expection' ,error=e.__cause__, statusCode=500), 500
            

@app.route('/test', methods=['GET'])
def test():
    return jsonify(message="hello!")

