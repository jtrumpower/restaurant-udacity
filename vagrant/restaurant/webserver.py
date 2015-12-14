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
        output += "<h3><a href='/restaurants/new'>Make a new Restaurant</a></h3>"
        for restaurant in restaurants:
          output += "<div>"
          output += "<h3>%s</h3>" % restaurant.name
          output += "<a href='/restaurant/%s/edit'>Edit</a><br />" % restaurant.id
          output += "<a href='/restaurant/%s/delete'>Delete</a>" % restaurant.id
          output += "</div>"
        
        output += "</body></html>"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(output)
        return
      elif self.path.endswith("/restaurants/new"):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += "<h1>New Restaurant</h1>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="name" placeholder="Restaurant name" type="text" ><input type="submit" value="Create"></form>'''
        output += "</body></html>"
        self.wfile.write(output)
        return
      elif self.path.endswith("/edit"):
        id = self.path.split("/")[2]
        restaurant = restaurant_dao.getRestaurant(id)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'><h3>%s</h3></br /><input type="text" name="name" placeholder="New name"><input type="submit" value="Update" /></form>''' % (restaurant.id,restaurant.name)
        output += "</body></html>"
        self.wfile.write(output)
        return
      elif self.path.endswith("/delete"):
        id = self.path.split("/")[2]
        restaurant = restaurant_dao.getRestaurant(id)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += "<h3>Are you sure you want to delete: %s</h3>" % restaurant.name
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'><a href="/restaurants"><input type="button" value="no" /></a><input type="submit" value="Submit"> </form>''' % restaurant.id
        output += "</body></html>"
        self.wfile.write(output)
        return


    except IOError:
      self.send_error(404, 'File Not Found: %s' % self.path)

  def do_POST(self):
    try:
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      self.send_response(301)
      self.send_header('Location','/restaurants')
      self.end_headers()
      if ctype == 'multipart/form-data':
        fields = cgi.parse_multipart(self.rfile, pdict)

      if self.path.endswith("/restaurants/new"):
        name = fields.get('name')[0]
        restaurant_dao.addRestaurant(name)
        return
      elif self.path.endswith("/edit"):
        id = self.path.split("/")[2]
        name = fields.get('name')[0]
        restaurant_dao.updateRestaurant(id, name)
        return
      elif self.path.endswith("/delete"):
        id = self.path.split("/")[2]
        restaurant_dao.deleteRestaurant(id)
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