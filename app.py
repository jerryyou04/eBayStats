from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# HTML template for the form and results display
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>eBay Price Check</title>
    <style>
        html {
            height: 100%;
        }

        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh; /* Make the body take at least the full viewport height */
            margin: 0;
        }

        body {
            font-family: 'Lato', sans-serif;
        }
        h1, h2, h3 {
            color: rgb(204, 99, 13);
        }
        body, html {
            margin: 0;
            padding: 0;
        }

        header {
            height: 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #292a2b;
            padding: 10px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-top: 5px solid rgb(204, 99, 13);
        }
        @media screen and (max-width: 600px) {
            footer {
                display: none;
            }
            
            header {
                padding: 10px;
            }

            .brand {
                font-size: 0.6em;
            }

            .header-logo {
                height: 30px;
            }

            .button {
                font-size: 0.3em;
            }

            .brand-container {
                font-size: 0.6em;
                display: flex;
                align-items: center;
            }
        }

        .brand {
            font-size: 1.5em;
            font-weight: bold;
            color: rgb(255, 255, 255);
            text-decoration: none;
        }
        .header-logo {
            height: 40px;
            width: auto;
            margin-right: 10px;
        }
        .brand-container {
            display: flex;
            align-items: center;
        }
        .brand:hover, nav a.button:hover {
            text-decoration: none;
            color: rgb(255, 255, 255);
        }
        nav a.button {
            margin-left: 10px;
            text-decoration: none;
            color: #ffffff;
            background-color: transparent;
            font-weight: bold;
            font-family: 'Lato', sans-serif;
        }
        .main-content {
            flex: 1;
            padding: 20px;
        }
        .about-section {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        footer {
            background-color: #292a2b;
            color: white;
            text-align: center;
            padding: 10px 0;
            bottom: 0;
            width: 100%;
        }
        input[type="text"] {
            width: 80%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            width: 20%;
            background-color: rgb(204, 99, 13);
            color: white;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        input[type="submit"]:hover {
            background-color: rgb(226, 108, 30);
        }
        .results p {
            color: #fff;
            background-color: rgb(58, 53, 53);
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .price-info a {
            color: #FFF; /* This ensures the hyperlink text is white */
            text-decoration: none; /* Optionally removes the underline from links */
        }

        .price-info a:hover {
            color: rgb(226, 108, 30);  /* Restores underline on hover for visual feedback */
        }

        .price-info {
            color: #FFF; /* White text color for readability */
            background-color: #292a2b; /* Dark background for contrast */
            padding: 8px 12px; /* Padding for spacing inside the elements */
            border-radius: 4px; /* Rounded corners for a modern look */
            margin: 10px 0; /* Margin for spacing between each element */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Subtle shadow for depth */
            display: block; /* Makes the background only as wide as the content */
        }
        .scrollable-section {
            min-height: 30vh;
            overflow-y: auto; /* Enables vertical scrolling if the content overflows */
            /* Add other styles as needed */
        }
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        ::-webkit-scrollbar-thumb {
            background: rgb(63, 62, 62);
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
    </style>
    
</head>
<body>
    <header>
        <div class="brand-container">
            <a href="/" class="brand">eBay</a>
        </div>
    </header>

    <div class="main-content">
        <div class="about-section">
            <h2>Search eBay for Prices</h2>
            <form action="/" method="post">
                Search Term: <input type="text" name="search_term" required><br>
                <input type="submit" value="Submit">
            </form>
            {% if final_average %}
                <p class="price-info">Search Term: {{ search_term }}</p>
                <p class="price-info">Filtered Final Average: C ${{ final_average }}</p>
                <p class="price-info">Lowest Price in Filtered List: C ${{ lowest_price }}</p>
                <p class="price-info">Highest Price in Filtered List: C ${{ highest_price }}</p>
                <p class="price-info">Total Prices Analyzed: {{ total_prices }}</p>
                <p class="price-info">URL accessed by bot: <a href="{{ url }}" target="_blank">{{ url }}</a></p>

            
            {% endif %}
        </div>
    </div>
    <div class="scrollable-section"></div>
    <footer>
        <p>&copy; eBay App</p>
    </footer>
</body>
</html>
"""

def get_average_used_price_ebay(search_term):
    url = f"https://www.ebay.ca/sch/i.html?_from=R40&_nkw={search_term}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        prices = soup.find_all("span", class_="s-item__price")
        prices_numbers = [float(price.text.replace('C $', '').replace('$', '').replace(',', '').strip()) for price in prices if 'to' not in price.text]
        
        if prices_numbers:
            average_price = sum(prices_numbers) / len(prices_numbers)
            filtered_prices = [price for price in prices_numbers if price <= 1.5 * average_price and price >= 0.3 * average_price]
            final_average = round(sum(filtered_prices) / len(filtered_prices), 2) if filtered_prices else None
            lowest_price = round(min(filtered_prices), 2) if filtered_prices else None
            highest_price = round(max(filtered_prices), 2) if filtered_prices else None

            return final_average, lowest_price, highest_price, len(prices_numbers), url
        else:
            return None, None, None, 0, None
    except requests.RequestException as e:
        print(f"Error during requests to {url} : {str(e)}")
        return None, None, None, 0, None

@app.route("/", methods=["GET", "POST"])
def price_filter():
    if request.method == "POST":
        search_term = request.form["search_term"]
        print("Searching for: ", search_term)
        final_average, lowest_price, highest_price, total_prices, url = get_average_used_price_ebay(search_term)
        return render_template_string(HTML, final_average=final_average, lowest_price=lowest_price, highest_price=highest_price, total_prices=total_prices, search_term = search_term, url = url)
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
