from livereload import Server

server = Server()

# Watch the dashboard HTML and image folders
server.watch('index.html')
server.watch('plots/')
server.watch('models/')

# Serve from current directory on port 5000
server.serve(root='.', port=5000, open_url_delay=1)
