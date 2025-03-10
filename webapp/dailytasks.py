# import pytz
# from datetime import datetime, time
# from apscheduler.schedulers.background import BackgroundScheduler

# # Define the timezone for Jakarta (GMT+7)
# jakarta_tz = pytz.timezone('Asia/Jakarta')

# # Define schedule with opening and closing times
# schedule = [
#     {"date": "2024-09-27", "open": time(8, 0), "close": time(11, 0)},
#     {"date": "2024-09-28", "open": time(8, 0), "close": time(17, 0)},
#     {"date": "2024-09-29", "open": time(7, 30), "close": time(17, 0)},
#     {"date": "2024-09-30", "open": time(13, 30), "close": time(17, 0)},
#     {"date": "2024-10-01", "open": time(13, 30), "close": time(17, 0)},
#     {"date": "2024-10-02", "open": time(13, 30), "close": time(17, 0)},
#     {"date": "2024-10-03", "open": time(13, 30), "close": time(17, 0)},
#     {"date": "2024-10-04", "open": time(13, 30), "close": time(17, 0)},
#     {"date": "2024-10-05", "open": time(15, 0), "close": time(18, 0)}
# ]

# # Updated function to accept app context
# def reset_balances_and_store(app):
#     with app.app_context():
#         mongo_ccpay = app.extensions['mongo_ccpay']
        
#         # Reset balance and spending for all students
#         print("Resetting balances and spending for all students...")
#         result = mongo_ccpay.db.users.update_many(
#             {"type": "STUDENT"},
#             {"$set": {"balance": 0, "spending": 0}}
#         )
#         print(f"{result.modified_count} student accounts updated (balance and spending reset).")
        
#         # Store the balance of all merchants
#         print("Storing balance for all merchants...")
#         merchants = mongo_ccpay.db.users.find({"type": "MERCHANT"})
#         count = 0
#         for merchant in merchants:
#             mongo_ccpay.db.merchant_balance_history.insert_one({
#                 "merchant_id": merchant['_id'],
#                 "merchant_name": merchant['name'],
#                 "balance": merchant['balance'],
#                 "date": datetime.now(pytz.timezone('Asia/Jakarta'))
#             })
#             count += 1
#             print(f"Stored balance for merchant: {merchant['name']} with balance: {merchant['balance']}")

#         print(f"Balance stored for {count} merchants.")
#         print("Balances reset for students and stored for merchants.")

# # Updated scheduling function to pass app context
# def schedule_daily_tasks(app):
#     scheduler = BackgroundScheduler(timezone='Asia/Jakarta')

#     # Loop through the schedule and add a job for each closing time
#     for entry in schedule:
#         date = datetime.strptime(entry["date"], "%Y-%m-%d")
#         close_time = datetime.combine(date, entry["close"])

#         # Print for debugging purposes
#         print(f"Scheduling task for closing time: {close_time}")

#         # Add a job to reset and store balances at closing time, passing app instance
#         scheduler.add_job(reset_balances_and_store, trigger='date', run_date=close_time, args=[app])

#     scheduler.start()
#     print("Scheduler started with all tasks added.")
