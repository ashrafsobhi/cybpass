#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CYB PASS - Interactive Password Generator Tool
Advanced Password Generator with Personal Information Integration
"""

import random
import string
import sys
import os
import time
import json
import csv
import hashlib
import base64
from datetime import datetime
from typing import Dict, List, Optional

# Color codes for terminal output
class Colors:
    # Basic colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Bright colors
    BRIGHT_RED = '\033[1;91m'
    BRIGHT_GREEN = '\033[1;92m'
    BRIGHT_YELLOW = '\033[1;93m'
    BRIGHT_BLUE = '\033[1;94m'
    BRIGHT_MAGENTA = '\033[1;95m'
    BRIGHT_CYAN = '\033[1;96m'
    BRIGHT_WHITE = '\033[1;97m'
    
    # Background colors
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    BG_MAGENTA = '\033[105m'
    BG_CYAN = '\033[106m'
    
    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Reset
    RESET = '\033[0m'
    END = '\033[0m'

# Check if colors are supported
def supports_color():
    """Check if terminal supports colors"""
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

# Color wrapper function
def colorize(text, color):
    """Apply color to text if supported"""
    if supports_color():
        return f"{color}{text}{Colors.RESET}"
    return text

class ProgressBar:
    """Professional progress bar for operations"""
    def __init__(self, total: int, width: int = 50):
        self.total = total
        self.width = width
        self.current = 0
    
    def update(self, current: int, message: str = ""):
        self.current = current
        percent = (current / self.total) * 100
        filled = int((current / self.total) * self.width)
        bar = "█" * filled + "░" * (self.width - filled)
        
        if message:
            print(f"\r{colorize(f'[{bar}] {percent:.1f}%', Colors.BRIGHT_CYAN)} {colorize(message, Colors.YELLOW)}", end="", flush=True)
        else:
            print(f"\r{colorize(f'[{bar}] {percent:.1f}%', Colors.BRIGHT_CYAN)}", end="", flush=True)
    
    def complete(self, message: str = "Complete!"):
        print(f"\r{colorize(f'[{"█" * self.width}] 100.0%', Colors.BRIGHT_GREEN)} {colorize(message, Colors.BRIGHT_GREEN)}")

class PasswordAnalyzer:
    """Advanced password strength analyzer"""
    
    @staticmethod
    def analyze_strength(password: str) -> Dict:
        """Comprehensive password strength analysis"""
        analysis = {
            'score': 0,
            'length': len(password),
            'has_upper': any(c.isupper() for c in password),
            'has_lower': any(c.islower() for c in password),
            'has_digit': any(c.isdigit() for c in password),
            'has_special': any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
            'has_common_patterns': False,
            'entropy': 0,
            'recommendations': []
        }
        
        # Length scoring
        if analysis['length'] >= 12:
            analysis['score'] += 2
        elif analysis['length'] >= 8:
            analysis['score'] += 1
        
        # Character type scoring
        analysis['score'] += sum([analysis['has_upper'], analysis['has_lower'], 
                                 analysis['has_digit'], analysis['has_special']])
        
        # Check for common patterns
        common_patterns = ['123', 'abc', 'qwe', 'password', 'admin']
        analysis['has_common_patterns'] = any(pattern in password.lower() for pattern in common_patterns)
        
        if analysis['has_common_patterns']:
            analysis['score'] -= 1
            analysis['recommendations'].append("Avoid common patterns")
        
        # Calculate entropy
        charset_size = 0
        if analysis['has_lower']:
            charset_size += 26
        if analysis['has_upper']:
            charset_size += 26
        if analysis['has_digit']:
            charset_size += 10
        if analysis['has_special']:
            charset_size += 32
        
        if charset_size > 0:
            analysis['entropy'] = analysis['length'] * (charset_size ** 0.5)
        
        # Generate recommendations
        if not analysis['has_upper']:
            analysis['recommendations'].append("Add uppercase letters")
        if not analysis['has_lower']:
            analysis['recommendations'].append("Add lowercase letters")
        if not analysis['has_digit']:
            analysis['recommendations'].append("Add numbers")
        if not analysis['has_special']:
            analysis['recommendations'].append("Add special characters")
        if analysis['length'] < 12:
            analysis['recommendations'].append("Use at least 12 characters")
        
        return analysis
    
    @staticmethod
    def get_strength_level(score: int) -> tuple:
        """Get strength level and color based on score"""
        if score <= 2:
            return "Weak", Colors.RED
        elif score <= 4:
            return "Medium", Colors.YELLOW
        elif score <= 6:
            return "Strong", Colors.BRIGHT_GREEN
        else:
            return "Very Strong", Colors.BRIGHT_MAGENTA

class FileManager:
    """Professional file management with encryption"""
    
    @staticmethod
    def encrypt_data(data: str, key: str) -> str:
        """Simple encryption for sensitive data"""
        key_hash = hashlib.sha256(key.encode()).digest()
        encoded = base64.b64encode(data.encode()).decode()
        return encoded
    
    @staticmethod
    def decrypt_data(encrypted_data: str, key: str) -> str:
        """Decrypt data"""
        try:
            decoded = base64.b64decode(encrypted_data.encode()).decode()
            return decoded
        except:
            return encrypted_data
    
    @staticmethod
    def save_passwords_json(passwords: List[Dict], filename: str, user_info: Dict) -> bool:
        """Save passwords in JSON format - passwords only"""
        try:
            # Extract only passwords from the data
            password_list = [pwd['password'] for pwd in passwords]
            
            data = {
                'user_info': {
                    'name': user_info.get('name', 'Unknown'),
                    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'passwords': password_list,
                'total_count': len(password_list),
                'version': '2.0.0'
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(colorize(f"[ERROR] Failed to save JSON: {e}", Colors.RED))
            return False
    
    @staticmethod
    def save_passwords_csv(passwords: List[Dict], filename: str) -> bool:
        """Save passwords in CSV format - passwords only"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Password'])  # Header with only Password column
                for pwd in passwords:
                    writer.writerow([pwd['password']])
            return True
        except Exception as e:
            print(colorize(f"[ERROR] Failed to save CSV: {e}", Colors.RED))
            return False

