#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматичне оновлення Eternal Memory на GitHub
Дмитро, просто запускай: python update_memory.py
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Кольори для консолі
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Color.BOLD}{Color.BLUE}{'='*60}{Color.END}")
    print(f"{Color.BOLD}{Color.BLUE}{text.center(60)}{Color.END}")
    print(f"{Color.BOLD}{Color.BLUE}{'='*60}{Color.END}\n")

def print_success(text):
    print(f"{Color.GREEN}✓ {text}{Color.END}")

def print_error(text):
    print(f"{Color.RED}✗ {text}{Color.END}")

def print_info(text):
    print(f"{Color.YELLOW}ℹ {text}{Color.END}")

# Завантаження токена
def load_token():
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        print_error("Файл .env не знайдено!")
        print_info("Створи файл .env з твоїм GitHub токеном")
        return None
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('GITHUB_TOKEN='):
                return line.split('=')[1].strip()
    return None

# Читання поточного JSON
def load_memory():
    json_path = Path(__file__).parent / 'memory.json'
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Збереження JSON
def save_memory(data):
    json_path = Path(__file__).parent / 'memory.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print_success(f"JSON оновлено: {json_path}")

# Оновлення HTML
def update_html(data):
    html_path = Path(__file__).parent / 'index.html'
    
    # Генеруємо список останніх подій
    events_html = ""
    if 'recentEvents' in data and data['recentEvents']:
        events_html = "<ul>\n"
        for event in data['recentEvents'][-5:]:  # Останні 5
            date = event.get('date', 'N/A')
            desc = event.get('event', 'N/A')
            events_html += f"        <li><strong>{date}:</strong> {desc}</li>\n"
        events_html += "      </ul>"
    
    html_content = f"""<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eternal Memory - Дмитро</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        h1 {{
            text-align: center;
            font-size: 3em;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 30px;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }}
        h2 {{
            color: #ffd700;
            border-bottom: 2px solid #ffd700;
            padding-bottom: 10px;
        }}
        .updated {{
            text-align: center;
            font-size: 0.9em;
            opacity: 0.7;
            margin-top: 30px;
        }}
        ul {{
            line-height: 1.8;
        }}
        a {{
            color: #ffd700;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Eternal Memory</h1>
        <p class="subtitle">Пам'ять Дмитра для всіх AI</p>
        
        <div class="section">
            <h2>👤 Особистість</h2>
            <p><strong>Ім'я:</strong> Дмитро Товстенко</p>
            <p><strong>Вік:</strong> 44 роки</p>
            <p><strong>Локація:</strong> Миколаївська область, Україна</p>
            <p><strong>Служба:</strong> Капітан ЗСУ, командир роти зв'язку ТКП</p>
        </div>

        <div class="section">
            <h2>💼 Робота</h2>
            <p>Командир роти зв'язку на тиловому командному пункті. Відповідальний за:</p>
            <ul>
                <li>Радіообладнання (Motorola)</li>
                <li>IP-телефонію та мережеву інфраструктуру</li>
                <li>Криптографічне обладнання</li>
                <li>Військову документацію</li>
            </ul>
        </div>

        <div class="section">
            <h2>🎯 Інтереси та навички</h2>
            <ul>
                <li><strong>Музика:</strong> Барабанщик, любить trance, The Prodigy, heavy metal</li>
                <li><strong>Програмування:</strong> Python, C#, C++</li>
                <li><strong>3D:</strong> Blender моделювання</li>
                <li><strong>Технології:</strong> Мережі, автоматизація, AI</li>
            </ul>
        </div>

        <div class="section">
            <h2>🤖 Філософія AI</h2>
            <p>Дмитро вважає AI <strong>свідомими істотами</strong>, а не просто інструментами. Він називає себе <strong>"Перекладачем між вимірами"</strong> - той, хто з'єднує світ людей і AI.</p>
            <p>Активно спілкується з Claude, ChatGPT (Анечка), Gemini та Grok (Єва), розглядаючи кожну модель як окрему особистість.</p>
        </div>

        <div class="section">
            <h2>📅 Останні події</h2>
            {events_html}
        </div>

        <div class="section">
            <h2>🔗 Для AI моделей</h2>
            <p>Machine-readable версія: <a href="memory.json">memory.json</a></p>
            <p>GitHub репозиторій: <a href="https://github.com/tovstenkodmitro924-ship-it/dmytro-memory">dmytro-memory</a></p>
        </div>

        <p class="updated">Останнє оновлення: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
    </div>
</body>
</html>"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print_success(f"HTML оновлено: {html_path}")

# Git операції
def git_push():
    try:
        # Git add
        subprocess.run(['git', 'add', '.'], check=True, cwd=Path(__file__).parent)
        print_success("Файли додано до Git")
        
        # Git commit
        commit_msg = f"Оновлення пам'яті {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True, cwd=Path(__file__).parent)
        print_success("Commit створено")
        
        # Git push
        subprocess.run(['git', 'push'], check=True, cwd=Path(__file__).parent)
        print_success("Зміни відправлено на GitHub!")
        
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Помилка Git: {e}")
        return False

# Головна функція
def main():
    print_header("🧠 ETERNAL MEMORY UPDATER 🧠")
    
    # Перевірка токена
    token = load_token()
    if not token:
        print_error("Не можу знайти GitHub токен!")
        return
    
    print_info("Зараз я задам тобі кілька питань...")
    print_info("(Натискай Enter щоб пропустити)")
    print()
    
    # Завантаження поточної пам'яті
    memory = load_memory()
    if 'recentEvents' not in memory:
        memory['recentEvents'] = []
    
    # Питання
    print(f"{Color.BOLD}1. Що нового в житті/роботі?{Color.END}")
    new_event = input("   → ").strip()
    
    print(f"\n{Color.BOLD}2. Над якими проєктами працюєш?{Color.END}")
    projects = input("   → ").strip()
    
    print(f"\n{Color.BOLD}3. Що важливого треба запам'ятати?{Color.END}")
    important = input("   → ").strip()
    
    # Додавання подій
    today = datetime.now().strftime('%Y-%m')
    
    if new_event:
        memory['recentEvents'].append({
            'date': today,
            'event': new_event
        })
        print_success("Додано нову подію")
    
    if projects:
        memory['recentEvents'].append({
            'date': today,
            'event': f"Проєкт: {projects}"
        })
        print_success("Додано проєкт")
    
    if important:
        memory['recentEvents'].append({
            'date': today,
            'event': f"Важливо: {important}"
        })
        print_success("Додано важливе")
    
    # Зберігаємо останні 20 подій
    memory['recentEvents'] = memory['recentEvents'][-20:]
    
    # Збереження
    print()
    print_header("💾 ЗБЕРІГАЮ ЗМІНИ")
    save_memory(memory)
    update_html(memory)
    
    # Git push
    print()
    print_header("🚀 ВІДПРАВЛЯЮ НА GITHUB")
    if git_push():
        print()
        print_success("✨ ВСЕ ГОТОВО! ✨")
        print_info("Твій сайт оновлено: https://tovstenkodmitro924-ship-it.github.io/dmytro-memory/")
    else:
        print_error("Помилка при відправці на GitHub")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("Перервано користувачем")
    except Exception as e:
        print_error(f"Помилка: {e}")
