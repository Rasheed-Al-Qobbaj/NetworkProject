import socket

def handle_request(request, client_address):
    # Redirect rules
    if request == "/azn":
        redirect_url = "http://www.amazon.com"
        response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: {redirect_url}\r\n\r\n".encode("utf-8")
    elif request == "/so":
        redirect_url = "http://www.stackoverflow.com"
        response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: {redirect_url}\r\n\r\n".encode("utf-8")
    elif request == "/bzu":
        redirect_url = "http://www.birzeit.edu"
        response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: {redirect_url}\r\n\r\n".encode("utf-8")
    elif request == "/" or request == "/index.html" or request == "/main_en.html" or request == "/en":
        filename = "main_en.html"
        content_type = "text/html; charset=UTF-8"
        with open(filename, "rb") as file:
            content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8") + content
    elif request == "/ar":
        filename = "main_ar.html"
        content_type = "text/html; charset=UTF-8"
        with open(filename, "rb") as file:
            content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8") + content
    elif request.endswith(".css"):
        filename = "static" + request
        content_type = "text/css; charset=UTF-8"
        try:
            with open(filename, "rb") as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8") + content
        except FileNotFoundError:
            response = generate_404_response(client_address)
    else:
        filename = request[1:]
        content_type = "text/html; charset=UTF-8"
        try:
            with open(filename, "rb") as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8") + content
        except FileNotFoundError:
            response = generate_404_response(client_address)

    return response

def generate_404_response(client_address):
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
        "<p><strong>Your names and IDs: Rasheed Alqobbaj - 1202474, Mohammed Shabaneh - 1201297</strong></p>"
        f"<p><strong>Client IP and Port: {client_address[0]}:{client_address[1]}</strong></p>"
        "</body></html>"
    ).encode("utf-8")
    return response

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(1)

    print("Listening on port 12345...")

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode("utf-8").split()[1]
        print(f"Received request: {request}")
        response = handle_request(request, client_address)  # Pass client_address
        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    main()