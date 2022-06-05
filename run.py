

# Creating a dummy database query
posts = [
    {'author': 'John Doe', 
    'title': 'Blog Post 1', 
    'content': 'This is my first blog post',
    'date_posted': 'June 2, 2022'},

    {'author': 'Sarah Lee',
     'title': 'Blog Post 1',
     'content': 'This is my second blog post',
     'date_posted': 'June 2, 2022'}]

# importing dependencies
from datarail import app

# making sure we can run our app as a python script
if __name__ == "__main__":
    app.run(debug=True)