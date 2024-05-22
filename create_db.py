import sqlite3

# افتح اتصالًا بقاعدة البيانات أو قم بإنشائها إذا لم تكن موجودة
conn = sqlite3.connect('real_estate.db')
cursor = conn.cursor()

# إنشاء جدول العقارات
cursor.execute('''CREATE TABLE IF NOT EXISTS real_estate (
                reference TEXT,
                type TEXT,
                status TEXT,
                location TEXT,
                price TEXT,
                area TEXT,
                bedrooms TEXT,
                bathrooms TEXT,
                description TEXT,
                interior_design TEXT,
                floor TEXT,
                license TEXT,
                amenities TEXT,
                payment_flexibility TEXT,
                facilities TEXT,
                rating TEXT,
                finishing TEXT,
                view TEXT,
                direction TEXT,
                expected_delivery_date TEXT,
                age TEXT,
                maintenance TEXT,
                images TEXT,
                current_owner TEXT,
                views TEXT,
                security TEXT,
                nearby_services TEXT,
                transaction_status TEXT,
                contact_phone TEXT,
                notes TEXT
                )''')

# ارفع الاقفال عن قاعدة البيانات بعد انتهاء العمليات
conn.commit()
conn.close()
