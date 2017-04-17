import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        post = Model.get_by_id
        self.response.write(post)

class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_base(self):
        blogs = db.GqlQuery("SELECT * FROM Blog "
                            "ORDER BY created DESC ")
        self.render("frontpage.html", blogs=blogs)

    def get(self):
        self.render_base()

class NewPost(Handler):
    def render_front(self, title="", blog="", error=""):
        self.render("newpost.html", title=title, blog=blog, error=error)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        if title and blog:
            a = Blog(title = title, blog = blog)
            a.put()
            self.redirect("/blog")
        else:
            error = "We need both the title and blogpost!"
            self.render_front(title, blog, error)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', MainPage),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
