import os
import hashlib
import json
from datetime import datetime, timedelta

class JEMailSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.emails_file = "emails.json"
        self.lock_file = "system_lock.json"
        self.guests_file = "guests.json"  # Новый файл для гостей
        self.current_user = None
        self.is_guest = False  # Флаг для гостя
        self.system_locked = False
        self.admin_email = "crocorembo@gmail.com"
        self.admin_password = "1122334455667788"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
        
        if os.path.exists(self.emails_file):
            with open(self.emails_file, 'r') as f:
                self.emails = json.load(f)
        else:
            self.emails = []
        
        if os.path.exists(self.lock_file):
            with open(self.lock_file, 'r') as f:
                lock_data = json.load(f)
                self.system_locked = lock_data.get('locked', False)
        else:
            self.system_locked = False
        
        # Загружаем данные о гостях
        if os.path.exists(self.guests_file):
            with open(self.guests_file, 'r') as f:
                self.guests = json.load(f)
        else:
            self.guests = {}
    
    def save_data(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
        with open(self.emails_file, 'w') as f:
            json.dump(self.emails, f)
        with open(self.lock_file, 'w') as f:
            json.dump({'locked': self.system_locked}, f)
        # Сохраняем данные гостей
        with open(self.guests_file, 'w') as f:
            json.dump(self.guests, f)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def is_admin(self):
        if not self.current_user or self.is_guest:
            return False
        user_data = self.users.get(self.current_user, {})
        return user_data.get('email') == self.admin_email
    
    def verify_admin_password(self, password):
        return password == self.admin_password
    
    def validate_password(self, password):
        if len(password) < 9:
            return False, "❌ Пароль должен быть не менее 9 символов"
        
        forbidden_sequences = ['123', '234', '345', '456', '567', '678', '789', '000', '111', '222']
        for seq in forbidden_sequences:
            if seq in password:
                return False, f"❌ Запрещенная последовательность '{seq}' в пароле"
        
        forbidden_chars = ['!', '#', '.', '?']
        for char in forbidden_chars:
            if char in password:
                return False, f"❌ Запрещенный символ '{char}' в пароле"
        
        return True, "✅ Пароль соответствует требованиям"
    
    def create_guest_account(self):
        """Создает временный аккаунт гостя"""
        guest_id = f"guest_{len(self.guests) + 1}"
        guest_data = {
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'expires_at': (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
            'messages_sent': 0,
            'messages_received': 0
        }
        
        self.guests[guest_id] = guest_data
        self.save_data()
        
        return guest_id
    
    def check_guest_expired(self, guest_id):
        """Проверяет, истек ли срок действия гостевого аккаунта"""
        if guest_id not in self.guests:
            return True
        
        guest_data = self.guests[guest_id]
        expires_at = datetime.strptime(guest_data['expires_at'], "%Y-%m-%d %H:%M:%S")
        
        if datetime.now() > expires_at:
            # Удаляем просроченный гостевой аккаунт
            del self.guests[guest_id]
            self.save_data()
            return True
        
        return False
    
    def enter_as_guest(self):
        """Вход как гость"""
        if self.system_locked:
            print("❌ Система заблокирована!")
            return False
        
        print("\n" + "="*50)
        print("👤 ВХОД КАК ГОСТЬ")
        print("="*50)
        print("⚠️  Внимание: Гостевой аккаунт действует 3 дня!")
        print("   После этого он будет автоматически удален.")
        print("   Гость может только читать сообщения.")
        print("   Запрещено отправлять ссылки и письма.")
        
        confirm = input("\nПродолжить как гость? (да/нет): ")
        if confirm.lower() == 'да':
            guest_id = self.create_guest_account()
            self.current_user = guest_id
            self.is_guest = True
            print(f"✅ Вы вошли как гость ({guest_id})")
            print(f"📅 Аккаунт действителен до: {self.guests[guest_id]['expires_at']}")
            return True
        return False
    
    def guest_send_message(self):
        """Отправка сообщения гостем (ограниченная)"""
        if not self.is_guest:
            return False
        
        print("\n" + "="*50)
        print("📝 НАПИСАТЬ СООБЩЕНИЕ (ГОСТЬ)")
        print("="*50)
        print("⚠️  Гости могут писать только текстовые сообщения!")
        print("   Запрещено отправлять ссылки и специальные символы.")
        
        to = input("Кому (логин пользователя): ")
        
        if to not in self.users:
            print("❌ Пользователь не найден!")
            return
        
        if self.is_user_blocked(to):
            print("❌ Этот пользователь заблокирован!")
            return
        
        subject = input("Тема сообщения: ")
        
        # Проверка темы на ссылки
        if 'http://' in subject.lower() or 'https://' in subject.lower() or '.com' in subject.lower() or '.ru' in subject.lower():
            print("❌ Запрещено использовать ссылки в теме!")
            return
        
        print("Текст сообщения (введите 'END' для завершения):")
        
        message_lines = []
        while True:
            line = input()
            if line.upper() == 'END':
                break
            
            # Проверка на ссылки в тексте
            if 'http://' in line.lower() or 'https://' in line.lower() or '.com' in line.lower() or '.ru' in line.lower():
                print("❌ Запрещено отправлять ссылки!")
                return
            
            message_lines.append(line)
        
        message = '\n'.join(message_lines)
        
        # Добавляем пометку, что сообщение от гостя
        message += f"\n\n---\nОтправлено с гостевого аккаунта: {self.current_user}"
        
        new_email = {
            'id': len(self.emails) + 1,
            'from': self.current_user,
            'to': to,
            'subject': f"[ГОСТЬ] {subject}",
            'message': message,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'read': False,
            'is_guest': True
        }
        
        self.emails.append(new_email)
        
        # Обновляем статистику гостя
        self.guests[self.current_user]['messages_sent'] = self.guests[self.current_user].get('messages_sent', 0) + 1
        self.save_data()
        
        print("✅ Сообщение отправлено!")
        return True
    
    def guest_read_messages(self):
        """Чтение сообщений для гостя"""
        if not self.is_guest:
            return
        
        print("\n" + "="*50)
        print("📬 СООБЩЕНИЯ ДЛЯ ГОСТЯ")
        print("="*50)
        
        # Гость видит только сообщения, адресованные ему
        guest_emails = [email for email in self.emails if email['to'] == self.current_user]
        
        if not guest_emails:
            print("📭 У вас нет сообщений!")
            return
        
        for i, email in enumerate(guest_emails, 1):
            status = "📨" if not email['read'] else "📭"
            sender = "👤 " + email['from'] if not email.get('is_guest') else "👤 Гость"
            print(f"{i}. {status} {sender} | Тема: {email['subject']} | {email['timestamp']}")
        
        try:
            choice = int(input("\nВыберите номер сообщения для чтения (0 - отмена): ")) - 1
            if choice == -1:
                return
                
            if 0 <= choice < len(guest_emails):
                email = guest_emails[choice]
                
                print("\n" + "="*60)
                print(f"📧 СООБЩЕНИЕ #{email['id']}")
                print("="*60)
                sender = "👤 " + email['from'] if not email.get('is_guest') else "👤 Гость"
                print(f"От: {sender}")
                print(f"Тема: {email['subject']}")
                print(f"Дата: {email['timestamp']}")
                print("-" * 60)
                print(email['message'])
                print("=" * 60)
                
                # Помечаем как прочитанное
                email['read'] = True
                self.save_data()
                
            else:
                print("❌ Неверный номер сообщения!")
        except ValueError:
            print("❌ Введите число!")
    
    def guest_profile(self):
        """Профиль гостя"""
        if not self.is_guest:
            return
        
        guest_id = self.current_user
        guest_data = self.guests.get(guest_id, {})
        
        print("\n" + "="*50)
        print("👤 ПРОФИЛЬ ГОСТЯ")
        print("="*50)
        print(f"ID гостя: {guest_id}")
        print(f"Дата создания: {guest_data.get('created_at', 'Неизвестно')}")
        print(f"Действителен до: {guest_data.get('expires_at', 'Неизвестно')}")
        
        # Рассчитываем оставшееся время
        if 'expires_at' in guest_data:
            expires_at = datetime.strptime(guest_data['expires_at'], "%Y-%m-%d %H:%M:%S")
            remaining = expires_at - datetime.now()
            days = remaining.days
            hours = remaining.seconds // 3600
            
            if days < 0:
                print("⏰ Статус: ИСТЕК СРОК ДЕЙСТВИЯ")
                print("⚠️  Аккаунт будет удален при следующем входе")
            else:
                print(f"⏰ Осталось: {days} дней, {hours} часов")
        
        print(f"📤 Отправлено сообщений: {guest_data.get('messages_sent', 0)}")
        print(f"📥 Получено сообщений: {guest_data.get('messages_received', 0)}")
        
        print("\n⚠️  Ограничения гостя:")
        print("   • Нельзя отправлять ссылки")
        print("   • Нельзя отправлять письма регулярным пользователям")
        print("   • Аккаунт удаляется через 3 дня")
        print("   • Для полного доступа зарегистрируйтесь")
    
    def guest_menu(self):
        """Меню для гостя"""
        while self.is_guest:
            # Проверяем не истек ли срок действия
            if self.check_guest_expired(self.current_user):
                print("\n" + "="*50)
                print("⏰ СРОК ДЕЙСТВИЯ АККАУНТА ИСТЕК")
                print("="*50)
                print("Ваш гостевой аккаунт был удален.")
                print("Для продолжения работы зарегистрируйтесь или войдите.")
                self.current_user = None
                self.is_guest = False
                return
            
            print("\n" + "="*50)
            print(f"👤 РЕЖИМ ГОСТЯ: {self.current_user}")
            print("="*50)
            remaining_days = self.get_remaining_guest_days()
            print(f"⏰ Осталось дней: {remaining_days}")
            print("1. 📝 Написать сообщение (только текст)")
            print("2. 📬 Прочитать сообщения")
            print("3. 👤 Мой профиль гостя")
            print("4. 🚪 Выйти из режима гостя")
            print("0. ❌ Выйти из программы")
            
            choice = input("Выберите действие: ")
            
            if choice == '1':
                self.guest_send_message()
            elif choice == '2':
                self.guest_read_messages()
            elif choice == '3':
                self.guest_profile()
            elif choice == '4':
                self.current_user = None
                self.is_guest = False
                print("✅ Вы вышли из режима гостя!")
                break
            elif choice == '0':
                print("👋 До свидания!")
                exit()
            else:
                print("❌ Неверный выбор!")
    
    def get_remaining_guest_days(self):
        """Возвращает оставшееся количество дней для гостя"""
        if not self.is_guest or self.current_user not in self.guests:
            return 0
        
        guest_data = self.guests[self.current_user]
        expires_at = datetime.strptime(guest_data['expires_at'], "%Y-%m-%d %H:%M:%S")
        remaining = expires_at - datetime.now()
        return max(0, remaining.days)
    
    def lock_system(self):
        if not self.is_admin():
            print("❌ Доступ запрещен! Только crocorembo@gmail.com может блокировать систему.")
            return
            
        print("\n" + "="*50)
        print("🔒 БЛОКИРОВКА СИСТЕМЫ")
        print("="*50)
        
        admin_pass = input("Введите специальный пароль админа: ")
        if not self.verify_admin_password(admin_pass):
            print("❌ Неверный пароль админа!")
            return
        
        confirm = input("Вы уверены, что хотите заблокировать систему? (да/нет): ")
        if confirm.lower() == 'да':
            self.system_locked = True
            self.save_data()
            print("✅ Система заблокирована! Требуется пароль для доступа.")
        else:
            print("❌ Блокировка отменена.")
    
    def unlock_system(self):
        print("\n" + "="*50)
        print("🔓 РАЗБЛОКИРОВКА СИСТЕМЫ")
        print("="*50)
        
        password = input("Введите специальный пароль админа: ")
        if self.verify_admin_password(password):
            self.system_locked = False
            self.save_data()
            print("✅ Система разблокирована! Добро пожаловать!")
            return True
        else:
            print("❌ Неверный пароль! Система остается заблокированной.")
            return False
    
    def block_user(self):
        if not self.is_admin():
            print("❌ Доступ запрещен! Только crocorembo@gmail.com может блокировать пользователей.")
            return
        
        print("\n" + "="*50)
        print("🚫 БЛОКИРОВКА ПОЛЬЗОВАТЕЛЯ")
        print("="*50)
        
        admin_pass = input("Введите специальный пароль админа: ")
        if not self.verify_admin_password(admin_pass):
            print("❌ Неверный пароль админа!")
            return
        
        print("\n📋 Список пользователей:")
        for i, username in enumerate(self.users.keys(), 1):
            status = "🔴 ЗАБЛОКИРОВАН" if self.users[username].get('blocked') else "🟢 АКТИВЕН"
            print(f"{i}. {username} - {status}")
        
        target_user = input("\nВведите логин пользователя для блокировки: ")
        
        if target_user not in self.users:
            print("❌ Пользователь не найден!")
            return
        
        if target_user == self.current_user:
            print("❌ Нельзя заблокировать самого себя!")
            return
        
        if self.users[target_user].get('blocked'):
            confirm = input(f"Разблокировать пользователя {target_user}? (да/нет): ")
            if confirm.lower() == 'да':
                self.users[target_user]['blocked'] = False
                self.save_data()
                print(f"✅ Пользователь {target_user} разблокирован!")
        else:
            reason = input("Причина блокировки: ")
            confirm = input(f"Заблокировать пользователя {target_user}? (да/нет): ")
            if confirm.lower() == 'да':
                self.users[target_user]['blocked'] = True
                self.users[target_user]['block_reason'] = reason
                self.users[target_user]['blocked_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.users[target_user]['blocked_by'] = self.current_user
                self.save_data()
                print(f"✅ Пользователь {target_user} заблокирован!")
                
                block_email = {
                    'id': len(self.emails) + 1,
                    'from': 'admin@jemail.com',
                    'to': target_user,
                    'subject': '🚫 Ваш аккаунт заблокирован',
                    'message': f'''Уважаемый {target_user},

Ваш аккаунт был заблокирован администратором.

Причина: {reason}
Дата блокировки: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Если вы считаете, что это ошибка, свяжитесь с администратором.

С уважением,
Система JEmail
                    ''',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'read': False
                }
                self.emails.append(block_email)
                self.save_data()
    
    def is_user_blocked(self, username):
        return self.users.get(username, {}).get('blocked', False)
    
    def admin_tools(self):
        if not self.is_admin():
            print("❌ Доступ запрещен! Только для crocorembo@gmail.com")
            return
        
        admin_pass = input("Введите специальный пароль админа: ")
        if not self.verify_admin_password(admin_pass):
            print("❌ Неверный пароль админа!")
            return
            
        while True:
            print("\n" + "="*50)
            print("🛠️ АДМИН ПАНЕЛЬ - crocorembo@gmail.com")
            print("="*50)
            print("1. 📊 Статистика системы")
            print("2. 👥 Список всех пользователей")
            print("3. 📧 Просмотр всех писем")
            print("4. 🚫 Блокировка пользователя")
            print("5. 🗑️ Очистить все данные")
            print("6. 🔐 Изменить пароль админа")
            print("7. 📈 Статус системы")
            print("8. 👤 Управление гостями")
            print("0. ↩️ Назад")
            
            choice = input("Выберите действие: ")
            
            if choice == '1':
                self.system_stats()
            elif choice == '2':
                self.list_all_users()
            elif choice == '3':
                self.view_all_emails()
            elif choice == '4':
                self.block_user()
            elif choice == '5':
                self.clear_all_data()
            elif choice == '6':
                self.change_admin_password()
            elif choice == '7':
                self.show_system_status()
            elif choice == '8':
                self.manage_guests()
            elif choice == '0':
                break
            else:
                print("❌ Неверный выбор!")
    
    def manage_guests(self):
        """Управление гостями для админа"""
        print("\n" + "="*50)
        print("👤 УПРАВЛЕНИЕ ГОСТЯМИ")
        print("="*50)
        print(f"Всего гостей: {len(self.guests)}")
        
        # Удаляем просроченных гостей
        expired_count = 0
        guests_to_remove = []
        for guest_id in list(self.guests.keys()):
            if self.check_guest_expired(guest_id):
                guests_to_remove.append(guest_id)
                expired_count += 1
        
        if expired_count > 0:
            print(f"🚮 Удалено просроченных гостей: {expired_count}")
        
        print("\n📋 Активные гости:")
        for i, (guest_id, guest_data) in enumerate(self.guests.items(), 1):
            expires_at = datetime.strptime(guest_data['expires_at'], "%Y-%m-%d %H:%M:%S")
            remaining = expires_at - datetime.now()
            days = remaining.days
            status = "🟢" if days > 0 else "🔴"
            print(f"{i}. {status} {guest_id}")
            print(f"   Создан: {guest_data.get('created_at')}")
            print(f"   Истекает через: {max(0, days)} дней")
            print(f"   Сообщений: 📤{guest_data.get('messages_sent', 0)} 📥{guest_data.get('messages_received', 0)}")
    
    def system_stats(self):
        print("\n" + "="*50)
        print("📊 СТАТИСТИКА СИСТЕМЫ")
        print("="*50)
        print(f"Всего пользователей: {len(self.users)}")
        print(f"Всего писем: {len(self.emails)}")
        print(f"Активных гостей: {len(self.guests)}")
        
        blocked_users = sum(1 for user in self.users.values() if user.get('blocked'))
        active_users = len(self.users) - blocked_users
        print(f"Активных пользователей: {active_users}")
        print(f"Заблокированных пользователей: {blocked_users}")
        
        read_emails = sum(1 for email in self.emails if email.get('read', False))
        unread_emails = len(self.emails) - read_emails
        print(f"Прочитанных писем: {read_emails}")
        print(f"Непрочитанных писем: {unread_emails}")
        
        print("\n📈 Последние пользователи:")
        recent_users = sorted(self.users.items(), 
                            key=lambda x: x[1].get('registered_at', ''), 
                            reverse=True)[:5]
        for username, data in recent_users:
            status = "🔴" if data.get('blocked') else "🟢"
            print(f"  {status} {username} - {data.get('email', 'N/A')}")
    
    def list_all_users(self):
        print("\n" + "="*50)
        print("👥 ВСЕ ПОЛЬЗОВАТЕЛИ")
        print("="*50)
        for username, data in self.users.items():
            status = "🔴 ЗАБЛОКИРОВАН" if data.get('blocked') else "🟢 АКТИВЕН"
            print(f"{status} 👤 {username}")
            print(f"   📧 Email: {data.get('email', 'N/A')}")
            print(f"   📅 Регистрация: {data.get('registered_at', 'N/A')}")
            
            if data.get('blocked'):
                print(f"   🚫 Причина блокировки: {data.get('block_reason', 'N/A')}")
                print(f"   ⏰ Заблокирован: {data.get('blocked_at', 'N/A')}")
                print(f"   👮 Заблокировал: {data.get('blocked_by', 'N/A')}")
            
            user_emails = len([email for email in self.emails if email['to'] == username])
            sent_emails = len([email for email in self.emails if email['from'] == username])
            print(f"   📨 Получено: {user_emails} | 📤 Отправлено: {sent_emails}")
            print()
    
    def view_all_emails(self):
        print("\n" + "="*50)
        print("📧 ВСЕ ПИСЬМА В СИСТЕМЕ")
        print("="*50)
        for email in self.emails:
            status = "📨" if not email.get('read', False) else "📭"
            sender = email['from'] + " (гость)" if email.get('is_guest') else email['from']
            print(f"{status} ID: {email['id']} | От: {sender} → Кому: {email['to']}")
            print(f"   Тема: {email['subject']}")
            print(f"   Дата: {email['timestamp']}")
            print()
    
    def clear_all_data(self):
        print("\n" + "="*50)
        print("⚠️ ОПАСНАЯ ЗОНА - ОЧИСТКА ВСЕХ ДАННЫХ")
        print("="*50)
        confirm = input("Вы ТОЧНО уверены? Это удалит ВСЕХ пользователей и ВСЕ письма! (да/НЕТ): ")
        if confirm.lower() == 'да':
            double_confirm = input("Введите 'УДАЛИТЬ ВСЁ' для подтверждения: ")
            if double_confirm == 'УДАЛИТЬ ВСЁ':
                self.users = {}
                self.emails = []
                self.guests = {}
                self.save_data()
                print("✅ Все данные удалены!")
            else:
                print("❌ Отменено.")
        else:
            print("❌ Отменено.")
    
    def change_admin_password(self):
        print("\n" + "="*50)
        print("🔐 ИЗМЕНЕНИЕ ПАРОЛЯ АДМИНА")
        print("="*50)
        current_pass = input("Введите текущий пароль: ")
        if not self.verify_admin_password(current_pass):
            print("❌ Неверный текущий пароль!")
            return
        
        new_pass = input("Введите новый пароль: ")
        confirm_pass = input("Повторите новый пароль: ")
        
        if new_pass == confirm_pass:
            self.admin_password = new_pass
            print("✅ Пароль админа изменен!")
        else:
            print("❌ Пароли не совпадают!")
    
    def show_system_status(self):
        print("\n" + "="*50)
        print("📊 СТАТУС СИСТЕМЫ")
        print("="*50)
        status = "🔒 ЗАБЛОКИРОВАНА" if self.system_locked else "🔓 РАБОТАЕТ НОРМАЛЬНО"
        print(f"Статус: {status}")
        print(f"Пользователей: {len(self.users)}")
        print(f"Активных гостей: {len(self.guests)}")
        
        blocked_users = sum(1 for user in self.users.values() if user.get('blocked'))
        active_users = len(self.users) - blocked_users
        print(f"Активных: {active_users} | Заблокированных: {blocked_users}")
        print(f"Писем в системе: {len(self.emails)}")
        
        if self.system_locked:
            print("\n⚠️ Для разблокировки нужен специальный пароль админа")
    
    def register_user(self):
        if self.system_locked:
            print("❌ Система заблокирована! Обратитесь к администратору.")
            return False
            
        print("\n" + "="*50)
        print("🎉 РЕГИСТРАЦИЯ В JEMAIL")
        print("="*50)
        
        username = input("Придумайте логин: ")
        
        if username in self.users:
            print("❌ Этот логин уже занят!")
            return False
        
        password = input("Придумайте пароль: ")
        
        is_valid, message = self.validate_password(password)
        if not is_valid:
            print(message)
            return False
        
        email = input("Введите email: ")
        
        self.users[username] = {
            'password': self.hash_password(password),
            'email': email,
            'registered_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'blocked': False
        }
        
        self.save_data()
        
        welcome_email = {
            'id': len(self.emails) + 1,
            'from': 'admin@jemail.com',
            'to': username,
            'subject': 'Добро пожаловать в JEmail! 🎉',
            'message': f'''Приветствуем, {username}!

Добро пожаловать в JEmail - лучшую почтовую систему!

Ваш email: {email}
Дата регистрации: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

📝 Правила использования:
• Пароль должен быть не менее 9 символов
• Запрещены последовательности типа 123, 234 и т.д.
• Запрещены символы: ! # . ?

С уважением,
Команда JEmail 📧
            ''',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'read': False
        }
        
        self.emails.append(welcome_email)
        self.save_data()
        
        print(f"✅ Регистрация успешна! Добро пожаловать, {username}!")
        return True
    
    def login(self):
        if self.system_locked:
            print("❌ Система заблокирована! Обратитесь к администратору.")
            return False
            
        print("\n" + "="*50)
        print("🔐 ВХОД В JEMAIL")
        print("="*50)
        
        username = input("Логин: ")
        password = input("Пароль: ")
        
        if username in self.users:
            if self.is_user_blocked(username):
                user_data = self.users[username]
                print("🚫 Ваш аккаунт заблокирован!")
                print(f"Причина: {user_data.get('block_reason', 'Не указана')}")
                print(f"Дата блокировки: {user_data.get('blocked_at', 'Неизвестно')}")
                return False
            
            if self.users[username]['password'] == self.hash_password(password):
                self.current_user = username
                self.is_guest = False
                print(f"✅ Вход выполнен! Приветствуем, {username}!")
                return True
            else:
                print("❌ Неверный пароль!")
        else:
            print("❌ Пользователь не найден!")
        
        return False
    
    def send_email(self):
        if not self.current_user or self.is_guest:
            print("❌ Гости не могут отправлять обычные письма!")
            return
        
        if self.is_user_blocked(self.current_user):
            print("🚫 Ваш аккаунт заблокирован! Вы не можете отправлять письма.")
            return
        
        print("\n" + "="*50)
        print("📨 ОТПРАВКА ПИСЬМА")
        print("="*50)
        
        to = input("Кому (логин): ")
        
        if to not in self.users:
            print("❌ Получатель не найден!")
            return
        
        if self.is_user_blocked(to):
            print("❌ Этот пользователь заблокирован и не может получать письма!")
            return
        
        subject = input("Тема: ")
        print("Текст письма (введите 'END' для завершения):")
        
        message_lines = []
        while True:
            line = input()
            if line.upper() == 'END':
                break
            message_lines.append(line)
        
        message = '\n'.join(message_lines)
        
        new_email = {
            'id': len(self.emails) + 1,
            'from': self.current_user,
            'to': to,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'read': False
        }
        
        self.emails.append(new_email)
        self.save_data()
        
        print("✅ Письмо отправлено!")
    
    def check_emails(self):
        if not self.current_user:
            print("❌ Сначала войдите в систему!")
            return
        
        user_emails = [email for email in self.emails if email['to'] == self.current_user]
        
        print("\n" + "="*50)
        print(f"📬 ВАША ПОЧТА ({len(user_emails)} писем)")
        print("="*50)
        
        if not user_emails:
            print("📭 Почта пуста!")
            return
        
        unread_count = sum(1 for email in user_emails if not email['read'])
        if unread_count > 0:
            print(f"🔔 У вас {unread_count} непрочитанных писем!")
        
        for i, email in enumerate(user_emails, 1):
            status = "📨" if not email['read'] else "📭"
            print(f"{i}. {status} От: {email['from']} | Тема: {email['subject']} | {email['timestamp']}")
    
    def read_email(self):
        if not self.current_user:
            print("❌ Сначала войдите в систему!")
            return
        
        user_emails = [email for email in self.emails if email['to'] == self.current_user]
        
        if not user_emails:
            print("📭 Почта пуста!")
            return
        
        self.check_emails()
        
        try:
            choice = int(input("\nВыберите номер письма для чтения: ")) - 1
            if 0 <= choice < len(user_emails):
                email = user_emails[choice]
                
                print("\n" + "="*60)
                print(f"📧 ПИСЬМО #{email['id']}")
                print("="*60)
                print(f"От: {email['from']}")
                print(f"Кому: {email['to']}")
                print(f"Тема: {email['subject']}")
                print(f"Дата: {email['timestamp']}")
                print("-" * 60)
                print(email['message'])
                print("=" * 60)
                
                email['read'] = True
                self.save_data()
                
            else:
                print("❌ Неверный номер письма!")
        except ValueError:
            print("❌ Введите число!")
    
    def user_profile(self):
        if not self.current_user or self.is_guest:
            print("❌ Сначала войдите в систему!")
            return
        
        user_data = self.users[self.current_user]
        
        print("\n" + "="*50)
        print("👤 ВАШ ПРОФИЛЬ")
        print("="*50)
        print(f"Логин: {self.current_user}")
        print(f"Email: {user_data['email']}")
        print(f"Зарегистрирован: {user_data['registered_at']}")
        
        user_emails = len([email for email in self.emails if email['to'] == self.current_user])
        sent_emails = len([email for email in self.emails if email['from'] == self.current_user])
        
        print(f"Получено писем: {user_emails}")
        print(f"Отправлено писем: {sent_emails}")
        
        if user_data.get('blocked'):
            print("🚫 Статус: АККАУНТ ЗАБЛОКИРОВАН")
            print(f"Причина: {user_data.get('block_reason', 'Не указана')}")
            print(f"Заблокирован: {user_data.get('blocked_at', 'Неизвестно')}")
        else:
            print("🟢 Статус: АККАУНТ АКТИВЕН")
        
        if self.is_admin():
            print("⭐ Дополнительно: АДМИНИСТРАТОР СИСТЕМЫ")
    
    def main_menu(self):
        while True:
            print("\n" + "="*50)
            print("🏠 ГЛАВНОЕ МЕНЮ JEMAIL")
            print("="*50)
            
            if self.system_locked:
                print("🔒 СИСТЕМА ЗАБЛОКИРОВАНА")
                print("1. 🔓 Разблокировать систему (только для админа)")
                print("0. ❌ Выйти")
                
                choice = input("Выберите действие: ")
                
                if choice == '1':
                    if self.unlock_system():
                        continue
                elif choice == '0':
                    print("👋 До свидания!")
                    break
                else:
                    print("❌ Неверный выбор! Система заблокирована.")
            
            elif self.current_user:
                if self.is_guest:
                    self.guest_menu()
                    continue
                else:
                    print(f"👋 Привет, {self.current_user}!")
                    print("1. 📨 Отправить письмо")
                    print("2. 📬 Проверить почту")
                    print("3. 📧 Прочитать письмо")
                    print("4. 👤 Мой профиль")
                    print("5. 🚪 Выйти из аккаунта")
                    
                    if self.is_admin():
                        print("12. 🔒 Заблокировать систему")
                        print("13. 🛠️ Админ панель")
                    
                    print("0. ❌ Выйти из программы")
                    
                    choice = input("Выберите действие: ")
                    
                    if choice == '1':
                        self.send_email()
                    elif choice == '2':
                        self.check_emails()
                    elif choice == '3':
                        self.read_email()
                    elif choice == '4':
                        self.user_profile()
                    elif choice == '5':
                        self.current_user = None
                        self.is_guest = False
                        print("✅ Вы вышли из аккаунта!")
                    elif choice == '12' and self.is_admin():
                        self.lock_system()
                    elif choice == '13' and self.is_admin():
                        self.admin_tools()
                    elif choice == '0':
                        print("👋 До свидания! Спасибо за использование JEmail!")
                        break
                    else:
                        print("❌ Неверный выбор!")
            
            else:
                # ГЛАВНОЕ МЕНЮ ДОБАВЛЕНО "Войти как гость"
                print("1. 🎉 Зарегистрироваться")
                print("2. 🔐 Войти")
                print("3. 👤 Войти как гость (3 дня)")
                print("0. ❌ Выйти")
                
                choice = input("Выберите действие: ")
                
                if choice == '1':
                    self.register_user()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    if self.enter_as_guest():
                        continue
                elif choice == '0':
                    print("👋 До свидания!")
                    break
                else:
                    print("❌ Неверный выбор!")

if __name__ == "__main__":
    print("🌐 Добро пожаловать в JEmail - вашу почтовую систему!")
    print("📝 Правила паролей:")
    print("   • Не менее 9 символов")
    print("   • Запрещены: 123, 234, 345 и т.д.")
    print("   • Запрещены символы: ! # . ?")
    print("👤 Теперь доступен гостевой режим на 3 дня!")
    system = JEMailSystem()
    system.main_menu()