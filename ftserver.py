from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os.path
import focus

save_file = os.path.expanduser('~/.focus-tree.json')
PORT_NUMBER = 5051
ADDRESS = '0.0.0.0'

THE_TREE = focus.TreeManager()
try:
    THE_TREE = focus.TreeManager.load_from_file(save_file)
except:
    THE_TREE = focus.TreeManager()

# a_root_node = focus.make_test_tree()
# THE_TREE.root_nodes.append(a_root_node)
# REACT_MANIFEST = {}

class FocusTreeRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/api/send-command':
            self.send_response(200)
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            print(str(post_data))

            status = 'OK'
            errors = None
            try:
                THE_TREE.execute_command(post_data)
                THE_TREE.save_to_file(save_file)
            except IndexError as e:
                status = 'error'
                errors = str(e)
            except Exception as e:
                status = 'error'
                errors = str(e)
                raise e
            finally:

                resp = {
                    "command": post_data,
                    "status" : status,
                    "error"  : errors
                }
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(resp), 'utf-8'))


    def do_GET(self):
        print(self.path)
        if self.path == '/':
            return self.send_tree()
        elif self.path.startswith('/api/'):
            return self.serve_api()
        elif self.path.startswith('/simple-client/'):
            return self.serve_simple_client()
        else:
            return self.serve_static_react()

    def serve_api(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        if self.path == '/api/tree':
            return self.send_tree()
        elif self.path == '/api/current-task':
            return self.send_current()

    def serve_simple_client(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        if self.path == '/simple-client/main.js':
            self.send_javascript('main.js')
        elif self.path == '/simple-client/index.html':
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.send_file('index.html')

    def serve_static_react(self):
        # SERVE FILES FOR REACT WEB CLIENT
        react_file = os.path.normpath(
            os.getcwd() + '/clients/ft-web-client/build/' + self.path
            )
        print("os.getcwd() = {}".format(os.getcwd()))
        print("REACT_FILE = {}".format(react_file))
        if   react_file.endswith('css'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/css')
        elif react_file.endswith('js'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript')
        elif react_file.endswith('html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
        elif react_file.endswith('.map'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
        elif react_file.endswith('svg'):
            self.send_response(304)
            self.send_header('Content-Type', 'text/plain')
            pass
        else:
            self.send_header('Content-Type', 'text/plain')

        self.end_headers()
        self.send_file(react_file)


    def send_file(self, filename):
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

    def send_javascript(self, filename):
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        self.send_file(filename)



    def send_tree(self):
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        # hopefully_the_tree = focus.TreeManager.from_dict(THE_TREE.to_dict())
        # hopefully_the_tree.current_task = THE_TREE.current_task
        # message = json.dumps(hopefully_the_tree.to_dict())
        message = json.dumps(THE_TREE.to_dict())
        self.wfile.write(bytes(message, 'utf-8'))


    def send_current(self):
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        message = json.dumps({'current_task': "task"})
        self.wfile.write(bytes(str(THE_TREE.current_task), "utf-8"))



if __name__ == "__main__":
    try:

        with open('./clients/ft-web-client/build/manifest.json') as f:
            manifest = json.loads(f.read())
        # Obviously, frankly, this should be done with an argparse thingy
        import sys
        if len(sys.argv) >= 3:
            if sys.argv[1] == '--port':
                PORT_NUMBER = int(sys.argv[2])

        server = HTTPServer(
            (ADDRESS, PORT_NUMBER),
            FocusTreeRequestHandler
        )

        print("Server is started on {} port {}".format(ADDRESS, PORT_NUMBER))

        server.serve_forever()

    except KeyboardInterrupt:
        print("^C received, shutting down")
        server.socket.close()