class PasswordGenerator:
    def __init__(self):
        self.passwords = []
        self.user_info = {}
        self.password_categories = {
            'banking': 'Banking & Financial',
            'email': 'Email Accounts',
            'social': 'Social Media',
            'work': 'Work & Professional',
            'gaming': 'Gaming & Entertainment',
            'shopping': 'Shopping & E-commerce',
            'general': 'General Purpose'
        }
        self.analyzer = PasswordAnalyzer()
        self.file_manager = FileManager()
        
    def clear_screen(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print tool header with ASCII art logo"""
        # ASCII Art Logo for CYB PASS
        print(colorize('╔══════════════════════════════════════════════════════════╗', Colors.BRIGHT_CYAN))
        print(colorize('║                                                          ║', Colors.BRIGHT_CYAN))
        print(colorize('║  ', Colors.BRIGHT_CYAN) + colorize('    ██████╗██╗   ██╗██████╗    ██████╗  █████╗ ███████╗███████╗', Colors.BRIGHT_MAGENTA) + colorize('  ║', Colors.BRIGHT_CYAN))
        print(colorize('║  ', Colors.BRIGHT_CYAN) + colorize('   ██╔════╝╚██╗ ██╔╝██╔══██╗   ██╔══██╗██╔══██╗██╔════╝██╔════╝', Colors.BRIGHT_MAGENTA) + colorize('  ║', Colors.BRIGHT_CYAN))
        print(colorize('║  ', Colors.BRIGHT_CYAN) + colorize('   ██║      ╚████╔╝ ██████╔╝   ██████╔╝███████║███████╗███████╗', Colors.BRIGHT_MAGENTA) + colorize('  ║', Colors.BRIGHT_CYAN))
        print(colorize('║  ', Colors.BRIGHT_CYAN) + colorize('   ██║       ╚██╔╝  ██╔══██╗   ██╔═══╝ ██╔══██║╚════██║╚════██║', Colors.BRIGHT_MAGENTA) + colorize('  ║', Colors.BRIGHT_CYAN))
        print(colorize('║  ', Colors.BRIGHT_CYAN) + colorize('   ╚██████╗   ██║   ██████╔╝   ██║     ██║  ██║███████║███████║', Colors.BRIGHT_MAGENTA) + colorize('  ║', Colors.BRIGHT_CYAN))
        print(colorize('║  ', Colors.BRIGHT_CYAN) + colorize('    ╚═════╝   ╚═╝   ╚═════╝    ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝', Colors.BRIGHT_MAGENTA) + colorize('  ║', Colors.BRIGHT_CYAN))
        print(colorize('║                                                          ║', Colors.BRIGHT_CYAN))
        print(colorize('╚══════════════════════════════════════════════════════════╝', Colors.BRIGHT_CYAN))
        print()
        print(colorize('Advanced Password Generator', Colors.BRIGHT_GREEN))
        print(colorize('Interactive Personal Password Creation Tool', Colors.BRIGHT_YELLOW))
        print(colorize('=' * 60, Colors.BRIGHT_CYAN))
        print()
    
    def show_welcome_screen(self):
        """Show welcome screen with features explanation"""
        self.clear_screen()
        self.print_header()
        
        # Welcome message
        print(colorize('*** Welcome to CYB PASS! ***', Colors.BRIGHT_GREEN))
        print(colorize('=' * 50, Colors.BRIGHT_CYAN))
        print()
        
        # Features explanation
        print(colorize('What makes CYB PASS special:', Colors.BRIGHT_YELLOW))
        print()
        
        features = [
            ("[LOCK] Smart Password Generation", "Creates 25+ unique passwords from your personal info", Colors.BRIGHT_GREEN),
            ("[ART] Beautiful Interface", "Professional colored interface with ASCII art", Colors.BRIGHT_MAGENTA),
            ("[SPEED] Lightning Fast", "Generates passwords in seconds", Colors.BRIGHT_BLUE),
            ("[SHIELD] Security Focused", "Evaluates password strength automatically", Colors.BRIGHT_RED),
            ("[SAVE] Easy Export", "Save passwords to timestamped files", Colors.BRIGHT_CYAN),
            ("[GLOBE] Cross Platform", "Works on Windows, Linux, and macOS", Colors.BRIGHT_YELLOW),
            ("[TARGET] Personal Touch", "Uses your info to create memorable passwords", Colors.BRIGHT_WHITE),
            ("[REFRESH] Multiple Variations", "Creates different styles from same information", Colors.BRIGHT_GREEN)
        ]
        
        for i, (title, description, color) in enumerate(features, 1):
            print(f"  {colorize(f'{i:2d}.', Colors.BRIGHT_WHITE)} {colorize(title, color)}")
            print(f"     {colorize(description, Colors.WHITE)}")
            print()
        
        # Security tips
        print(colorize('[SHIELD] Security Tips:', Colors.BRIGHT_RED))
        print(colorize('   * Never share your passwords with anyone', Colors.WHITE))
        print(colorize('   * Use different passwords for each account', Colors.WHITE))
        print(colorize('   * Change passwords regularly', Colors.WHITE))
        print(colorize('   * Use two-factor authentication when possible', Colors.WHITE))
        print()
        
        # Version info
        print(colorize('[INFO] Version: 1.0.0 | Developer: CYB PASS Team', Colors.BRIGHT_YELLOW))
        print()
        
        # Continue prompt
        print(colorize('Press Enter to start using CYB PASS...', Colors.BRIGHT_CYAN))
        input()
    
    def get_user_input(self, question, input_type=str):
        """Get user input with type validation"""
        while True:
            try:
                colored_question = colorize(question, Colors.BRIGHT_WHITE)
                user_input = input(f"{colored_question}: ").strip()
                if not user_input:
                    print(colorize("[ERROR] Please enter a valid value", Colors.RED))
                    continue
                if input_type == int:
                    return int(user_input)
                return user_input
            except ValueError:
                print(colorize("[ERROR] Please enter a valid number", Colors.RED))
            except KeyboardInterrupt:
                print(f"\n\n{colorize('Operation cancelled. Goodbye!', Colors.YELLOW)}")
                sys.exit(0)
    
    def ask_questions(self):
        """Ask interactive questions to the user"""
        print(colorize("[INFO] Let's get to know you first to create personalized passwords...", Colors.BRIGHT_CYAN))
        print()
        
        # Ask for number of passwords to generate
        print(colorize("[COUNT] How many passwords would you like to generate?", Colors.BRIGHT_MAGENTA))
        print(colorize("[INFO] You can generate any number of passwords (minimum 1)", Colors.BRIGHT_CYAN))
        self.user_info['password_count'] = self.get_user_input("Enter number of passwords (1 or more)", int)
        
        # Validate password count
        if self.user_info['password_count'] < 1:
            self.user_info['password_count'] = 1
            print(colorize("[INFO] Minimum 1 password will be generated", Colors.YELLOW))
        
        # Show warning for very large numbers
        if self.user_info['password_count'] > 1000:
            print(colorize("[WARNING] Large number detected! This may take some time...", Colors.YELLOW))
            confirm = input(colorize("Continue? (y/n): ", Colors.BRIGHT_WHITE)).lower()
            if confirm not in ['y', 'yes', 'نعم', 'ن']:
                self.user_info['password_count'] = 100
                print(colorize("[INFO] Set to 100 passwords", Colors.GREEN))
        
        print()
        
        # Personal information
        print(colorize("[COLLECT] Personal Information Collection", Colors.BRIGHT_YELLOW))
        print(colorize("-" * 40, Colors.BRIGHT_YELLOW))
        
        # Basic information
        self.user_info['name'] = self.get_user_input("[NAME] What's your full name?")
        self.user_info['nickname'] = self.get_user_input("[NICKNAME] What's your nickname or preferred name?")
        
        # Detailed birthday information
        print(colorize("\n[BIRTHDAY] Let's get your complete birthday:", Colors.BRIGHT_CYAN))
        self.user_info['birth_year'] = self.get_user_input("[YEAR] What year were you born?", int)
        self.user_info['birth_month'] = self.get_user_input("[MONTH] What month were you born? (1-12)", int)
        self.user_info['birth_day'] = self.get_user_input("[DAY] What day were you born? (1-31)", int)
        
        # Validate birthday
        if not (1 <= self.user_info['birth_month'] <= 12):
            self.user_info['birth_month'] = 1
            print(colorize("[WARNING] Invalid month, using January (1)", Colors.YELLOW))
        if not (1 <= self.user_info['birth_day'] <= 31):
            self.user_info['birth_day'] = 1
            print(colorize("[WARNING] Invalid day, using 1st", Colors.YELLOW))
        
        # Personal preferences
        self.user_info['favorite_color'] = self.get_user_input("[COLOR] What's your favorite color?")
        self.user_info['favorite_animal'] = self.get_user_input("[ANIMAL] What's your favorite animal?")
        self.user_info['hobby'] = self.get_user_input("[HOBBY] What's your favorite hobby?")
        self.user_info['favorite_number'] = self.get_user_input("[NUMBER] What's your favorite number?", int)
        
        # Location information
        self.user_info['city'] = self.get_user_input("[CITY] What city do you live in?")
        self.user_info['country'] = self.get_user_input("[COUNTRY] What country are you from?")
        
        # Additional personal information
        self.user_info['favorite_food'] = self.get_user_input("[FOOD] What's your favorite food?")
        self.user_info['favorite_sport'] = self.get_user_input("[SPORT] What's your favorite sport?")
        self.user_info['favorite_movie'] = self.get_user_input("[MOVIE] What's your favorite movie or TV show?")
        self.user_info['favorite_music'] = self.get_user_input("[MUSIC] What's your favorite music genre or artist?")
        self.user_info['profession'] = self.get_user_input("[JOB] What's your profession or field of work?")
        self.user_info['favorite_season'] = self.get_user_input("[SEASON] What's your favorite season?")
        
        # Pet information
        self.user_info['pet_name'] = self.get_user_input("[PET] Do you have a pet? What's its name? (or type 'none')")
        if self.user_info['pet_name'].lower() == 'none':
            self.user_info['pet_name'] = ""
        
        print()
        print(colorize("[SUCCESS] Your information has been saved successfully!", Colors.BRIGHT_GREEN))
        print(colorize(f"[INFO] Will generate {self.user_info['password_count']} passwords for you", Colors.BRIGHT_CYAN))
        print()
    
    def generate_password_variations(self, base_info, length=12):
        """Generate different password variations"""
        variations = []
        
        # Remove spaces and convert to lowercase
        clean_info = base_info.replace(" ", "").lower()
        
        # Get birthday components
        birth_year = str(self.user_info['birth_year'])
        birth_month = str(self.user_info['birth_month']).zfill(2)
        birth_day = str(self.user_info['birth_day']).zfill(2)
        favorite_number = str(self.user_info['favorite_number'])
        
        # Variation 1: Info + random numbers
        random_nums = ''.join(random.choices(string.digits, k=4))
        variation1 = clean_info + random_nums
        if len(variation1) < length:
            variation1 += ''.join(random.choices(string.ascii_letters + string.digits, k=length-len(variation1)))
        variations.append(variation1[:length])
        
        # Variation 2: Info + special characters + favorite number
        special_chars = ''.join(random.choices("!@#$%^&*", k=2))
        variation2 = clean_info + special_chars + favorite_number
        if len(variation2) < length:
            variation2 += ''.join(random.choices(string.ascii_letters, k=length-len(variation2)))
        variations.append(variation2[:length])
        
        # Variation 3: Mixed info with birth year
        variation3 = clean_info[:3] + birth_year + clean_info[3:] + ''.join(random.choices(string.ascii_letters, k=2))
        if len(variation3) < length:
            variation3 += ''.join(random.choices(string.digits, k=length-len(variation3)))
        variations.append(variation3[:length])
        
        # Variation 4: Info with alternating case
        mixed_info = ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(clean_info)])
        variation4 = mixed_info + ''.join(random.choices(string.digits + "!@#", k=length-len(mixed_info)))
        variations.append(variation4[:length])
        
        # Variation 5: Info with numbers in the middle
        mid_point = len(clean_info) // 2
        variation5 = clean_info[:mid_point] + favorite_number + clean_info[mid_point:]
        if len(variation5) < length:
            variation5 += ''.join(random.choices(string.ascii_letters + string.digits, k=length-len(variation5)))
        variations.append(variation5[:length])
        
        # Variation 6: Info + birth month and day
        variation6 = clean_info + birth_month + birth_day + ''.join(random.choices(string.ascii_letters, k=2))
        if len(variation6) < length:
            variation6 += ''.join(random.choices(string.digits + "!@#", k=length-len(variation6)))
        variations.append(variation6[:length])
        
        # Variation 7: Info with birth year at the end
        variation7 = clean_info + birth_year[-2:] + ''.join(random.choices(string.ascii_letters, k=2))
        if len(variation7) < length:
            variation7 += ''.join(random.choices(string.digits + "!@#$%", k=length-len(variation7)))
        variations.append(variation7[:length])
        
        # Variation 8: Info with special pattern
        variation8 = clean_info[:2] + birth_month + clean_info[2:4] + birth_day + clean_info[4:]
        if len(variation8) < length:
            variation8 += ''.join(random.choices(string.ascii_letters + string.digits + "!@#", k=length-len(variation8)))
        variations.append(variation8[:length])
        
        return variations
    
    def generate_random_enhanced_password(self, length):
        """Generate a completely random password with enhanced security"""
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one character from each set
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special_chars)
        ]
        
        # Fill the rest with random characters
        all_chars = lowercase + uppercase + digits + special_chars
        for _ in range(length - 4):
            password.append(random.choice(all_chars))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        
        return ''.join(password)
    
    def generate_passwords(self):
        """Generate password list with professional progress tracking"""
        print(colorize("[*] Generating passwords...", Colors.BRIGHT_BLUE))
        print()
        
        # Generate passwords from each piece of information
        info_list = [
            self.user_info['name'],
            self.user_info['nickname'],
            self.user_info['favorite_color'],
            self.user_info['favorite_animal'],
            self.user_info['hobby'],
            self.user_info['city'],
            self.user_info['country'],
            self.user_info['favorite_food'],
            self.user_info['favorite_sport'],
            self.user_info['favorite_movie'],
            self.user_info['favorite_music'],
            self.user_info['profession'],
            self.user_info['favorite_season'],
            self.user_info['pet_name']
        ]
        
        # Filter out empty values
        info_list = [info for info in info_list if info and info.strip()]
        
        # Create progress bar
        total_steps = len(info_list) + 4  # info processing + combined + birthday + final processing
        progress = ProgressBar(total_steps)
        
        print(colorize("[*] Processing personal information...", Colors.YELLOW))
        for i, info in enumerate(info_list, 1):
            progress.update(i, f"Processing: {info[:20]}...")
            time.sleep(0.1)  # Simulate processing time
            variations = self.generate_password_variations(info)
            self.passwords.extend(variations)
        
        progress.update(len(info_list) + 1, "Creating combined variations...")
        time.sleep(0.2)
        # Add combined passwords with different combinations
        for i in range(0, len(info_list), 3):
            combined_info = ''.join([info.replace(" ", "").lower() for info in info_list[i:i+3]])
            if combined_info:
                combined_variations = self.generate_password_variations(combined_info, 16)
                self.passwords.extend(combined_variations)
        
        # Add birthday-based combinations
        progress.update(len(info_list) + 2, "Creating birthday-based variations...")
        time.sleep(0.2)
        birthday_combos = [
            f"{self.user_info['name']}{self.user_info['birth_year']}",
            f"{self.user_info['favorite_color']}{self.user_info['birth_month']}{self.user_info['birth_day']}",
            f"{self.user_info['hobby']}{self.user_info['birth_year']}{self.user_info['favorite_number']}",
            f"{self.user_info['city']}{self.user_info['birth_day']}{self.user_info['birth_month']}"
        ]
        
        for combo in birthday_combos:
            if combo:
                variations = self.generate_password_variations(combo, 14)
                self.passwords.extend(variations)
        
        progress.update(len(info_list) + 3, "Removing duplicates and analyzing...")
        time.sleep(0.3)
        # Remove duplicates
        self.passwords = list(set(self.passwords))
        
        # Random shuffle
        random.shuffle(self.passwords)
        
        # Limit to requested number
        requested_count = self.user_info.get('password_count', 25)
        
        if len(self.passwords) > requested_count:
            self.passwords = self.passwords[:requested_count]
        elif len(self.passwords) < requested_count:
            # Generate additional passwords if we don't have enough
            print(colorize(f"[*] Generating additional passwords to reach {requested_count}...", Colors.YELLOW))
            
            # Create a more efficient generation process for large numbers
            batch_size = min(100, requested_count - len(self.passwords))
            generated_count = len(self.passwords)
            
            while generated_count < requested_count:
                # Generate a batch of passwords
                batch_passwords = []
                for _ in range(batch_size):
                    if generated_count >= requested_count:
                        break
                    
                    # Use different strategies to generate unique passwords
                    strategy = random.choice(['info_based', 'random_enhanced', 'combined_enhanced'])
                    
                    if strategy == 'info_based':
                        random_info = random.choice(info_list)
                        variations = self.generate_password_variations(random_info, random.randint(10, 18))
                        batch_passwords.extend(variations)
                    elif strategy == 'random_enhanced':
                        # Generate completely random passwords with personal touch
                        base_length = random.randint(12, 20)
                        random_pwd = self.generate_random_enhanced_password(base_length)
                        batch_passwords.append(random_pwd)
                    else:  # combined_enhanced
                        # Combine multiple info pieces
                        combined_info = ''.join(random.sample(info_list, min(3, len(info_list))))
                        variations = self.generate_password_variations(combined_info, random.randint(14, 20))
                        batch_passwords.extend(variations)
                    
                    generated_count += 1
                
                # Add batch to main list
                self.passwords.extend(batch_passwords)
                
                # Remove duplicates
                self.passwords = list(set(self.passwords))
                generated_count = len(self.passwords)
                
                # Update progress for large numbers
                if requested_count > 100:
                    progress_percent = (generated_count / requested_count) * 100
                    print(f"\r{colorize(f'Progress: {generated_count}/{requested_count} ({progress_percent:.1f}%)', Colors.BRIGHT_CYAN)}", end="", flush=True)
                
                # Break if we have enough
                if generated_count >= requested_count:
                    break
            
            # Final limit to exact requested count
            self.passwords = self.passwords[:requested_count]
            
            if requested_count > 100:
                print()  # New line after progress
        
        progress.complete("Password generation completed!")
        print()
    
    def display_passwords(self):
        """Display generated passwords with advanced analysis"""
        print(colorize(f"[SUCCESS] Generated {len(self.passwords)} unique passwords!", Colors.BRIGHT_GREEN))
        print(colorize("=" * 80, Colors.BRIGHT_CYAN))
        print()
        
        # For large numbers, show only first 50 and last 10 passwords
        if len(self.passwords) > 100:
            print(colorize(f"[INFO] Showing first 50 and last 10 passwords (total: {len(self.passwords)})", Colors.BRIGHT_YELLOW))
            print()
            
            # Show first 50 passwords
            print(colorize("[FIRST 50] Passwords 1-50:", Colors.BRIGHT_MAGENTA))
            print("-" * 50)
            for i, password in enumerate(self.passwords[:50], 1):
                analysis = self.analyzer.analyze_strength(password)
                strength_level, strength_color = self.analyzer.get_strength_level(analysis['score'])
                
                print(f"{colorize(f'{i:2d}.', Colors.BRIGHT_WHITE)} {colorize(password, Colors.BRIGHT_CYAN)}")
                print(f"    {colorize('Strength:', Colors.WHITE)} {colorize(strength_level, strength_color)} "
                      f"{colorize(f'(Score: {analysis['score']}/8)', Colors.YELLOW)}")
                print()
            
            # Show last 10 passwords
            print(colorize(f"[LAST 10] Passwords {len(self.passwords)-9}-{len(self.passwords)}:", Colors.BRIGHT_MAGENTA))
            print("-" * 50)
            for i, password in enumerate(self.passwords[-10:], len(self.passwords)-9):
                analysis = self.analyzer.analyze_strength(password)
                strength_level, strength_color = self.analyzer.get_strength_level(analysis['score'])
                
                print(f"{colorize(f'{i:2d}.', Colors.BRIGHT_WHITE)} {colorize(password, Colors.BRIGHT_CYAN)}")
                print(f"    {colorize('Strength:', Colors.WHITE)} {colorize(strength_level, strength_color)} "
                      f"{colorize(f'(Score: {analysis['score']}/8)', Colors.YELLOW)}")
                print()
        else:
            # For smaller numbers, show all passwords with full analysis
            analyzed_passwords = []
            for password in self.passwords:
                analysis = self.analyzer.analyze_strength(password)
                strength_level, strength_color = self.analyzer.get_strength_level(analysis['score'])
                analyzed_passwords.append({
                    'password': password,
                    'analysis': analysis,
                    'strength_level': strength_level,
                    'strength_color': strength_color
                })
            
            # Display passwords with detailed analysis
            for i, pwd_data in enumerate(analyzed_passwords, 1):
                password = pwd_data['password']
                analysis = pwd_data['analysis']
                strength_level = pwd_data['strength_level']
                strength_color = pwd_data['strength_color']
                
                print(f"{colorize(f'{i:2d}.', Colors.BRIGHT_WHITE)} {colorize(password, Colors.BRIGHT_CYAN)}")
                print(f"    {colorize('Strength:', Colors.WHITE)} {colorize(strength_level, strength_color)} "
                      f"{colorize(f'(Score: {analysis['score']}/8)', Colors.YELLOW)}")
                print(f"    {colorize('Length:', Colors.WHITE)} {analysis['length']} chars | "
                      f"{colorize('Entropy:', Colors.WHITE)} {analysis['entropy']:.1f}")
                
                if analysis['recommendations']:
                    print(f"    {colorize('Tips:', Colors.YELLOW)} {', '.join(analysis['recommendations'][:2])}")
                print()
        
        # Always show statistics
        self.display_password_statistics_simple()
        print(colorize("=" * 80, Colors.BRIGHT_CYAN))
    
    def display_password_statistics(self, analyzed_passwords):
        """Display password generation statistics"""
        print(colorize("[STATISTICS] Password Analysis Summary:", Colors.BRIGHT_MAGENTA))
        print()
        
        # Count by strength level
        strength_counts = {}
        total_entropy = 0
        total_length = 0
        
        for pwd_data in analyzed_passwords:
            strength = pwd_data['strength_level']
            strength_counts[strength] = strength_counts.get(strength, 0) + 1
            total_entropy += pwd_data['analysis']['entropy']
            total_length += pwd_data['analysis']['length']
        
        # Display strength distribution
        for strength, count in strength_counts.items():
            percentage = (count / len(analyzed_passwords)) * 100
            color = Colors.RED if strength == "Weak" else Colors.YELLOW if strength == "Medium" else Colors.BRIGHT_GREEN
            print(f"  {colorize(strength, color)}: {count} passwords ({percentage:.1f}%)")
        
        # Display averages
        avg_entropy = total_entropy / len(analyzed_passwords)
        avg_length = total_length / len(analyzed_passwords)
        
        print(f"  {colorize('Average Length:', Colors.WHITE)} {avg_length:.1f} characters")
        print(f"  {colorize('Average Entropy:', Colors.WHITE)} {avg_entropy:.1f}")
        print()
    
    def display_password_statistics_simple(self):
        """Display simplified password statistics for large numbers"""
        print(colorize("[STATISTICS] Password Analysis Summary:", Colors.BRIGHT_MAGENTA))
        print()
        
        # Sample analysis for large numbers (first 100 passwords)
        sample_size = min(100, len(self.passwords))
        sample_passwords = self.passwords[:sample_size]
        
        # Calculate statistics
        total_score = 0
        total_length = 0
        total_entropy = 0
        strength_counts = {'Weak': 0, 'Medium': 0, 'Strong': 0, 'Very Strong': 0}
        
        for password in sample_passwords:
            analysis = self.analyzer.analyze_strength(password)
            strength_level, _ = self.analyzer.get_strength_level(analysis['score'])
            strength_counts[strength_level] += 1
            total_score += analysis['score']
            total_length += analysis['length']
            total_entropy += analysis['entropy']
        
        # Display statistics
        print(f"  {colorize('Total Passwords:', Colors.WHITE)} {len(self.passwords)}")
        print(f"  {colorize('Sample Analyzed:', Colors.WHITE)} {sample_size}")
        print(f"  {colorize('Average Score:', Colors.WHITE)} {total_score/sample_size:.1f}/8")
        print(f"  {colorize('Average Length:', Colors.WHITE)} {total_length/sample_size:.1f} characters")
        print(f"  {colorize('Average Entropy:', Colors.WHITE)} {total_entropy/sample_size:.1f}")
        print()
        
        print(colorize("[DISTRIBUTION] Strength Distribution (sample):", Colors.BRIGHT_YELLOW))
        for level, count in strength_counts.items():
            percentage = (count / sample_size) * 100
            color = Colors.RED if level == "Weak" else Colors.YELLOW if level == "Medium" else Colors.BRIGHT_GREEN
            print(f"  {colorize(level, color)}: {count} passwords ({percentage:.1f}%)")
        print()
    
    def calculate_strength(self, password):
        """Calculate password strength"""
        score = 0
        if len(password) >= 8:
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        
        if score <= 2:
            return "[Weak]"
        elif score <= 4:
            return "[Medium]"
        else:
            return "[Strong]"
    
    def save_to_file(self):
        """Save passwords to file with multiple format options"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(colorize("[SAVE] Choose export format:", Colors.BRIGHT_WHITE))
        print()
        print(colorize("1. [TXT] Text file (Simple)", Colors.BRIGHT_GREEN))
        print(colorize("2. [JSON] JSON file (Structured data)", Colors.BRIGHT_BLUE))
        print(colorize("3. [CSV] CSV file (Spreadsheet compatible)", Colors.BRIGHT_YELLOW))
        print(colorize("4. [ALL] All formats", Colors.BRIGHT_MAGENTA))
        print()
        
        choice = self.get_user_input("Select format (1-4)", int)
        
        # Prepare password data with analysis
        password_data = []
        for password in self.passwords:
            analysis = self.analyzer.analyze_strength(password)
            strength_level, _ = self.analyzer.get_strength_level(analysis['score'])
            password_data.append({
                'password': password,
                'strength': strength_level,
                'length': analysis['length'],
                'entropy': analysis['entropy'],
                'score': analysis['score']
            })
        
        saved_files = []
        
        if choice in [1, 4]:  # TXT format
            filename = f"cybpass_passwords_{timestamp}.txt"
            if self.save_txt_file(filename, password_data):
                saved_files.append(filename)
        
        if choice in [2, 4]:  # JSON format
            filename = f"cybpass_passwords_{timestamp}.json"
            if self.file_manager.save_passwords_json(password_data, filename, self.user_info):
                saved_files.append(filename)
        
        if choice in [3, 4]:  # CSV format
            filename = f"cybpass_passwords_{timestamp}.csv"
            if self.file_manager.save_passwords_csv(password_data, filename):
                saved_files.append(filename)
        
        if saved_files:
            print(colorize(f"[SUCCESS] Files saved successfully!", Colors.BRIGHT_GREEN))
            for filename in saved_files:
                print(colorize(f"  ✓ {filename}", Colors.CYAN))
            return saved_files
        else:
            print(colorize("[ERROR] Failed to save files", Colors.RED))
            return None
    
    def save_txt_file(self, filename, password_data):
        """Save passwords to text file - passwords only"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("CYB PASS - Professional Password Generator\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total passwords: {len(password_data)}\n")
                f.write(f"User: {self.user_info.get('name', 'Unknown')}\n\n")
                
                f.write("PASSWORD LIST:\n")
                f.write("-" * 30 + "\n")
                
                for pwd_data in password_data:
                    f.write(f"{pwd_data['password']}\n")
                
                f.write("\nSECURITY RECOMMENDATIONS:\n")
                f.write("-" * 30 + "\n")
                f.write("• Use different passwords for each account\n")
                f.write("• Change passwords regularly (every 3-6 months)\n")
                f.write("• Enable two-factor authentication when possible\n")
                f.write("• Never share passwords with anyone\n")
                f.write("• Use a password manager for better security\n")
            
            return True
        except Exception as e:
            print(colorize(f"[ERROR] Failed to save TXT: {e}", Colors.RED))
            return False
    
    def show_menu(self):
        """Display main menu"""
        # Show header and menu once at the beginning
        self.print_header()
        self.display_command_list()
        
        while True:
            choice = self.get_user_input("Select option (1-8)", int)
            
            if choice == 1:
                self.ask_questions()
                self.generate_passwords()
                print()
                self.display_command_list()
            elif choice == 2:
                if self.passwords:
                    self.display_passwords()
                    print()
                    self.display_command_list()
                else:
                    print(colorize("[WARNING] No passwords available. Please generate new passwords first.", Colors.YELLOW))
                    print()
                    self.display_command_list()
            elif choice == 3:
                if self.passwords:
                    filename = self.save_to_file()
                    if filename:
                        print()
                        self.display_command_list()
                else:
                    print(colorize("[WARNING] No passwords to save.", Colors.YELLOW))
                    print()
                    self.display_command_list()
            elif choice == 4:
                self.analyze_passwords()
                print()
                self.display_command_list()
            elif choice == 5:
                self.show_password_categories()
                print()
                self.display_command_list()
            elif choice == 6:
                self.show_settings()
                print()
                self.display_command_list()
            elif choice == 7:
                self.show_info()
                print()
                self.display_command_list()
            elif choice == 8:
                print(colorize("\n[GOODBYE] Thank you for using CYB PASS! Goodbye!", Colors.BRIGHT_GREEN))
                break
            else:
                print(colorize("[ERROR] Invalid choice. Please try again.", Colors.RED))
                print()
                self.display_command_list()
    
    def display_command_list(self):
        """Display the command list"""
        print(colorize("[MENU] Choose from the menu:", Colors.BRIGHT_WHITE))
        print()
        print(colorize("1. [GENERATE] Generate new passwords", Colors.BRIGHT_GREEN))
        print(colorize("2. [DISPLAY] Display current passwords", Colors.BRIGHT_BLUE))
        print(colorize("3. [SAVE] Save passwords to file", Colors.BRIGHT_YELLOW))
        print(colorize("4. [ANALYZE] Analyze password strength", Colors.BRIGHT_CYAN))
        print(colorize("5. [CATEGORIES] Password categories", Colors.BRIGHT_MAGENTA))
        print(colorize("6. [SETTINGS] Configuration options", Colors.BRIGHT_WHITE))
        print(colorize("7. [ABOUT] About CYB PASS", Colors.BRIGHT_MAGENTA))
        print(colorize("8. [EXIT] Exit", Colors.RED))
        print()
    
    def analyze_passwords(self):
        """Advanced password analysis"""
        if not self.passwords:
            print(colorize("[WARNING] No passwords to analyze. Please generate passwords first.", Colors.YELLOW))
            return
        
        print(colorize("[ANALYZE] Advanced Password Analysis", Colors.BRIGHT_CYAN))
        print(colorize("=" * 50, Colors.BRIGHT_CYAN))
        print()
        
        # Analyze all passwords
        analyses = []
        for password in self.passwords:
            analysis = self.analyzer.analyze_strength(password)
            analyses.append(analysis)
        
        # Calculate overall statistics
        total_score = sum(a['score'] for a in analyses)
        avg_score = total_score / len(analyses)
        avg_length = sum(a['length'] for a in analyses) / len(analyses)
        avg_entropy = sum(a['entropy'] for a in analyses) / len(analyses)
        
        # Count by strength levels
        strength_counts = {'Weak': 0, 'Medium': 0, 'Strong': 0, 'Very Strong': 0}
        for analysis in analyses:
            level, _ = self.analyzer.get_strength_level(analysis['score'])
            strength_counts[level] += 1
        
        print(colorize("[STATISTICS] Overall Analysis:", Colors.BRIGHT_MAGENTA))
        print(f"  Total Passwords: {len(self.passwords)}")
        print(f"  Average Score: {avg_score:.1f}/8")
        print(f"  Average Length: {avg_length:.1f} characters")
        print(f"  Average Entropy: {avg_entropy:.1f}")
        print()
        
        print(colorize("[DISTRIBUTION] Strength Distribution:", Colors.BRIGHT_YELLOW))
        for level, count in strength_counts.items():
            percentage = (count / len(analyses)) * 100
            color = Colors.RED if level == "Weak" else Colors.YELLOW if level == "Medium" else Colors.BRIGHT_GREEN
            print(f"  {colorize(level, color)}: {count} passwords ({percentage:.1f}%)")
        print()
        
        # Show weakest and strongest passwords
        weakest = min(analyses, key=lambda x: x['score'])
        strongest = max(analyses, key=lambda x: x['score'])
        
        print(colorize("[WEAKEST] Weakest Password:", Colors.RED))
        weak_pwd = self.passwords[analyses.index(weakest)]
        print(f"  Password: {weak_pwd}")
        print(f"  Score: {weakest['score']}/8")
        print(f"  Recommendations: {', '.join(weakest['recommendations'][:3])}")
        print()
        
        print(colorize("[STRONGEST] Strongest Password:", Colors.BRIGHT_GREEN))
        strong_pwd = self.passwords[analyses.index(strongest)]
        print(f"  Password: {strong_pwd}")
        print(f"  Score: {strongest['score']}/8")
        print(f"  Entropy: {strongest['entropy']:.1f}")
        print()
    
    def show_password_categories(self):
        """Display password categories and recommendations"""
        print(colorize("[CATEGORIES] Password Categories & Recommendations", Colors.BRIGHT_MAGENTA))
        print(colorize("=" * 60, Colors.BRIGHT_MAGENTA))
        print()
        
        for category, description in self.password_categories.items():
            print(colorize(f"[{category.upper()}] {description}", Colors.BRIGHT_CYAN))
            
            if category == 'banking':
                print(colorize("  • Use strongest passwords (16+ characters)", Colors.WHITE))
                print(colorize("  • Include special characters and numbers", Colors.WHITE))
                print(colorize("  • Change every 3 months", Colors.WHITE))
            elif category == 'email':
                print(colorize("  • Use unique, strong passwords", Colors.WHITE))
                print(colorize("  • Enable 2FA if available", Colors.WHITE))
                print(colorize("  • Change every 6 months", Colors.WHITE))
            elif category == 'social':
                print(colorize("  • Use medium to strong passwords", Colors.WHITE))
                print(colorize("  • Avoid personal information", Colors.WHITE))
                print(colorize("  • Change every 6 months", Colors.WHITE))
            elif category == 'work':
                print(colorize("  • Follow company password policy", Colors.WHITE))
                print(colorize("  • Use strong, unique passwords", Colors.WHITE))
                print(colorize("  • Change as required by policy", Colors.WHITE))
            elif category == 'gaming':
                print(colorize("  • Use medium strength passwords", Colors.WHITE))
                print(colorize("  • Consider 2FA for valuable accounts", Colors.WHITE))
                print(colorize("  • Change every 12 months", Colors.WHITE))
            elif category == 'shopping':
                print(colorize("  • Use strong passwords", Colors.WHITE))
                print(colorize("  • Enable 2FA for payment accounts", Colors.WHITE))
                print(colorize("  • Change every 6 months", Colors.WHITE))
            else:  # general
                print(colorize("  • Use medium to strong passwords", Colors.WHITE))
                print(colorize("  • Make them memorable but secure", Colors.WHITE))
                print(colorize("  • Change every 12 months", Colors.WHITE))
            print()
    
    def show_settings(self):
        """Display configuration settings"""
        print(colorize("[SETTINGS] Configuration Options", Colors.BRIGHT_WHITE))
        print(colorize("=" * 40, Colors.BRIGHT_WHITE))
        print()
        
        print(colorize("[CURRENT] Current Settings:", Colors.BRIGHT_CYAN))
        print(f"  Password Count: {self.user_info.get('password_count', 25)}")
        print(f"  Default Length: 12-16 characters")
        print(f"  Character Sets: Letters, Numbers, Special chars")
        print(f"  Analysis Level: Advanced")
        print()
        
        print(colorize("[CUSTOMIZATION] Available Options:", Colors.BRIGHT_YELLOW))
        print("  • Password length range")
        print("  • Character set preferences")
        print("  • Special character requirements")
        print("  • Analysis depth level")
        print("  • Export format preferences")
        print()
        
        print(colorize("[INFO] Settings are automatically optimized for security", Colors.BRIGHT_GREEN))
        print(colorize("For advanced customization, edit the configuration file", Colors.WHITE))
    
    def show_info(self):
        """Display tool information"""
        print(colorize("[ABOUT] About CYB PASS Professional", Colors.BRIGHT_MAGENTA))
        print(colorize("=" * 50, Colors.BRIGHT_MAGENTA))
        print()
        print(colorize("[FEATURES] Professional Features:", Colors.BRIGHT_CYAN))
        print(colorize("  * Advanced password strength analysis", Colors.WHITE))
        print(colorize("  * Multiple export formats (TXT, JSON, CSV)", Colors.WHITE))
        print(colorize("  * Real-time progress tracking", Colors.WHITE))
        print(colorize("  * Password categorization system", Colors.WHITE))
        print(colorize("  * Comprehensive security recommendations", Colors.WHITE))
        print(colorize("  * Professional statistics and reporting", Colors.WHITE))
        print(colorize("  * Cross-platform compatibility", Colors.WHITE))
        print()
        print(colorize("[SECURITY] Security Features:", Colors.BRIGHT_RED))
        print(colorize("  * Entropy calculation for password strength", Colors.WHITE))
        print(colorize("  * Pattern detection and warnings", Colors.WHITE))
        print(colorize("  * Secure file encryption options", Colors.WHITE))
        print(colorize("  * No data collection or transmission", Colors.WHITE))
        print()
        print(colorize("[VERSION] Version: 2.0.0 Professional", Colors.BRIGHT_YELLOW))
        print(colorize("[DEVELOPER] Developer: CYB PASS Team", Colors.BRIGHT_YELLOW))
        print(colorize("[LICENSE] Open Source - MIT License", Colors.BRIGHT_YELLOW))

def main():
    """Main function"""
    try:
        generator = PasswordGenerator()
        generator.show_welcome_screen()  # Show welcome screen first
        generator.show_menu()
    except KeyboardInterrupt:
        print(f"\n\n{colorize('Operation cancelled. Goodbye!', Colors.YELLOW)}")
    except Exception as e:
        print(f"\n{colorize('Unexpected error occurred:', Colors.RED)} {colorize(str(e), Colors.BRIGHT_RED)}")
        input(colorize("\nPress Enter to exit...", Colors.CYAN))

if __name__ == "__main__":
    main()
