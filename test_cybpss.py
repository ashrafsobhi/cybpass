#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for CybPss
"""

from CybPss import PasswordGenerator

def test_cybpss():
    """Test CybPss functionality"""
    print("Testing CybPss - Advanced Password Generator")
    print("=" * 50)
    
    # Create generator instance
    generator = PasswordGenerator()
    
    # Set test user info
    generator.user_info = {
        'name': 'John',
        'birth_year': 1990,
        'favorite_color': 'blue',
        'favorite_animal': 'tiger',
        'hobby': 'reading',
        'favorite_number': 7,
        'city': 'New York'
    }
    
    print("Test user info set:")
    for key, value in generator.user_info.items():
        print(f"  {key}: {value}")
    print()
    
    # Generate passwords
    print("Generating passwords...")
    generator.generate_passwords()
    
    # Display results
    print(f"Generated {len(generator.passwords)} unique passwords!")
    print("=" * 50)
    
    for i, password in enumerate(generator.passwords[:10], 1):  # Show first 10
        strength = generator.calculate_strength(password)
        print(f"{i:2d}. {password} {strength}")
    
    if len(generator.passwords) > 10:
        print(f"... and {len(generator.passwords) - 10} more passwords")
    
    print("=" * 50)
    
    # Test file saving
    print("Testing file save...")
    filename = generator.save_to_file()
    if filename:
        print(f"Passwords saved successfully to: {filename}")
    else:
        print("Failed to save passwords")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_cybpss()
