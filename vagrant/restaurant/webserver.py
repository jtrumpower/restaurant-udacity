from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import restaurant_dao
import cgi


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
          if self.path.endswith("/restaurants"):
              restaurants = restaurant_dao.getRestaurants()
              output = ""
              output += "<html><body>"
              for restaurant in restaurants
                output += "<div>"
                output += "<h3>%s</h3>" % restaurant.name
                output += "<a href='/restaurant/%s/edit'>Edit</a><br />" % restaurant.id
                output += "<a href='/restaurant/%s/delete'>Delete</a>"
                output += "</div>"
                output += "</body></html>"

              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              self.wfile.write(output)
              print output
              return
          elif self.path.endswith("/restaurants/new"):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              output = ""
              output += "<html><body>"
              output += "<h1>New Restaurant</h1>"
              output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="message" placeholder="Restaurant name" type="text" ><input type="submit" value="Submit"> </form>'''
              output += "</body></html>"
              self.wfile.write(output)
              print output
              return
          elif self.path.endswith("/edit"):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              output = ""
              output += "<html><body>"
              output += "<h1>&#161 Hola !</h1>"
              output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
              output += "</body></html>"
              self.wfile.write(output)
              print output
              return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
      try:
      	if self.path.endswith("/restaurants/new"):
          return
        elif self.path.endswith("/edit"):
          return
      except:
          pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()