import json
import os
import random
import sys
from datetime import datetime

DB_FILE = "proje.json"

CUSTOMER_REVIEWS = [
    "☕ Harika seçim! Kahveniz sevgiyle hazırlanıyor.",
    "🌟 Bugünün favorisi kesinlikle bu kahve!",
    "🥐 Kahvenizin yanına güzel bir tatlı çok yakışırdı!",
    "🔥 Mels Kafe'de her yudum ayrı bir keyif!",
    "⚡ Enerjiniz tavan yapacak, harika bir tercih!",
    "🎯 Bu aromanın kokusu şimdiden tüm kafeyi sardı!"
]

def initialize_database():
    default_db = {
        "users": {
            "admin": {
                "password": "admin123",
                "role": "admin",
                "first_name": "Sistem",
                "last_name": "Yöneticisi",
                "age": 30,
                "points": 0
            },
            "mels": {
                "password": "123",
                "role": "customer",
                "first_name": "Melis",
                "last_name": "Yılmaz",
                "age": 22,
                "points": 120 
            }
        },
        "menu": {
            "Espresso": {"price": 100, "stock": 10},
            "Americano": {"price": 150, "stock": 8},
            "Latte": {"price": 200, "stock": 5}
        },
        "sizes": {
            "Small": {"name": "Small (Küçük)", "price_diff": 0},
            "Medium": {"name": "Medium (Orta)", "price_diff": 40},
            "Large": {"name": "Large (Büyük)", "price_diff": 80}
        },
        "milks": {
            "1": {"name": "Normal Süt", "price": 0},
            "2": {"name": "Yulaf Sütü", "price": 20},
            "3": {"name": "Badem Sütü", "price": 25}
        },
        "flavors": {
            "1": {"name": "Karamel", "price": 75},
            "2": {"name": "Vanilya", "price": 75},
            "3": {"name": "Çikolata", "price": 75}
        },
        "orders": [],
        "total_revenue": 0.0,
        "coupon_code": "MELS50"
    }
    
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_db, f, indent=4, ensure_ascii=False)

