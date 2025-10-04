#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CybPss - Interactive Password Generator Tool
Advanced Password Generator with Personal Information Integration
"""

import random
import string
import sys
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self):
        self.passwords = []
        self.user_info = {}
        
    def clear_screen(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print tool header"""
        print("=" * 60)
        print("CybPss - Advanced Password Generator")
        print("Interactive Personal Password Creation Tool")
        print("=" * 60)
        print()
    
    def get_user_input(self, question, input_type=str):
        """Get user input with type validation"""
        while True:
            try:
                user_input = input(f"{question}: ").strip()
                if not user_input:
                    print("Error: Please enter a valid value")
                    continue
                if input_type == int:
                    return int(user_input)
                return user_input
            except ValueError:
                print("Error: Please enter a valid number")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled. Goodbye!")
                sys.exit(0)
    
    def ask_questions(self):
        """Ask interactive questions to the user"""
        print("Let's get to know you first to create personalized passwords...")
        print()
        
        # Personal information
        self.user_info['name'] = self.get_user_input("What's your name?")
        self.user_info['birth_year'] = self.get_user_input("What year were you born?", int)
        self.user_info['favorite_color'] = self.get_user_input("What's your favorite color?")
        self.user_info['favorite_animal'] = self.get_user_input("What's your favorite animal?")
        self.user_info['hobby'] = self.get_user_input("What's your favorite hobby?")
        self.user_info['favorite_number'] = self.get_user_input("What's your favorite number?", int)
        self.user_info['city'] = self.get_user_input("What city do you live in?")
        
        print()
        print("Your information has been saved successfully!")
        print()
    
    def generate_password_variations(self, base_info, length=12):
        """Generate different password variations"""
        variations = []
        
        # Remove spaces and convert to lowercase
        clean_info = base_info.replace(" ", "").lower()
        
        # Variation 1: Info + random numbers
        random_nums = ''.join(random.choices(string.digits, k=4))
        variation1 = clean_info + random_nums
        if len(variation1) < length:
            variation1 += ''.join(random.choices(string.ascii_letters + string.digits, k=length-len(variation1)))
        variations.append(variation1[:length])
        
        # Variation 2: Info + special characters
        special_chars = ''.join(random.choices("!@#$%^&*", k=2))
        variation2 = clean_info + special_chars + str(self.user_info['favorite_number'])
        if len(variation2) < length:
            variation2 += ''.join(random.choices(string.ascii_letters, k=length-len(variation2)))
        variations.append(variation2[:length])
        
        # Variation 3: Mixed info with birth year
        year_str = str(self.user_info['birth_year'])
        variation3 = clean_info[:3] + year_str + clean_info[3:] + ''.join(random.choices(string.ascii_letters, k=2))
        if len(variation3) < length:
            variation3 += ''.join(random.choices(string.digits, k=length-len(variation3)))
        variations.append(variation3[:length])
        
        # Variation 4: Info with alternating case
        mixed_info = ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(clean_info)])
        variation4 = mixed_info + ''.join(random.choices(string.digits + "!@#", k=length-len(mixed_info)))
        variations.append(variation4[:length])
        
        # Variation 5: Info with numbers in the middle
        mid_point = len(clean_info) // 2
        variation5 = clean_info[:mid_point] + str(self.user_info['favorite_number']) + clean_info[mid_point:]
        if len(variation5) < length:
            variation5 += ''.join(random.choices(string.ascii_letters + string.digits, k=length-len(variation5)))
        variations.append(variation5[:length])
        
        return variations
    
    def generate_passwords(self):
        """Generate password list"""
        print("Generating passwords...")
        print()
        
        # Generate passwords from each piece of information
        info_list = [
            self.user_info['name'],
            self.user_info['favorite_color'],
            self.user_info['favorite_animal'],
            self.user_info['hobby'],
            self.user_info['city']
        ]
        
        for info in info_list:
            variations = self.generate_password_variations(info)
            self.passwords.extend(variations)
        
        # Add combined passwords
        combined_info = ''.join([info.replace(" ", "").lower() for info in info_list])
        combined_variations = self.generate_password_variations(combined_info, 16)
        self.passwords.extend(combined_variations)
        
        # Remove duplicates
        self.passwords = list(set(self.passwords))
        
        # Random shuffle
        random.shuffle(self.passwords)
    
    def display_passwords(self):
        """Display generated passwords"""
        print(f"Generated {len(self.passwords)} unique passwords!")
        print("=" * 60)
        print()
        
        for i, password in enumerate(self.passwords, 1):
            strength = self.calculate_strength(password)
            print(f"{i:2d}. {password} {strength}")
        
        print()
        print("=" * 60)
    
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
        """Save passwords to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cybpss_passwords_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("CybPss Generated Passwords\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total passwords: {len(self.passwords)}\n\n")
                
                for i, password in enumerate(self.passwords, 1):
                    strength = self.calculate_strength(password)
                    f.write(f"{i:2d}. {password} {strength}\n")
            
            print(f"Passwords saved to file: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    def show_menu(self):
        """Display main menu"""
        while True:
            self.clear_screen()
            self.print_header()
            
            print("Choose from the menu:")
            print("1. Generate new passwords")
            print("2. Display current passwords")
            print("3. Save passwords to file")
            print("4. About CybPss")
            print("5. Exit")
            print()
            
            choice = self.get_user_input("Select option (1-5)", int)
            
            if choice == 1:
                self.ask_questions()
                self.generate_passwords()
                input("\nPress Enter to continue...")
            elif choice == 2:
                if self.passwords:
                    self.display_passwords()
                    input("\nPress Enter to continue...")
                else:
                    print("No passwords available. Please generate new passwords first.")
                    input("\nPress Enter to continue...")
            elif choice == 3:
                if self.passwords:
                    filename = self.save_to_file()
                    if filename:
                        input("\nPress Enter to continue...")
                else:
                    print("No passwords to save.")
                    input("\nPress Enter to continue...")
            elif choice == 4:
                self.show_info()
                input("\nPress Enter to continue...")
            elif choice == 5:
                print("\nThank you for using CybPss! Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
    
    def show_info(self):
        """Display tool information"""
        print("About CybPss:")
        print("-" * 30)
        print("- This tool generates strong and diverse passwords")
        print("- Uses your personal information to create memorable passwords")
        print("- Supports both English and Arabic characters")
        print("- Includes numbers and special characters for enhanced security")
        print("- Can save results to a text file")
        print()
        print("Security Tips:")
        print("- Never share your passwords with anyone")
        print("- Use different passwords for each account")
        print("- Change your passwords regularly")
        print("- Use two-factor authentication when possible")

def main():
    """Main function"""
    try:
        generator = PasswordGenerator()
        generator.show_menu()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
