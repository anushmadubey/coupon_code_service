import datetime

class Coupon:
    def __init__(self, code, discount_percentage, expiry_date, 
                    global_total_repeat_count=0, 
                    user_total_repeat_count=0,
                    user_daily_repeat_count=0,
                    user_weekly_repeat_count=0,
                    coupons_left=0):
        self.id = len(coupon_dict) + 1  # Assign a unique ID
        self.code = code
        self.discount_percentage = float(discount_percentage)
        self.expiry_date = expiry_date
        self.global_total_repeat_count = int(global_total_repeat_count)
        self.user_total_repeat_count = int(user_total_repeat_count)
        self.user_daily_repeat_count = int(user_daily_repeat_count)
        self.user_weekly_repeat_count = int(user_weekly_repeat_count)
        self.coupons_left = coupons_left
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'discount_percentage': self.discount_percentage,
            'expiry_date': self.expiry_date,
            'global_total_repeat_count': self.global_total_repeat_count, 
            'user_total_repeat_count': self.user_total_repeat_count, 
            'user_daily_repeat_count': self.user_daily_repeat_count,
            'user_weekly_repeat_count': self.user_weekly_repeat_count,
            'coupons_left': self.coupons_left
        }

class User:
    def __init__(self, name, email_id):
        self.id=len(user_dict) + 1
        self.name=name
        self.email_id=email_id
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email_id' :self.email_id
        }

class CouponTxn:
    def __init__(self,coupon_code, user_id,user_total=0,user_daily=0,user_weekly=0):
        self.coupon_code = coupon_code
        self.user_id = user_id
        self.user_total = int(user_total)
        self.user_weekly = int(user_weekly)
        self.user_daily = int(user_daily)
        self.redemption_date = datetime.datetime.now().strftime('%Y-%m-%d') 

    def to_dict(self):
        return{
            'coupon_code' : self.coupon_code,
            'user_id': self.user_id,
            'user_total': self.user_total,
            'user_weekly': self.user_weekly,
            'user_daily': self.user_daily,
            'redemption_date': self.redemption_date
        }

user_dict = {}
coupon_dict={}
user_coupon_txn = {}

