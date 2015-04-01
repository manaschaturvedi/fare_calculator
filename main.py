import os
import webapp2
import jinja2
from google.appengine.ext import db
import urllib
from xml.dom import minidom


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Query(db.Model):
    source = db.StringProperty(required = True)
    destination = db.StringProperty(required = True)
    
class MainPage(Handler):
    def get(self):
        qo = db.GqlQuery("SELECT * FROM Query")
        self.render('map.html', qo = qo)
    def post(self):
        addr1 = self.request.get("addr1")
        addr2 = self.request.get("addr2")
        a = Query(source = addr1, destination = addr2)
        a.put()
        url = 'http://maps.googleapis.com/maps/api/distancematrix/xml?origins=' + urllib.quote_plus(addr1) + '&destinations=' + urllib.quote_plus(addr2) + '&mode=driving&sensor=false'
        link = urllib.urlopen(url).read()
        x = minidom.parseString(link)
        p = x.getElementsByTagName('text')[1].childNodes [0].nodeValue
        li = p.split()
        dist = float(li[0])
        dii = str(dist)
        self.response.write('The total distance between the source and the destination is' + ' ' + dii + 'km')
        if(dist <= 1.5):
            ans = 'Rs.15'
            total_taxi = 'Rs.19'
            
        else:
            districk = dist*10
            ans = 'Rs.' + str(districk)
            d = dist - 1.5
            t = d * 12.35
            tot_taxi = t + 19
            total_taxi = 'Rs.' + str(tot_taxi)
            
            
        dist_bus = dist
        if(dist_bus <= 2):
            j = 'Rs.6'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=2 and dist_bus <=3):
            j = 'Rs.8'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=3 and dist_bus <=5):
            j = 'Rs.10'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=5 and dist_bus <=7):
            j = 'Rs.12'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=7 and dist_bus <=10):
            j = 'Rs.15'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=10 and dist_bus <=15):
            j = 'Rs.18'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=15 and dist_bus <=20):
            j = 'Rs.20'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=20 and dist_bus <=25):
            j = 'Rs.22'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=25 and dist_bus <=30):
            j = 'Rs.25'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=30 and dist_bus <=35):
            j = 'Rs.28'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=35 and dist_bus <=40):
            j = 'Rs.30'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=40 and dist_bus <=45):
            j = 'Rs.35'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
        elif(dist_bus >=45 and dist_bus <=50):
            j = 'Rs.40'
            self.render('fare.html', j = j, total_taxi = total_taxi, ans = ans)
            
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)