def load_database():
    initialize_database()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_database(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

def register_user(db):
    print("\n--- KAYIT OL ---")
    username = input("Kullanıcı Adı belirleyin: ").strip().lower()
    
    if not username:
        print("❌ Kullanıcı adı boş bırakılamaz!")
        return
    
    if username in db["users"]:
        print("❌ Bu kullanıcı adı zaten alınmış!")
        return
        
    password = input("Şifre belirleyin: ").strip()
    if not password:
        print("❌ Şifre boş bırakılamaz!")
        return
        
    first_name = input("Adınız: ").strip()
    last_name = input("Soyadınız: ").strip()
    
    while True:
        try:
            age = int(input("Yaşınız: "))
            if age <= 0:
                print("Lütfen geçerli bir yaş giriniz.")
                continue
            break
        except ValueError:
            print("Lütfen sadece sayı giriniz!")
            
    db["users"][username] = {
        "password": password,
        "role": "customer",
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "points": 0
    }
    
    save_database(db)
    print(f"🎉 Tebrikler {first_name}, başarıyla kayıt oldun! Giriş yapabilirsin.")

def login(db):
    print("\n--- GİRİŞ YAP ---")
    username = input("Kullanıcı Adı: ").strip().lower()
    password = input("Şifre: ").strip()
    
    if username in db["users"] and db["users"][username]["password"] == password:
        print(f"\n✅ Giriş Başarılı! Hoş geldin, {db['users'][username]['first_name']}.")
        return username
    else:
        print("❌ Hatalı kullanıcı adı veya şifre!")
        return None

def generate_text_receipt(customer_name, username, product_name, base_price, extra_price, discount, coupon, happy_hour_disc, final_price, note):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    file_name = f"mels_kafe_fis_{timestamp}.txt"
    
    receipt_content = f"""
=========================================
            MELS KAFE FATURASI          
=========================================
Tarih/Saat  : {now.strftime("%Y-%m-%d %H:%M:%S")}
Müşteri Adı : {customer_name} ({username})
-----------------------------------------
Satın Alınan Ürün:
-> {product_name}

Sipariş Notu: {note if note else 'Yok'}
-----------------------------------------
Ara Toplam       : {base_price + extra_price:.2f} TL
- Genç İndirimi  : {discount:.2f} TL
- Kupon İndirimi : {coupon:.2f} TL
- Happy Hour (%10): {happy_hour_disc:.2f} TL
-----------------------------------------
TOPLAM ÖDENEN    : {final_price:.2f} TL
=========================================
⭐ Bizi tercih ettiğiniz için teşekkürler!
⭐ Kazandığınız puanlar Mels Kart'a yüklendi.
=========================================
"""
    try:
        with open(file_name, "w", encoding="utf-8-sig") as f:
            f.write(receipt_content)
        
        abs_path = os.path.abspath(file_name)
        print(f"\n💾 Fiziksel Fişiniz başarıyla oluşturuldu!")
        print(f"📍 Dosya Konumu: {abs_path}")
        
        try:
            if sys.platform.startswith('win'):
                os.startfile(file_name)
            elif sys.platform.startswith('darwin'):
                import subprocess
                subprocess.call(('open', file_name))
            else:
                import subprocess
                subprocess.call(('xdg-open', file_name))
        except:
            pass
            
    except Exception as e:
        print(f"⚠️ Fiş dosyası yazılırken bir hata oluştu: {e}")

def check_happy_hour():
    current_hour = datetime.now().hour
    if 14 <= current_hour < 16:
        return True
    return False

def order_coffee(db, username):
    user = db["users"][username]
    
    print("\n--- KAHVE MENÜSÜ ---")
    menu_items = list(db["menu"].keys())
    
    for idx, item in enumerate(menu_items, 1):
        price = db["menu"][item]["price"]
        stock = db["menu"][item]["stock"]
        stock_status = f"{stock} Adet Kaldı" if stock > 0 else "❌ TÜKENDİ!"
        print(f"{idx} - {item:<12} --> {price} ₺ ({stock_status})")
        
    choice = input("Seçiminiz (1-3): ").strip()
    if choice not in ["1", "2", "3"]:
        print("❌ Geçersiz menü seçimi!")
        return
        
    coffee_name = menu_items[int(choice) - 1]
    coffee_data = db["menu"][coffee_name]
    
    if coffee_data["stock"] <= 0:
        print(f"\n😔 Üzgünüz, {coffee_name} tükendi! Lütfen başka bir kahve seçiniz.")
        return
        
    base_price = coffee_data["price"]
    extra_price = 0.0 
    
    print("\n--- BOY SEÇİMİ ---")
    size_keys = list(db["sizes"].keys())
    for idx, key in enumerate(size_keys, 1):
        size_info = db["sizes"][key]
        diff = f"+{size_info['price_diff']} ₺" if size_info['price_diff'] > 0 else "Ücretsiz"
        print(f"{idx} - {size_info['name']:<15} ({diff})")
        
    size_choice = input("Boy seçimi yapınız (1-3): ").strip()
    if size_choice not in ["1", "2", "3"]:
        print("❌ Geçersiz seçim! Standart (Small) boy seçildi.")
        size_key = "Small"
    else:
        size_key = size_keys[int(size_choice) - 1]
        
    size_price = db["sizes"][size_key]["price_diff"]
    size_name = db["sizes"][size_key]["name"]
    extra_price += size_price
    
    print("\n--- SÜT SEÇENEĞİ ---")
    for key, milk_info in db["milks"].items():
        price_diff = f"+{milk_info['price']} ₺" if milk_info['price'] > 0 else "Ücretsiz"
        print(f"{key} - {milk_info['name']:<12} ({price_diff})")
        
    milk_choice = input("Süt tercihinizi giriniz (1-3): ").strip()
    if milk_choice not in db["milks"]:
        print("Normal süt tercih edildi.")
        milk_key = "1"
    else:
        milk_key = milk_choice
        
    milk_name = db["milks"][milk_key]["name"]
    extra_price += db["milks"][milk_key]["price"]
    
    flavor_name = ""
    if coffee_name == "Latte":
        print("\n--- AROMA SEÇİMİ ---")
        for key, value in db["flavors"].items():
            print(f"{key} - {value['name']:<10} (+{value['price']} ₺)")
        print("4 - Aroma İstemiyorum (Sade)")
        
        flavor_choice = input("Aroma seçimi yapınız (1-4): ").strip()
        if flavor_choice in db["flavors"]:
            flavor_data = db["flavors"][flavor_choice]
            extra_price += flavor_data["price"]
            flavor_name = flavor_data["name"] + " Aromalı"
            
    print("\n--- SİPARİŞ NOTU (İsteğe Bağlı) ---")
    order_note = input("Baristaya iletmek istediğiniz özel bir not var mı? (Boş geçmek için Enter): ").strip()
    
    milk_prefix = f"({milk_name})" if milk_key != "1" else ""
    flavor_prefix = f"{flavor_name}" if flavor_name else "Sade"
    
    if coffee_name == "Latte":
        full_product_name = f"{size_key} {milk_prefix} {flavor_prefix} {coffee_name}"
    else:
        full_product_name = f"{size_key} {milk_prefix} {coffee_name}"
    
    use_points = False
    if user["points"] >= 100:
        print(f"\n⭐ Tebrikler! {user['points']} Mels Puanınız var!")
        use_point_choice = input("100 Puan kullanarak bu kahveyi BEDAVA almak ister misiniz? (1-Evet / 2-Hayır): ").strip()
        if use_point_choice == "1":
            use_points = True
            
    final_price = base_price + extra_price
    points_earned = 20 
    
    youth_discount = 0.0
    coupon_discount = 0.0
    happy_hour_discount = 0.0
    
    if use_points:
        final_price = 0.0
        points_earned = 0
        user["points"] -= 100
        print("🎁 100 Puanınız kullanıldı! Kahveniz tamamen Ücretsiz!")
    else:
        if check_happy_hour():
            happy_hour_discount = final_price * 0.10
            final_price -= happy_hour_discount
            print(f"⏰ MUTLU SAATLER! 14:00-16:00 arası %10 Happy Hour indirimi uygulandı: -{round(happy_hour_discount, 2)} ₺")
            
        if user["age"] < 25:
            youth_discount = final_price * 0.10
            final_price -= youth_discount
            print(f"-> Genç İndirimi (%10) uygulandı! Kazanılan indirim: -{round(youth_discount, 2)} ₺")
            
        coupon_choice = input("\nKupon kodu kullanmak istiyor musunuz? (1-Evet / 2-Hayır): ").strip()
        if coupon_choice == "1":
            entered_code = input("Kupon kodunu giriniz: ").strip()
            if entered_code.upper() == db["coupon_code"]:
                coupon_discount = 50.0
                final_price -= coupon_discount
                if final_price < 0:
                    final_price = 0.0
                print(f"-> Başarılı! {db['coupon_code']} kodu ile 50 ₺ indirim yapıldı.")
            else:
                print("❌ Geçersiz kupon kodu!")
                
    final_price = round(final_price, 2)
    print(f"\n📝 Siparişiniz: {full_product_name}")
    if order_note:
        print(f"✍️ Sipariş Notunuz: \"{order_note}\"")
    print(f"💰 Ödenecek Tutar: {final_price} ₺")
    
    confirm = input("Siparişi onaylıyor musunuz? (1-Evet / 2-Hayır): ").strip()
    if confirm != "1":
        print("❌ Sipariş iptal edildi.")
        return
        
    db["menu"][coffee_name]["stock"] -= 1
    if not use_points:
        user["points"] += points_earned
        print(f"⭐ Bu siparişten {points_earned} puan kazandınız! Güncel Puanınız: {user['points']}")
        
    new_order = {
        "username": username,
        "customer_name": f"{user['first_name']} {user['last_name']}",
        "product": full_product_name,
        "base_coffee": coffee_name, 
        "price": final_price,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    db["orders"].append(new_order)
    db["total_revenue"] += final_price
    
    save_database(db)
    
    generate_text_receipt(
        customer_name=f"{user['first_name']} {user['last_name']}",
        username=username,
        product_name=full_product_name,
        base_price=base_price,
        extra_price=extra_price,
        discount=youth_discount,
        coupon=coupon_discount,
        happy_hour_disc=happy_hour_discount,
        final_price=final_price,
        note=order_note
    )
    
    print("\n" + "-"*40)
    print(random.choice(CUSTOMER_REVIEWS))
    print("-"*40)

def show_customer_orders(db, username):
    print("\n--- SİPARİŞ GEÇMİŞİNİZ ---")
    user_orders = [o for o in db["orders"] if o["username"] == username]
    
    if not user_orders:
        print("Henüz bir siparişiniz bulunmamaktadır. İlk siparişinizi vermeye ne dersiniz? 😊")
    else:
        for idx, order in enumerate(user_orders, 1):
            print(f"{idx}. {order['date']} | {order['product']} -> {order['price']} ₺")
        print(f"⭐ Toplam birikmiş kart puanınız: {db['users'][username]['points']} Puan")

def display_sales_chart(db):
    print("\n--- 📈 POPÜLER KAHVELER SATIŞ ANALİZİ ---")
    
    sales_counts = {"Espresso": 0, "Americano": 0, "Latte": 0}
    for order in db["orders"]:
        coffee_type = order.get("base_coffee")
        if coffee_type in sales_counts:
            sales_counts[coffee_type] += 1
            
    max_label_length = max(len(k) for k in sales_counts.keys())
    for coffee, count in sales_counts.items():
        bar = "█" * count
        print(f"{coffee:<{max_label_length}} | {bar:<15} ({count} Adet)")
    print("-" * 40)

def admin_panel(db):
    while True:
        print("\n" + "═"*40)
        print("          🛡️ YÖNETİCİ ADMİN PANELİ 🛡️          ")
        print("═"*40)
        print("1 - Toplam Kazancı Görüntüle")
        print("2 - Tüm Siparişleri Görüntüle")
        print("3 - Kahve Satış İstatistikleri (Grafik)")
        print("4 - Kayıtlı Kullanıcıları Listele (Puanlar)")
        print("5 - Stok Durumu & Güncelleme")
        print("6 - Ana Menüye Dön")
        print("═"*40)
        
        choice = input("Yapmak istediğiniz işlemi seçin (1-6): ").strip()
        
        if choice == "1":
            print(f"\n💵 TOPLAM ELDE EDİLEN KAZANÇ: {round(db['total_revenue'], 2)} ₺")
            
        elif choice == "2":
            print("\n--- TÜM SİPARİŞLERİN LİSTESİ ---")
            if not db["orders"]:
                print("Sistemde henüz kayıtlı sipariş bulunmuyor.")
            else:
                for idx, o in enumerate(db["orders"], 1):
                    print(f"[{idx}] {o['date']} | Müşteri: {o['customer_name']} ({o['username']}) | Ürün: {o['product']} | Tutar: {o['price']} ₺")
                    
        elif choice == "3":
            display_sales_chart(db) 
            
        elif choice == "4":
            print("\n--- KAYITLI KULLANICILAR VE KART PUANLARI ---")
            for username, info in db["users"].items():
                if info["role"] == "admin":
                    continue
                print(f"👤 {info['first_name']} {info['last_name']} ({username}) -> Yaş: {info['age']} | Mels Kart Puanı: {info['points']} ⭐")
                
        elif choice == "5":
            print("\n--- KAHVE STOK DURUMU ---")
            for item, info in db["menu"].items():
                print(f"📦 {item:<12} -> Mevcut Stok: {info['stock']} Adet")
                
            update_choice = input("\nStok güncellemek ister misiniz? (1-Evet / 2-Hayır): ").strip()
            if update_choice == "1":
                coffee_to_update = input("Stok eklemek istediğiniz kahve adı (Espresso, Americano, Latte): ").strip().capitalize()
                if coffee_to_update in db["menu"]:
                    try:
                        amount = int(input(f"Kaç adet {coffee_to_update} stoğu eklenecek?: "))
                        if amount < 0:
                            print("❌ Negatif stok girilemez!")
                            continue
                        db["menu"][coffee_to_update]["stock"] += amount
                        save_database(db)
                        print(f"✅ {coffee_to_update} stoğu başarıyla güncellendi! Yeni stok: {db['menu'][coffee_to_update]['stock']}")
                    except ValueError:
                        print("❌ Lütfen geçerli bir tamsayı giriniz!")
                else:
                    print("❌ Menüde böyle bir kahve bulunamadı!")
                    
        elif choice == "6":
            print("Admin panelinden çıkılıyor...")
            break
        else:
            print("❌ Geçersiz seçim!")

def main():
    while True:
        db = load_database()
        
        print("\n" + "═"*45)
        print("         M E L S   K A F E Y E   H O Ş G E L D İ N İ Z         ")
        print("═"*45)
        print("1 - Giriş Yap (Müşteri & Yetkili)")
        print("2 - Yeni Müşteri Kaydı Oluştur")
        print("3 - Programı Kapat")
        print("═"*45)
        
        main_choice = input("Lütfen bir seçim yapınız (1-3): ").strip()
        
        if main_choice == "1":
            username = login(db)
            if username:
                user_role = db["users"][username]["role"]
                
                if user_role == "admin":
                    admin_panel(db)
                else:
                    while True:
                        db = load_database()
                        print("\n" + "═"*35)
                        print(f"        ☕ MÜŞTERİ MENÜSÜ ({db['users'][username]['first_name'].upper()})        ")
                        print("═"*35)
                        print("1 - Kahve Siparişi Ver")
                        print("2 - Sipariş Geçmişimi Görüntüle")
                        print("3 - Mels Kart Puanlarımı Sorgula")
                        print("4 - Oturumu Kapat (Ana Menü)")
                        print("═"*35)
                        
                        cust_choice = input("Seçiminiz: ").strip()
                        
                        if cust_choice == "1":
                            order_coffee(db, username)
                        elif cust_choice == "2":
                            show_customer_orders(db, username)
                        elif cust_choice == "3":
                            print(f"\n⭐ Güncel Mels Kart Puanınız: {db['users'][username]['points']} Puan.")
                            print("💡 Unutmayın, 100 puan ile sonraki kahveniz tamamen ücretsiz!")
                        elif cust_choice == "4":
                            print("Oturum kapatıldı. Ana menüye yönlendiriliyorsunuz...")
                            break
                        else:
                            print("❌ Hatalı işlem seçimi!")
                            
        elif main_choice == "2":
            register_user(db)
        elif main_choice == "3":
            print("\nMels Kafe'yi tercih ettiğiniz için teşekkürler! İyi günler dileriz! 👋☕")
            break
        else:
            print("❌ Geçersiz seçim! Lütfen ana menüden 1, 2 veya 3'ü tuşlayınız.")

if __name__ == "__main__":
    main()