import requests

# def test_testing_input():
#     with app.test_client() as client:
#         response = client.get('/testing-input?name=John')  # Send a GET request to '/testing-input?name=John'
#         print("Test Testing Input:", response.status_code, response.data.decode())

# def test_get_groupings():
#     words = "Apple, Pear, Orange, Banana, Rose, Tulip, Lily, Daisy, Violin, Piano, Guitar, Drum, Red, Green, Blue, Yellow"
#     with app.test_client() as client:
#         response = client.get(f'/get-groupings?words={words}')  # Send a GET request to '/get-groupings'
#         print("Test Get Groupings:", response.status_code, response.data.decode())


def test_something():
    # Define the API endpoint (change port if needed)
    url = "http://127.0.0.1:5000/get-groupings"

    # Define the parameters for the GET request
    params = {
        "words": "Apple, Pear, Orange, Banana, Rose, Tulip, Lily, Daisy, Violin, Piano, Guitar, Drum, Red, Green, Blue, Yellow"
    }

    # Send GET request to the API
    try:
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Print the JSON response if the route returns JSON
            try:
                print("API response:", response.json())  # Use response.json() if JSON is returned
            except ValueError:
                print("API response (non-JSON):", response.text)
        else:
            print("Error:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

if __name__ == "__main__":
    test_something()
