# CybPss - Advanced Password Generator

A professional Python tool for generating strong and diverse passwords based on your personal information with a beautiful colored interface.

## ✨ Features

- 🎯 **Interactive English Interface**: Easy to use and intuitive
- 🔒 **Strong Password Generation**: Combines letters, numbers, and special characters
- 🎨 **Personal Customization**: Uses your personal information to create memorable passwords
- 📊 **Password Strength Assessment**: Shows security level for each password
- 💾 **Save Results**: Ability to save passwords to a text file
- 🎲 **Smart Variations**: Generates multiple variations from the same information
- 🌈 **Professional Colored Interface**: Beautiful ASCII art logo and colored output
- ⚡ **Cross-Platform**: Works on Windows, Linux, and macOS

## 🚀 How to Run

### Requirements
- Python 3.6 or later
- No external libraries required

### Running
```bash
python CybPss.py
```

## 📋 How to Use

1. **Run the tool**: Execute the file in Terminal
2. **Answer questions**: You'll be asked about personal information like:
   - Your name
   - Birth year
   - Favorite color
   - Favorite animal
   - Favorite hobby
   - Favorite number
   - City you live in

3. **Choose from menu**:
   - Generate new passwords
   - Display current passwords
   - Save passwords to file
   - About CybPss
   - Exit

## 🔧 How the Tool Works

The tool performs:
1. **Collects personal information** through interactive questions
2. **Generates multiple variations** from each piece of information:
   - Adding random numbers
   - Adding special characters
   - Mixing uppercase and lowercase letters
   - Combining multiple information pieces
3. **Evaluates password strength** based on:
   - Length (8+ characters)
   - Presence of uppercase and lowercase letters
   - Presence of numbers
   - Presence of special characters
4. **Displays results** with security strength indicators

## 🛡️ Security Tips

- ❌ Never share your passwords with anyone
- 🔄 Use different passwords for each account
- 📅 Change your passwords regularly
- 🔐 Use two-factor authentication when possible
- 💾 Store passwords in a secure place

## 📁 Project Files

- `CybPss.py` - Main tool file
- `requirements.txt` - Project requirements
- `README.md` - Usage guide
- `test_cybpss.py` - Test script

## 🎯 Usage Example

```
╔══════════════════════════════════════════════════════════╗
║  ██╗   ██╗██╗██████╗ ██████╗ ██████╗ ███████╗███████╗  ║
║  ╚██╗ ██╔╝██║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝  ║
║   ╚████╔╝ ██║██████╔╝██████╔╝██████╔╝███████╗███████╗   ║
║    ╚██╔╝  ██║██╔═══╝ ██╔═══╝ ██╔═══╝ ╚════██║╚════██║    ║
║     ██║   ██║██║     ██║     ██║     ███████║███████║     ║
║     ╚═╝   ╚═╝╚═╝     ╚═╝     ╚═╝     ╚══════╝╚══════╝     ║
╚══════════════════════════════════════════════════════════╝

Advanced Password Generator
Interactive Personal Password Creation Tool
============================================================

[MENU] Choose from the menu:

1. [GENERATE] Generate new passwords
2. [DISPLAY] Display current passwords
3. [SAVE] Save passwords to file
4. [ABOUT] About CybPss
5. [EXIT] Exit

[NAME] What's your name?: John
[YEAR] What year were you born?: 1990
[COLOR] What's your favorite color?: blue
[ANIMAL] What's your favorite animal?: tiger
[HOBBY] What's your favorite hobby?: reading
[NUMBER] What's your favorite number?: 7
[CITY] What city do you live in?: New York

[SUCCESS] Your information has been saved successfully!

[*] Generating passwords...

[SUCCESS] Generated 29 unique passwords!
============================================================

 1. TiGeR1@655#3 [Strong]
 2. tiger!*7EkKS [Strong]
 3. BlUe3#1!01@3 [Strong]
 4. ReAdInG32187 [Medium]
 5. bl7ueSCKLqdy [Medium]
 ...
```

## 📞 Support

If you encounter any issues or have suggestions, please contact us.

---

**Note**: This tool is for educational and personal purposes. Make sure to follow security best practices when creating passwords.
