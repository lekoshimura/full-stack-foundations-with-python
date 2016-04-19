import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re
import string
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Restaurant

engine = create_engine("sqlite:///restaurantmenu.db")
session = sessionmaker(bind=engine)()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                # http://my-py-lekoshimura.c9users.io/restaurants
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                try:
                    restaurants = session.query(Restaurant).all()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Restaurantes</h1>"
                    for r in restaurants:
                        output += "<ul>"
                        output += "<li>" + str(r.id) + "</li>"
                        output += "<li>" + r.name + "</li>"
                        output += "<li><a href='/restaurants/" + str(r.id) + "/edit'>Edit</a>"
                        output += "<li><a href='/restaurants/" + str(r.id) + "/delete'>Delete</a>"
                        output += "</ul>"
                    output += "<a href='restaurants/new'>Criar novo restaurante</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                except:
                    output = ""
                    output += "<html><body>"
                    output += "<h1>ERROR!</h1>"
                    output += "Unexpected error:" + sys.exc_info()[0]
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                return

            if self.path.endswith("/restaurants/new"):
                # http://my-py-lekoshimura.c9users.io/restaurants/new
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Criar Novo Restaurante</h1>"
                output += "<form method='post' enctype='multipart/form-data' action='/restaurants/post'>"
                output += "Nome: <input type='text' name='name' />"
                output += "<input type='submit' />"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output

            if re.search('/restaurants/\d+/edit', self.path, re.M|re.I):
                # http://my-py-lekoshimura.c9users.io/restaurants/[id]/new
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).get(int(id))

                output = ""
                output += '''
                <html><body>
                <h1>Editar Restaurante</h1>
                <form method='POST' enctype='multipart/form-data' action='/restaurants/edit_post'>
                Nome: <input type="text" name="name" value="%s" />
                <br /><input type="text" name="id" value="%s" />
                <br /><input type="submit" />
                </form>
                </body></html>
                '''  % (restaurant.name, restaurant.id)
                self.wfile.write(output)
                print output

            if re.search('/restaurants/\d+/delete', self.path, re.M|re.I):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).get(int(id))

                output = ""
                output += '''
                <html><body>
                <h1>Excluir Restaurante?</h1>
                <form method='POST' enctype='multipart/form-data' action='/restaurants/delete_post'>
                <ul>
                <li>Nome: %s</li>
                <li>id: %s <input type="hidden" name="id" value="%s" /> </li>
                </ul>
                <input type="submit"/>
                </form>
                </body></html>
                '''  % (restaurant.name, restaurant.id, restaurant.id)
                self.wfile.write(output)
                print output

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path.endswith("/restaurants/edit_post"):
            try:
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                restaurant_id = fields.get('id')[0]
                restaurant_name = fields.get('name')[0]

                print "/restaurants/edit_post"
                print "restaurant_id: " + restaurant_id
                print "restaurant_name: " + restaurant_name

                restaurant = session.query(Restaurant).get(int(restaurant_id))
                restaurant.name = restaurant_name
                session.add(restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header("Location", '/restaurants')
                self.end_headers()
            except:
                pass

        if self.path.endswith("/restaurants/delete_post"):
            try:
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                restaurant_id = fields.get('id')[0]

                print "/restaurants/delete_post"
                print "restaurant_id: " + restaurant_id

                restaurant = session.query(Restaurant).get(int(restaurant_id))
                session.delete(restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header("Location", '/restaurants')
                self.end_headers()
            except:
                pass

        if self.path.endswith("/restaurants/post"):
            try:
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('name')[0]

                restaurant = Restaurant(name = restaurant_name)
                session.add(restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header("Location", '/restaurants')
                self.end_headers()
            except:
                pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        print "http://my-py-lekoshimura.c9users.io/restaurants"
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()