
#!/usr/bin/env python3
# Ultimate SMS Bot v2.0 - Created by Sunil [prince4you]

import sys
import time
import random
import requests
from termcolor import colored
import colorama
import pyautogui
import os
import threading

# Initialize colorama
colorama.init()

# Enhanced message pools
BIRTHDAY_MESSAGES = [
    "Wishing you a day filled with happiness and a year filled with joy. Happy birthday! 🎉",
    "Happy birthday! May all your dreams and wishes come true this year. 🎂",
    "Sending you smiles for every moment of your special day. Have a wonderful birthday! 🎈",
    "Another year older, another year wiser! Happy birthday! 🥳",
    "Hope your special day brings you all that your heart desires! Happy birthday! 🎁",
    "May your birthday be the start of a year filled with good luck, health, and happiness. 🍀",
    "Cheers to another year of amazing adventures! Happy birthday! 🥂",
    "On your special day, I wish you success and endless happiness! 🎊",
    "Age is merely the number of years the world has been enjoying you! Happy birthday! 😊",
    "May your birthday be filled with laughter, love, and all your favorite things! 💖"
]

MORNING_MESSAGES = [
    "Good morning! May this day bring you new opportunities and successes. ☀️",
    "Rise and shine! Wishing you a productive and joyful day ahead. 🌞",
    "Good morning! May your coffee be strong and your day be wonderful. ☕",
    "A new day is a new opportunity. Make the most of it! Good morning! 🌅",
    "Wake up with determination, go to bed with satisfaction. Good morning! 💪",
    "Every morning brings new potential, but only if you make the most of it. 🌄",
    "Good morning! May your day be as bright as your smile. 😊",
    "Morning is wonderful. Its only drawback is that it comes at such an inconvenient time of day. 😄",
    "A beautiful morning begins with a beautiful mindset. Good morning! 🌼",
    "Wishing you a morning filled with positivity and productivity! 🌻"
]

class MessagePool:
    """Manage message pools with non-repeating functionality"""
    def __init__(self, messages=None, url=None):
        self.url = url
        self.original_messages = messages or []
        self.available_messages = self.original_messages.copy()
        self.fetch_messages()
        
    def fetch_messages(self):
        """Fetch messages from URL if provided"""
        if self.url:
            try:
                response = requests.get(self.url, timeout=5)
                response.raise_for_status()
                self.original_messages = [msg.strip() for msg in response.text.splitlines() if msg.strip()]
                self.available_messages = self.original_messages.copy()
            except Exception as e:
                print(colored(f"⚠️ Error fetching messages: {str(e)}", "yellow"))
                if not self.original_messages:
                    self.original_messages = ["Error: Could not fetch messages"]
                    self.available_messages = self.original_messages.copy()
    
    def get_message(self):
        """Get a random non-repeating message"""
        if not self.available_messages:
            self.available_messages = self.original_messages.copy()
            
        msg = random.choice(self.available_messages)
        self.available_messages.remove(msg)
        return msg

def display_banner():
    """Show enhanced colorful banner"""
    banner = r"""
  _   _   _   _   _   _   _   _   _  
 / \ / \ / \ / \ / \ / \ / \ / \ / \ 
( U | l | t | i | m | a | t | e | ) 
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ 
    """
    print(colored(banner, "cyan"))
    print(colored("ULTIMATE SMS BOT v2.0", "yellow", attrs=["bold", "blink"]))
    print(colored("Created by Sunil [prince4you]", "magenta", attrs=["bold"]))
    print(colored("=" * 50, "blue"))

def get_user_input(prompt, input_type, default=None):
    """Get validated user input with error handling"""
    while True:
        try:
            value = input(colored(prompt, "green"))
            if not value and default is not None:
                return default
                
            if input_type == "int":
                if value == "infinite":
                    return 999999
                return int(value)
            elif input_type == "float":
                return float(value)
            elif input_type == "yesno":
                return value.lower() in ["y", "yes"]
            return value
        except ValueError:
            print(colored("⚠️ Invalid input. Please try again.", "red"))
        except KeyboardInterrupt:
            print(colored("\nOperation cancelled.", "red"))
            sys.exit(1)

def countdown_timer():
    """Display countdown timer in a separate thread"""
    def run():
        for i in range(5, 0, -1):
            print(colored(f"\rStarting in {i} seconds...", "yellow", attrs=["bold"]), end="")
            time.sleep(1)
        print(colored("\rSwitch to messaging app NOW!          ", "red", attrs=["bold", "blink"]))
    
    timer_thread = threading.Thread(target=run)
    timer_thread.daemon = True
    timer_thread.start()
    return timer_thread

