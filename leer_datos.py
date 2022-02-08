from http.server import HTTPServer, BaseHTTPRequestHandler

host='192.168.20.135'
puerto=8888

class texthandler (BaseHTTPRequestHandler):
    #si se usa esta clase se envia el string de wfile.write
    def do_GET(self):
        self.send_response(200)
        self.send_header('context-type', 'text/html')
        self.end_headers()
        self.wfile.write('pruebaxdxdxd'.encode())

class echohandler (BaseHTTPRequestHandler):
    # si se usa esta clase se envia lo que aparezca 
    # luego del primer / de la url
    def do_GET(self):
        self.send_response(200)
        self.send_header('context-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.path[1:].encode())

def configurarservidor():
    puerto=8888
    servidor = HTTPServer((host,puerto), echohandler)
    print('el servidor esta activo')
    print(f'http://{host}:{puerto}')
    servidor.serve_forever()
    servidor.server_close()
    print('servidor detenido')

configurarservidor()