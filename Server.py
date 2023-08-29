# Rasheed Alqobbaj 1202474 - Mohammed Shabaneh 1201297
import socket
import csv


# Read laptop information from CSV file
def read_laptops():
    laptops = []

    with open("laptops.csv", "r") as file:
        # Read CSV file and store each row as a dictionary
        reader = csv.DictReader(file)
        for row in reader:
            # add row to laptops list
            laptops.append(row)
    return laptops

# Sort laptops by name
def sort_by_name(laptops):
    # sorted function takes a list and a key function, it's called on each item in the list
    return sorted(laptops, key=lambda x: x["Laptop Name"].upper())

# Sort laptops by price
def sort_by_price(laptops):
    return sorted(laptops, key=lambda x: float(x["Price"]))


# Handle incoming requests
def handle_request(request, client_address):

    # Redirect rules
    if request == "/" or request == "/index.html" or request == "/main_en.html" or request == "/en":
        # Handle main page requests
        filename = "main_en.html"
        content_type = "text/html; charset=UTF-8"
        # rb = read binary. it's used for reading files that are not text files
        with open(filename, "rb") as file:
            content = file.read()
            # fstring is a string with a variable inside it. it's used for easier string formatting
            # HTTP response Header + Body
            # Encode converts string to bytes
            # utf-8 is a character encoding standard
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8") + content
    elif request == "/ar":
        # Handle Arabic main page requests
        filename = "main_ar.html"
        content_type = "text/html; charset=UTF-8"
        with open(filename, "rb") as file:
            content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8") + content
    elif request.endswith(".css"):
        # Handle CSS file requests
        # filename is the path of the file
        filename = "static" + request
        content_type = "text/css; charset=UTF-8"
        try:
            with open(filename, "rb") as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8") + content
        # FileNotFoundError is raised when a file is not found
        except FileNotFoundError:
            # Generate 404 response for missing files in a separate function
            response = generate_404_response(client_address)
    elif request.endswith(".png"):
        # Handle PNG image requests
        try:
            # request[1:] removes the first character from the request string the "/"
            with open(request[1:], "rb") as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n".encode("utf-8") + content
        except FileNotFoundError:
            # Generate 404 response for missing files
            response = generate_404_response(client_address)
    elif request.endswith(".jpg"):
        # Handle JPG image requests
        try:
            with open(request[1:], "rb") as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n".encode("utf-8") + content
        except FileNotFoundError:
            # Generate 404 response for missing files
            response = generate_404_response(client_address)
    elif request == "/SortByName":
        # Sort laptops by name and generate response
        laptops = read_laptops()
        sorted_laptops = sort_by_name(laptops)
        # shorthand for in loop (list comprehension)
        response_content = "\n".join([f"{item['Laptop Name'].upper()}: ${item['Price']}" for item in sorted_laptops])
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n{response_content}".encode("utf-8")
    elif request == "/SortByPrice":
        # Sort laptops by price, calculate total price, and generate response
        laptops = read_laptops()
        sorted_laptops = sort_by_price(laptops)
        total_price = sum(float(item["Price"]) for item in sorted_laptops)
        response_content = "\n".join([f"{item['Laptop Name']}: ${item['Price']}" for item in sorted_laptops])
        response_content += f"\n\nTotal Price: ${total_price:.2f}"
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n{response_content}".encode("utf-8")
    elif request == "/azn":
        # Handle redirects to amazon.com
        redirect_url = "http://www.amazon.com"
        response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: {redirect_url}\r\n\r\n".encode("utf-8")
    elif request == "/so":
        # Handle redirects to stackoverflow.com
        redirect_url = "http://www.stackoverflow.com"
        response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: {redirect_url}\r\n\r\n".encode("utf-8")
    elif request == "/bzu":
        # Handle redirects to birzeit.edu
        redirect_url = "http://www.birzeit.edu"
        response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: {redirect_url}\r\n\r\n".encode("utf-8")
    else:
        # Handle other requests for files such as html files
        filename = request[1:]
        content_type = "text/html; charset=UTF-8"
        try:
            with open(filename, "rb") as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8") + content
        except FileNotFoundError:
            # Generate 404 response for missing files
            response = generate_404_response(client_address)

    return response

# Generate 404 response page
def generate_404_response(client_address):
    # simple html file for HTTP 404 response as specified
    response = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n\r\n"
        "<html>"
        "<head>"
        "<title>Error 404</title>"
        "<link rel=stylesheet type=text/css href=styles.css>"
        "</head>"
        "<body style='text-align:center;'>"
        "<h1>Error 404</h1>"
        "<p style='color:red;'>The file is not found</p>"
        "<p><strong>Rasheed Alqobbaj - 1202474, Mohammed Shabaneh - 1201297</strong></p>"
        f"<p><strong>Client IP and Port: {client_address[0]}:{client_address[1]}</strong></p>"
        "</body></html>"
    ).encode("utf-8")
    return response

# Main server loop
def main():
    # Create a socket object
    # AF_INET parameter indicates that we are using IPv4
    # SOCK_STREAM parameter indicates that we are using TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a host and port
    server_socket.bind(("localhost", 12345))
    # Listen for incoming connections (1 connection at a time since specified using the same computer in the project description)
    server_socket.listen(1)

    # Print a message to indicate that the server is listening
    print("Listening on port 12345...")

    # while true loop to keep the server running
    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()

        # Receive data from client
        # Should look like this "GET /SortByName HTTP/1.1"
        received_data = client_socket.recv(1024).decode("utf-8")

        # Handle the request and generate a response
        if received_data:
            # Split the received data into parts based on spaces
            # Should look like this ["GET", "/SortByName", "HTTP/1.1"]
            request_parts = received_data.split()
            # Check if the request is valid
            if len(request_parts) >= 2:
                request = request_parts[1]
                # Print the request to the console as specified in the project description
                print(f"Received request: {request}")
                # Handle the request and generate a response
                response = handle_request(request, client_address)
                # Send the response to the client
                # sendall() is used to send the entire response at once
                client_socket.sendall(response)
            else:
                print("Invalid request format")
        else:
            print("No data received from client")

        # Close the connection with the client
        client_socket.close()

if __name__ == "__main__":
    main()