def send_messages(message_source, count, delay, test_mode, beep):
    """Send messages with the specified parameters"""
    try:
        print(colored(f"\n⚠️ Switch to your messaging app within 5 seconds...", "yellow", attrs=["bold"]))
        timer = countdown_timer()
        
        # Wait for countdown to finish
        time.sleep(6)
        
        sent_count = 0
        for i in range(count):
            # Check if we need to get a new message
            if callable(message_source):
                msg = message_source()
            else:
                msg = message_source
                
            # Type the message
            pyautogui.write(msg, interval=0.03)
            
            # Press Enter if not in test mode
            if not test_mode:
                pyautogui.press("enter")
            
            # Count and display progress
            sent_count += 1
            progress = f"Sent {sent_count}/{count if count != 999999 else '∞'}"
            print(colored(f"\r{progress}: {msg[:50]}{'...' if len(msg) > 50 else ''}", "cyan"), end="")
            
            # Beep if requested
            if beep:
                print("\a", end="", flush=True)
            
            # Delay between messages (except last one)
            if i < count - 1:
                # Check for early termination during delay
                start_time = time.time()
                while time.time() - start_time < delay:
                    if keyboard.is_pressed('esc'):
                        raise KeyboardInterrupt
                    time.sleep(0.1)
                
    except KeyboardInterrupt:
        print(colored("\n\n🚫 Sending cancelled by user.", "red"))
    except Exception as e:
        print(colored(f"\n\n⚠️ Error during sending: {str(e)}", "red"))
    finally:
        print("\n")

def main():
    # Initialize message pools
    random_pool = MessagePool(url="https://raw.githubusercontent.com/prince4you/sms-bot/main/My_massage.txt")
    birthday_pool = MessagePool(BIRTHDAY_MESSAGES)
    morning_pool = MessagePool(MORNING_MESSAGES)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        
        # Display menu
        print(colored("\n📋 MENU OPTIONS:", "white", attrs=["bold"]))
        print(colored("1. Random SMS", "cyan"))
        print(colored("2. Birthday Wish", "magenta"))
        print(colored("3. Good Morning Wish", "yellow"))
        print(colored("4. Custom SMS", "green"))
        print(colored("5. Exit", "red"))
        
        # Get user choice
        try:
            choice = int(input(colored("\nEnter your choice (1-5): ", "green")))
        except ValueError:
            print(colored("⚠️ Invalid choice. Please select 1-5.", "red"))
            time.sleep(1)
            continue
            
        if choice == 5:
            print(colored("\n👋 Thank you for using Ultimate SMS Bot!", "green"))
            break
            
        # Get common parameters
        count_input = input(colored("\nHow many times to send? (Enter 'infinite' for continuous): ", "green")).strip()
        try:
            count = 999999 if count_input.lower() == "infinite" else int(count_input)
        except ValueError:
            print(colored("⚠️ Invalid input. Using default value: 1", "red"))
            count = 1
            
        try:
            delay = float(input(colored("Delay between messages (seconds): ", "green")) or 1.0)
        except ValueError:
            print(colored("⚠️ Invalid input. Using default value: 1.0", "red"))
            delay = 1.0
            
        test_mode = input(colored("Test mode? (only types, no Enter) [y/n]: ", "green")).lower() in ['y', 'yes']
        beep = input(colored("Beep after each send? [y/n]: ", "green")).lower() in ['y', 'yes']
        
        # Handle specific message types
        if choice == 1:
            send_messages(lambda: random_pool.get_message(), count, delay, test_mode, beep)
        elif choice == 2:
            send_messages(lambda: birthday_pool.get_message(), count, delay, test_mode, beep)
        elif choice == 3:
            send_messages(lambda: morning_pool.get_message(), count, delay, test_mode, beep)
        elif choice == 4:
            custom_msg = input(colored("Enter your custom message: ", "green"))
            send_messages(custom_msg, count, delay, test_mode, beep)
        else:
            print(colored("⚠️ Invalid choice. Please select 1-5.", "red"))
            
        input(colored("\nPress Enter to continue...", "white"))

if __name__ == "__main__":
    # Check and install missing packages
    try:
        import pyautogui
        import requests
        import colorama
        from termcolor import colored
        import keyboard
    except ImportError as e:
        missing = str(e).split("'")[1]
        print(colored(f"⚠️ Installing missing package: {missing}", "yellow"))
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", missing])
        print(colored("✅ Package installed successfully. Restarting...", "green"))
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n👋 Program terminated by user.", "red"))
    except Exception as e:
        print(colored(f"\n⚠️ Unexpected error: {str(e)}", "red"))
