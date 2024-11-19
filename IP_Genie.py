from typing import final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
import ipaddress
import math
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: final = os.getenv('TOKEN')
BOT_USERNAME: final = os.getenv('BOT_USERNAME')

# Home messages
welcome_message: str = (
    "Hello! I’m here to help you with IP calculations.\n"
    "Use the commands below to get started:\n\n"
    "Just provide an IP address or subnet information, and I'll help you with calculations. "
)

menu_message: str = (
    "Welcome to the menu! Here are your options:\n\n"
    "<b>Notes</b>: Access important notes and information.\n"
    "<b>Calculate</b>: Perform IP calculations and get quick results.\n\n"
    "Choose an option by clicking one of the buttons below."
)

about_message: str = (
    "IP Genie – Your dedicated IP calculation assistant! Designed to handle IP address calculations easily, "
    "IP Genie is your perfect companion for subnetting and managing IP information in any network setup."
)

contact_message: str = "Contact the developer on Telegram: @htetarkar2246 for any questions or help.\nIf this bot is helpful to you, you can buy me a coffee!\n\nKpay & Wave \nName: Htet Arkar\nPh: 09791444137"

# Menu messages
notes_message: str = (
    "<b>Classes</b>: IPv4 Address Classes\n"
    "<b>Ranges</b>: Special Address Ranges\n"
    "<b>Private</b>: Private Address Space\n"
    "<b>Default</b>: Default Subnet Masks\n"
)

calculate_message: str = (
    "<b>IP Information</b>: Detailed information of the IP.\n"
    "<b>Subnetting</b>: Detailed functions for subnetting the IP.\n"
)

# Notes messages
classes_message: str = (
    "IPv4 Address Classes\n"
    "<b>Class A</b>:       1 – 127\n"
    "<b>Class B</b>:     128 – 191\n"
    "<b>Class C</b>:     192 – 223\n"
    "<b>Class D</b>:     224 – 239     (Reserved for multicast)\n"
    "<b>Class E</b>:     240 – 255     (Reserved for experimental, used for research)\n\n"
)

ranges_message: str = (
    "<b>Loopback</b> - Only the single 127.0.0.1 address is used; addresses 127.0.0.0 to 127.255.255.255 "
    "are reserved. Any address within this block will loop back to the local host.\n\n"
    "<b>Link-Local Addresses</b> - IPv4 addresses in the address block 169.254.0.0 to 169.254.255.255 "
    "(169.254.0.0/16) are designated as link-local addresses.\n\n"
    "<b>TEST-NET Addresses</b> - The address block 192.0.2.0 to 192.0.2.255 (192.0.2.0/24) is set aside "
    "for teaching and learning purposes.\n\n"
    "<b>Experimental Addresses</b> - The addresses in the block 240.0.0.0 to 255.255.255.254 are listed "
    "as reserved for future use (RFC 3330)."
)

private_message: str = (
    "<b>Class A</b>: 10.0.0.0 to 10.255.255.255\n"
    "<b>Class B</b>: 172.16.0.0 to 172.31.255.255\n"
    "<b>Class C</b>: 192.168.0.0 to 192.168.255.255"
)

default_message: str = (
    "<b>Class A</b>: 255.0.0.0\n"
    "<b>Class B</b>: 255.255.0.0\n"
    "<b>Class C</b>: 255.255.255.0"
)

subnetting_message: str = (
    "<b>CIDR Notation</b>:Subnet ID with CIDR Notation.\n"
    "<b>Needed Subnets</b>:Subnet ID with Needed Subnets.\n"
    "<b>Needed Usable Hosts</b>:Subnet ID with Needed Usable Hosts."
)

# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Menu", callback_data='menu')],
        [InlineKeyboardButton("Contact Me", callback_data='help')],
        [InlineKeyboardButton("About", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Home buttons
    if query.data == 'menu':
        keyboard = [
            [InlineKeyboardButton("Notes", callback_data='notes')],
            [InlineKeyboardButton("Calculate", callback_data='calculate')],
            [InlineKeyboardButton("Back", callback_data='back_to_home')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(menu_message, reply_markup=reply_markup, parse_mode='HTML')

    elif query.data == 'help':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back_to_home')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(contact_message, reply_markup=reply_markup, parse_mode='HTML')

    elif query.data == 'about':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back_to_home')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(about_message, reply_markup=reply_markup, parse_mode='HTML')

    # Menu buttons
    elif query.data == 'notes':
        keyboard = [
            [InlineKeyboardButton("Classes", callback_data='classes')],
            [InlineKeyboardButton("Ranges", callback_data='ranges')],
            [InlineKeyboardButton("Private", callback_data='private')],
            [InlineKeyboardButton("Default", callback_data='default')],
            [InlineKeyboardButton("Back", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(notes_message, reply_markup=reply_markup, parse_mode='HTML')

    elif query.data == 'calculate':
        keyboard = [
            [InlineKeyboardButton("IP Information", callback_data='ip_information')],
            [InlineKeyboardButton("Subnetting", callback_data='subnetting')],
            [InlineKeyboardButton("Back", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(calculate_message, reply_markup=reply_markup, parse_mode='HTML')

    elif query.data == 'back_to_home':
        keyboard = [
            [InlineKeyboardButton("Menu", callback_data='menu')],
            [InlineKeyboardButton("Contact Me", callback_data='help')],
            [InlineKeyboardButton("About", callback_data='about')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode='HTML')

    # Notes buttons
    elif query.data == 'classes':
        keyboard = [[InlineKeyboardButton("Back", callback_data='notes')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(classes_message, reply_markup=reply_markup, parse_mode='HTML')

    elif query.data == 'ranges':
        keyboard = [[InlineKeyboardButton("Back", callback_data='notes')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(ranges_message, reply_markup=reply_markup, parse_mode='HTML')

    elif query.data == 'private':
        keyboard = [[InlineKeyboardButton("Back", callback_data='notes')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(private_message, reply_markup=reply_markup, parse_mode='HTML')

    elif query.data == 'default':
        keyboard = [[InlineKeyboardButton("Back", callback_data='notes')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(default_message, reply_markup=reply_markup, parse_mode='HTML')

    # Calculate buttons
    elif query.data == 'ip_information':
        context.user_data['mode'] = 'ip_information'
        await query.edit_message_text("Please enter an IP address (e.g., '192.168.1.0/24 or 192.168.1.0').")
        
    elif query.data == 'subnetting':
        keyboard = [    
            [InlineKeyboardButton("CIDR Notation", callback_data='cidr_subnet')],
            [InlineKeyboardButton("Needed Subnets", callback_data='needed_subnets_subnet')],
            [InlineKeyboardButton("Needed Usuable Hosts", callback_data='needed_usable_hosts')],
            [InlineKeyboardButton("Back", callback_data='calculate')]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(subnetting_message, reply_markup=reply_markup, parse_mode='HTML')
        
    #Subnet buttons 
    elif query.data == 'cidr_subnet':
        context.user_data['mode'] = 'cidr_subnet'
        await query.edit_message_text("Please enter an IP address with CIDR format (e.g.'192.168.1.0/24').")
    
    elif query.data == 'needed_subnets_subnet':
        context.user_data['mode'] = 'needed_subnets_subnet'
        await query.edit_message_text("Please enter an IP address and a positive integer as number of needed subnets. (e.g.'192.168.1.0, 3').")
    
    elif query.data == 'needed_usable_hosts':
        context.user_data['mode'] = 'needed_usable_hosts'
        await query.edit_message_text("Please enter an IP address and a positive integer as number of needed usuable hosts. (e.g.'192.168.1.0, 3').")
    #subnet details
    elif query.data == 'subnet_details':
        context.user_data['mode'] = 'subnet_details'
        await query.edit_message_text("Please enter a positive inter as subnet number to view subnet deatils. (e.g. for 1st subnet enter '1' or for 2nd subnet enter '2')")

#calculation functions

#ip information function 

def ip_information(ip: str):
    try:
    
        # return {"Error: ": "Prefix length required for Class D and E IP addresses."}       
        ip_obj = ipaddress.ip_interface(ip)
        network = ip_obj.network
        cidr_notation = network.prefixlen
        network_address = network.network_address
        custom_subnet_mask = network.netmask

        # Separate octets for IP class determination 
        octets = ip.split('.')
        first_octet = int(octets[0])

        # Class, net-host and binary subnet mask
        if 1 <= first_octet <= 127:
            ip_class = "A"
            net_host = "NET.HOST.HOST.HOST"
            subnet_mask = "255.0.0.0"
            binary_subnet_mask = "11111111.00000000.00000000.00000000"
            default_prefix = "8"
        elif 128 <= first_octet <= 191:
            ip_class = "B"
            net_host = "NET.NET.HOST.HOST"
            subnet_mask = "255.255.0.0"
            binary_subnet_mask = "11111111.11111111.00000000.00000000"
            default_prefix = "16"
        elif 192 <= first_octet <= 223:
            ip_class = "C"
            net_host = "NET.NET.NET.HOST"
            subnet_mask = "255.255.255.0"
            binary_subnet_mask = "11111111.11111111.11111111.00000000"
            default_prefix = "24"
        elif 224 <= first_octet <= 239:
            ip_class = "D (Multicast)"
            net_host = "Used for multicast addresses and does not have a network or host division."
            binary_subnet_mask = "Reserved for multicast"
            default_prefix = "-"
        else:
            ip_class = "E (Experimental)"
            net_host = "Reserved for experimental purposes and does not have a typical network or host division."
            binary_subnet_mask = "Reserved for experimental"
            default_prefix = "-"
             
        # Binary Network Address (calculate using network address)
        binary_network_address = '.'.join([format(int(octet), '08b') for octet in str(network_address).split('.')])

        # Identify if the IP is private or public
        if ip_obj.is_private:
            ip_type = "Private"
        else:
            ip_type = "Public"

        # Prepare the return object
        return_obj = {
            "IP Address: ": ip,
            "Class: ": ip_class,
            "Network Address: ": str(network_address),
            "Binary Network Address: ": binary_network_address,
            "Default Subnet Mask: ": str(subnet_mask),
            "Custom Subnet Mask: ": str(custom_subnet_mask),
            "Binary Default Subnet Mask: ": binary_subnet_mask,
            "Net-Host: ": net_host,
            "Default Prefix Length: ":default_prefix,
            "CIDR Notation: ": f"/{cidr_notation}",
            "IP Type: ": ip_type
        }       
        
        return return_obj    
    except ValueError:
        return {"Error: ": "Invalid IP address. Please try again (e.g., '192.168.1.0/24' or '192.168.1.0')."}

#CIDR subnetting
def cidr_subnetting(ip: str):
    """
    Subnetting calculations based on CIDR.
    """
    
    try:        
        ip_info_obj = ip_information(ip)
        
        ip_obj = ipaddress.ip_interface(ip)
        network = ip_obj.network
        
        # Calculations for subnetting
        total_subnets = 2 ** (network.prefixlen - int(ip_info_obj["Default Prefix Length: "]))
        total_hosts = network.num_addresses
        usable_hosts = total_hosts - 2  # Subtracting 2 for network and broadcast addresses
        borrowed_bits = network.prefixlen - int(ip_info_obj["Default Prefix Length: "])
        custom_prefix = int(ip_info_obj["Default Prefix Length: "])+borrowed_bits
        custom_subnet_mask = ipaddress.IPv4Network('0.0.0.0/' + str(custom_prefix), strict=False).netmask
        
        #detail subnets
        network_address = network.network_address
        
        subnets = []
        
        for i in range(total_subnets):
            network_id = network_address+(total_hosts*i)
            broadcast_id = (network_address+(total_hosts*(i+1))) - 1
            start_address = network_id + 1
            end_address = broadcast_id - 1
            
            subnets.append({
            "Network ID: ": network_id,
            "Start Address: ":start_address,
            "End Address: ":end_address,
            "Broadcast ID: ":broadcast_id
            })
            
        return_obj = {
            "IP Address: ": ip_info_obj["IP Address: "],
            "Class: ": ip_info_obj["Class: "],
            "Network Address: ": str(ip_info_obj["Network Address: "]),
            "Default Subnet Mask: ": str(ip_info_obj["Default Subnet Mask: "]),
            "Custom Subnet Mask: ": str(custom_subnet_mask),
            "Total Number of Subnets: ": str(total_subnets),
            "Total Number of Host Addresses: ": str(total_hosts),
            "Number of Usable Addresses: ": str(usable_hosts),
            "Borrowed Bits: ": str(borrowed_bits),
            "Subnets: ":subnets
        }
        
        return return_obj
    
    except ValueError:
        return {"Error": "Invalid IP address. Please try again (e.g., '192.168.1.0/24' or '192.168.1.0')."}
    
#needed_subnets_subnetting
def needed_subnets_subnetting(user_input: str):
    """
    Subnetting calculations based on needed subnets.
    """
    try:
        # Attempt to split the input into IP and needed_subnets
        ip, needed_subnets = user_input.strip().split(",")
    except ValueError:
        # If splitting fails, return an error message
        return {
            "Error": "Invalid input!!"
        }
        
        
    try:
        # Validate and convert needed_subnets to an integer
        needed_subnets = int(needed_subnets)
        if needed_subnets <= 0:
            return {
                "Error": "Needed subnets must be a positive integer.\n"
                         "Please enter an IP address and a positive integer as the number of needed subnets. (e.g., '192.168.1.0,3')."
            }
    except ValueError:
        return {
            "Error": "Invalid needed subnets value.\n"
                     "Please enter an IP address and a positive integer as the number of needed subnets. (e.g., '192.168.1.0,3')."
        }
        
    try:  
        ip_info_obj = ip_information(ip)
        borrowed_bits = math.ceil(math.log2(needed_subnets))
        default_prefix = int(ip_info_obj["Default Prefix Length: "])
        custom_prefix = default_prefix + borrowed_bits
        custom_subnet_mask = ipaddress.IPv4Network('0.0.0.0/' + str(custom_prefix), strict=False).netmask
        
        if custom_prefix > 32:
            return {"Error": "Cannot create subnets; too many subnets requested."}
        
        host_bits = 32 - custom_prefix
        total_hosts = 2**host_bits
        usable_hosts = total_hosts - 2
        total_subnets = 2**(custom_prefix - int(ip_info_obj["Default Prefix Length: "]))
        
        #detail subnets
        ip_obj = ipaddress.ip_interface(ip)
        network = ip_obj.network
        network_address = network.network_address
        
        subnets = []
        
        for i in range(total_subnets):
            network_id = network_address+(total_hosts*i)
            broadcast_id = (network_address+(total_hosts*(i+1))) - 1
            start_address = network_id + 1
            end_address = broadcast_id - 1
            
            subnets.append({
            "Network ID: ": network_id,
            "Start Address: ":start_address,
            "End Address: ":end_address,
            "Broadcast ID: ":broadcast_id
            })
                        
        return_obj = {
            "IP Address: ": ip_info_obj["IP Address: "],
            "Class: ": ip_info_obj["Class: "],
            "Network Address: ": str(ip_info_obj["Network Address: "]),
            "Default Subnet Mask: ": str(ip_info_obj["Default Subnet Mask: "]),
            "Custom Subnet Mask: ": str(custom_subnet_mask),
            "Total Number of Subnets: ": str(total_subnets),
            "Total Number of Host Addresses: ": str(total_hosts),
            "Number of Usable Addresses: ": str(usable_hosts),
            "Borrowed Bits: ": str(borrowed_bits),
            "Subnets: ":subnets
        }
        
        return return_obj
        
    except ValueError:
        return {
            "Error": "Invalid IP address.\n"
                     "Please enter a valid IP address and a positive integer as the number of needed subnets. (e.g., '192.168.1.0,3')."
        }
 
#needed_usuable_hosts_subnetting
def needed_usable_hosts_subnetting(user_input: str):
    """
    Subnetting calculations based on needed subnets.
    """
    try:
        # Attempt to split the input into IP and needed_subnets
        ip, needed_usable_hosts = user_input.strip().split(",")
    except ValueError:
        # If splitting fails, return an error message
        return {
            "Error": "Invalid input!!"
        }
        
    try:
        # Validate and convert needed_subnets to an integer
        needed_usable_hosts = int(needed_usable_hosts)
        if needed_usable_hosts <= 0:
            return {
                "Error": "Needed subnets must be a positive integer.\n"
                         "Please enter an IP address and a positive integer as the number of needed usuable hosts. (e.g., '192.168.1.0,3')."
            }
    except ValueError:
        return {    
            "Error": "Invalid needed subnets value.\n"
                     "Please enter an IP address and a positive integer as the number of needed usuable hosts. (e.g., '192.168.1.0,3')."
        }
        
    try:
    
        ip_info_obj = ip_information(ip.strip())
        
        default_prefix = int(ip_info_obj["Default Prefix Length: "])
        host_bits = math.ceil(math.log2(needed_usable_hosts + 2))# +2 for network ID and broadcast addresses
        custom_prefix = 32 - host_bits
        custom_subnet_mask = ipaddress.IPv4Network('0.0.0.0/' + str(custom_prefix), strict=False).netmask

        if custom_prefix < default_prefix:
            return {"Error": "Not enough host bits to accommodate the required usable hosts."}
        
        borrowed_bits = custom_prefix - default_prefix
        total_subnets = 2**borrowed_bits
        total_hosts = 2**host_bits
        usable_hosts = total_hosts - 2
        
        #detail subnets
        ip_obj = ipaddress.ip_interface(ip)
        network = ip_obj.network
        network_address = network.network_address
        
        subnets = []
        
        for i in range(total_subnets):
            network_id = network_address+(total_hosts*i)
            broadcast_id = (network_address+(total_hosts*(i+1))) - 1
            start_address = network_id + 1
            end_address = broadcast_id - 1
            
            subnets.append({
            "Network ID: ": str(network_id),
            "Start Address: ":str(start_address),
            "End Address: ":str(end_address),
            "Broadcast ID: ":str(broadcast_id)
            })
                
        return_obj = {
            "IP Address: ": ip_info_obj["IP Address: "],
            "Class: ": ip_info_obj["Class: "],
            "Network Address: ": str(ip_info_obj["Network Address: "]),
            "Default Subnet Mask: ": str(ip_info_obj["Default Subnet Mask: "]),
            "Custom Subnet Mask: ": str(custom_subnet_mask),
            "Total Number of Subnets: ": str(total_subnets),
            "Total Number of Host Addresses: ": str(total_hosts),
            "Number of Usable Addresses: ": str(usable_hosts),
            "Borrowed Bits: ": str(borrowed_bits),
            "Subnets: ":subnets
        }
        
        return return_obj
        
    except ValueError:
        return {
            "Error": "Invalid IP address.\n"
                     "Please enter a valid IP address and a positive integer as the number of needed usuable hosts. (e.g., '192.168.1.0, 3')."
        }      

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    mode = context.user_data.get('mode')
    global subnets_list
    
    if mode == 'ip_information':
        
        keyboard = [
            [InlineKeyboardButton("Back", callback_data='calculate')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        return_obj = ip_information(user_input)
        result = ""
        for key, value in return_obj.items():
            result += f"\n{key} {value}\n"
        await update.message.reply_text(result, reply_markup=reply_markup)
        
    elif mode == 'cidr_subnet':            
        return_obj = cidr_subnetting(user_input)
        
        if "Error" not in return_obj:
            
            keyboard = [
                [InlineKeyboardButton("Subnet Details", callback_data='subnet_details')],
                [InlineKeyboardButton("Back", callback_data='subnetting')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            result = ""
            items = list(return_obj.items())[:-1]
            subnets = list(return_obj.items())[-1]
                
            for key, value in items:
                result += f"\n{key} {value}\n"
            await update.message.reply_text(result, reply_markup=reply_markup)   
        else:
            keyboard = [
                [InlineKeyboardButton("Back", callback_data='subnetting')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(return_obj["Error"], reply_markup=reply_markup) 
    
    elif mode == 'needed_subnets_subnet':          
        return_obj = needed_subnets_subnetting(user_input)
        
        if "Error" not in return_obj:
        
            keyboard = [
                [InlineKeyboardButton("Subnet Details", callback_data='subnet_details')],
                [InlineKeyboardButton("Back", callback_data='subnetting')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            result = ""
            items = list(return_obj.items())[:-1]
            subnets = list(return_obj.items())[-1]    
            subnets_list = subnets  
            
            for key, value in items:
                result += f"\n{key} {value}\n"
            await update.message.reply_text(result, reply_markup=reply_markup)
        else:
            keyboard = [
                [InlineKeyboardButton("Back", callback_data='subnetting')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(return_obj["Error"], reply_markup=reply_markup) 
        
    elif mode == 'needed_usable_hosts':
                   
        return_obj = needed_usable_hosts_subnetting(user_input)
        
        if "Error" not in return_obj:
        
            keyboard = [
                [InlineKeyboardButton("Subnet Details", callback_data='subnet_details')],
                [InlineKeyboardButton("Back", callback_data='subnetting')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            result = ""
            items = list(return_obj.items())[:-1]
            subnets = list(return_obj.items())[-1]
            
            for key, value in items:
                result += f"\n{key} {value}\n"
            await update.message.reply_text(result, reply_markup=reply_markup)
        else:
            keyboard = [
                [InlineKeyboardButton("Back", callback_data='subnetting')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(return_obj["Error"], reply_markup=reply_markup) 
        
    elif mode == 'subnet_details':     
        keyboard = [
            [InlineKeyboardButton("Back", callback_data='subnetting')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)        
        
        try:
            # Convert user_input to an integer index (0-based)
            index = int(user_input) - 1
        
            # Check if the index is within range
            if index < 0:
                await update.message.reply_text(f"Subnet can't be negative number.", reply_markup=reply_markup)
            elif index >= len(subnets_list[1]):
                await update.message.reply_text(f"No subnet at {user_input}.", reply_markup=reply_markup)

            # Get the subnet dictionary at the given index
            subnet = subnets_list[1][index]  # Access the second element of the tuple (the list of subnets)
        
            # Access values from the dictionary
            network_id = subnet['Network ID: ']
            start_address = subnet['Start Address: ']
            end_address = subnet['End Address: ']
            broadcast_id = subnet['Broadcast ID: ']
        
            # Prepare the response message
            reply = f"Subnet {user_input}\n\n" \
                    f"Network ID: {network_id}\n" \
                    f"Start Address: {start_address}\n" \
                    f"End Address: {end_address}\n" \
                    f"Broadcast ID: {broadcast_id}"

            # Send the reply with the subnet details
            await update.message.reply_text(reply, reply_markup=reply_markup)

        except ValueError:
            await update.message.reply_text("Invalid input. Please enter a valid subnet number.", reply_markup=reply_markup)

    else:
        await update.message.reply_text("Invalid Input.", reply_markup=reply_markup)
    
    
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    print("Bot Starting...")
    app.run_polling()

