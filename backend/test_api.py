import requests

def test_testing_input():
    with app.test_client() as client:
        response = client.get('/testing-input?name=John')  # Send a GET request to '/testing-input?name=John'
        print("Test Testing Input:", response.status_code, response.data.decode())

def test_get_groupings():
    words = "apple, orange, banana, cherry, dog, cat, mouse, fish, car, bike, plane, boat, tree, flower, river, mountain"
    with app.test_client() as client:
        response = client.get(f'/get-groupings?words={words}')  # Send a GET request to '/get-groupings'
        print("Test Get Groupings:", response.status_code, response.data.decode())


def test_something():
    # Define the API endpoint (change port if needed)
    url = "http://127.0.0.1:5000/get-groupings"

    # Define the parameters for the GET request
    params = {
        "words": "apple,banana,carrot,dog,elephant,flute,grape,hat,ice,jaguar,kiwi,lion,mango,nectar,orange,pineapple"
    }

    # Send GET request to the API
    try:
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Print the response from the API
            print("API response:", response.json())  # Or response.text for raw text
        else:
            print("Error:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

if __name__ == "__main__":
    # test_testing_input()
    # test_get_groupings()
    test_something()
