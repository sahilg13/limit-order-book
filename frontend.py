from flask import Flask, request, redirect
from processing import init_lob, gen_order, process_order, reformat_lob, reformat_order, get_spread

# FRONT END #

# Initial state of variables displayed on website
lob = init_lob()
order = gen_order()
spread = get_spread(lob)

# Defining a Flask application
app = Flask(__name__)
app.config["DEBUG"] = True

# Displaying the main page
@app.route("/", methods=["GET", "POST"])
def hello_world():

    if request.method == "POST":
        # We handle the appropriate post action
        global lob, order, spread

        if request.form.get("submit_button") == "Process Order":
            # We process the randomly generated order and redirect
            lob = process_order(lob, order)
            spread = get_spread(lob)
            order = gen_order()

            return redirect("http://sahilg13.pythonanywhere.com")
        else:
            # We clear the book and redirect
            lob = init_lob()
            spread = get_spread(lob)

            return redirect("http://sahilg13.pythonanywhere.com")

    # We display all elements of our webpage including the order and book
    return '''
        <html>
            <head>
                <title>Limit Order Book Simulator</title>
            </head>
            <h1>Limit Order Book Simulator</h1>
            <body style="background-color:grey;">
                <form method="post" action=".">
                    <h2 style="display:inline;">Randomly Generated Order</h2>
                    <input type="submit" style="background-color: rgb(159, 183, 141); border: 3px solid rgb(73, 136, 85);" name="submit_button" value="Process Order" />
                    <br>
                    <br>
                </form>
            </body>
        </html>
    ''' + "<style type=\"text/css\">" + "\n" + "\t" + "table    {border:ridge 5px black; background-image:url(https://img.rawpixel.com/s3fs-private/rawpixel_images/website_content/v1008-22-c-x.jpg?w=1200&h=1200&dpr=1&fit=clip&crop=default&fm=jpg&q=75&vib=3&con=3&usm=15&cs=srgb&bg=F4F4F3&ixlib=js-2.2.1&s=34830f4633b34d78b97cf2bd6ff017c6);}" + "\n" + "\t" + "table td {border:inset 1px #000;}" + "\n" + "</style>" + "\n" + reformat_order(order).to_html(index=False, na_rep = "-") + '''
        <html>
            <br>
            <form method="post" action=".">
                <h2 style="display:inline;">Limit Order Book</h2>
                <input type="submit" style="background-color: rgb(159, 183, 141); border: 3px solid rgb(73, 136, 85);" name="submit_button" value="Clear Book" />
                <br>
                <br>
                <a>Current Bid-Ask Spread: {spd}</a>
            </form>
        <html>
    '''.format(spd = spread) + reformat_lob(lob).to_html(index=False, na_rep = "-")