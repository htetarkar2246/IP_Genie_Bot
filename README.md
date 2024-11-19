# IP Genie Bot

IP Genie is a Telegram bot designed to assist users with IP address calculations, subnetting and general IP-related information. It offers interactive commands and an intuitive menu-driven interface to perform tasks such as CIDR subnetting, IP class identification and more.

---

## Features

- **IP Information**: Get detailed information about any IP address, including its class, type (private/public), default and custom subnet masks, and more.
- **Subnetting**:
  - Perform CIDR-based subnetting calculations.
  - Generate subnets based on the required number of subnets or usable hosts.
  - View details of specific subnets such as Network ID, Start Address, End Address, and Broadcast Address.
- **Notes and References**: Explore IPv4 address classes, special ranges, private address spaces, and default subnet masks.
- **Contact and Support**: Easy access to developer contact details for further queries.

---

## Prerequisites

- **Python 3.8+**
- Telegram Bot Token (available from [BotFather](https://core.telegram.org/bots#botfather)).
- Required Python packages: 
  - `python-telegram-bot`
  - `python-dotenv`

---

## Setup Instructions

1. Clone this repository or download the script directly.
   ```bash
   git clone <repository-url>
   ```
   
2. Create and activate a virtual environment :
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```
      
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file in the project directory and add your bot token:
   ```bash
   TOKEN=<your-telegram-bot-token>
   BOT_USERNAME=<your-bot-username>
   ```
5. Run the bot:
   ```bash
   python IP_Genie.py
   ```
---
  ## Commands
  Initiates the bot and displays the welcome message with interactive buttons:
  ```bash
    /start
  ```
  **Menu**: Navigate to the main menu for options like **Notes** and **Calculate**.
  **Contact Me**: View developer contact information.
  **About**: Learn about the bot.
  
  ## Input Commands
    Depending on the selected mode, provide appropriate input:
    
  - **IP Information**: Provide an IP address (e.g., 192.168.1.0/24).
  - **Subnetting**:
    - **CIDR format**: 192.168.1.0/24.
    - **Needed subnets**: 192.168.1.0,3.
    - **Needed usable hosts**: 192.168.1.0,50.


 ## Menu Options
  - **Notes**:

    - **Classes**: Learn about IPv4 address classes (A, B, C, D, E).
    - **Ranges**: Explore special IP ranges such as loopback and multicast.
    - **Private**: Details of private address spaces.
    - **Default**: Information on default subnet masks.
    
- **Calculate**:

  - **IP Information**: Fetch detailed information about a given IP address.
  - **Subnetting**:
        Generate subnets based on CIDR notation, needed subnets, or usable hosts.
        View details of individual subnets.

---
  ## Contact
  For support or queries, contact the developer on Telegram: @jacob_like_22.
  
  Buy me a coffee via Kpay & Wave:
  
  Name: Htet Arkar
  Phone: 09791444137
  
---
  ## About
  IP Genie – Your dedicated IP calculation assistant! Designed to handle IP address calculations easily, 
  IP Genie is your perfect companion for subnetting and managing IP information in any network setup.

---
  ## License
  This project is open-source and available for modification and distribution. Contributions are welcome!

---
