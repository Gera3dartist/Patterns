# Redirect is used to forward user to full url if he came
#   with shortened
# Request encapsulates HTTP request

from flask import redirect, render_template, request, Flask
from werkzeug.exceptions import BadRequest, NotFound
import models



__author__ = 'agerasym'


# Initialize Flask application
app = Flask(__name__, template_folder='views')


@app.route("/")
def index():
    """Renders main page"""
    return render_template('main_page.html')

@app.route("/shorten/")
def shorten():
    """Returns short_url of requested full_url."""
    # Validate user input
    full_url = request.args.get('url')
    if not full_url:
        raise BadRequest()

    # Model returns object with short_url property
    url_model = models.Url.shorten(full_url)

    # Pass data to view and call its render method
    short_url = request.host + '/' + url_model.short_url
    return render_template('success.html', short_url=short_url)

@app.route('/<path:path>')
def redirect_to_full(path=''):
    """
    Gets short url and redirect to corresponding full url
    if found

    """
    # Models returns object with full property
    url_model = models.Url.get_by_short_url(path)

    # Validate model return
    if not url_model:
        raise NotFound()

    return redirect(url_model.full_url)


if __name__ == "__main__":
    app.run(debug=True)