import socket
# Function to get IP address for a domain
def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None
# Read the domain names from the input file
with open('sites.txt', 'r') as file:
    domains = file.readlines()
# Open a file to save the domain-IP results
with open('jito_range.txt', 'a') as output_file:
    for domain in domains:
        domain = domain.strip() # Remove any extra spaces or newline characters
        ip_address = get_ip(domain)

        if ip_address:
            output_file.write(f'{ip_address} ==> {domain}\n')
        else:
            pass
print("IP addresses saved to jito_range.txt")
