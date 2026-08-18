import pandas as pd
import datetime
import os

class DoctorHamrah:
    def __init__(self, filename='health_data.csv'):
        self.filename = filename
        self.columns = ['Date', 'Time', 'Blood_Sugar', 'Stress_Level', 'Note']
        self._prepare_file()

    def _prepare_file(self):
        """ایجاد فایل ذخیره‌سازی اگر وجود نداشته باشد"""
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.filename, index=False)
            print(f"✅ فایل جدید {self.filename} ایجاد شد.")

    def add_record(self, blood_sugar, stress_level, note=""):
        """ثبت اطلاعات جدید"""
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        new_data = {
            'Date': [date_str],
            'Time': [time_str],
            'Blood_Sugar': [blood_sugar],
            'Stress_Level': [stress_level],
            'Note': [note]
        }
        
        df_new = pd.DataFrame(new_data)
        df_new.to_csv(self.filename, mode='a', header=False, index=False)
        print("✅ اطلاعات با موفقیت ذخیره شد.")

    def show_report(self):
        """نمایش گزارش وضعیت"""
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            if df.empty:
                print("⚠️ هنوز داده‌ای ثبت نشده است.")
            else:
                print("\n--- گزارش وضعیت سلامتی ---")
                print(df)
                print("--------------------------\n")
        else:
            print("❌ فایل داده‌ای یافت نشد.")

def main():
    app = DoctorHamrah()
    
    while True:
        print("--- برنامه دکتر همراه ---")
        print("1. ثبت قند خون و سطح استرس")
        print("2. مشاهده گزارش‌ها")
        print("3. خروج")
        
        choice = input("یک گزینه انتخاب کن (1/2/3): ")
        
        if choice == '1':
            try:
                bs = float(input("مقدار قند خون را وارد کن (mg/dL): "))
                stress = int(input("سطح استرس (1 تا 10): "))
                note = input("یادداشت (اختیاری): ")
                app.add_record(bs, stress, note)
            except ValueError:
                print("❌ خطا: لطفا فقط عدد وارد کن.")
        
        elif choice == '2':
            app.show_report()
            
        elif choice == '3':
            print("👋 خداحافظ!")
            break
        else:
            print("❌ گزینه نامعتبر است.")

if __name__ == "__main__":
    main()

