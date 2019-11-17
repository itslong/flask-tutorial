from app import app

"""
A common pattern with decorators is to use them to register functions as callbacks for certain events. 
In this case, the @app.route decorator creates an association between the URL given as an argument and the function. 
In this example there are two decorators, which associate the URLs / and /index to this function. 
This means that when a web browser requests either of these two URLs, 
Flask is going to invoke this function and pass the return value of it back to the browser as a response.
"""

@app.route('/')
@app.route('/index')

def index():
    return 'Hello, World'
