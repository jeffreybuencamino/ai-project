import requests
from bs4 import BeautifulSoup

url = "https://www.chewy.press/"
response = requests.get(url)

if response.status_code == 200:
    print("Request was successful!\n")
    soup = BeautifulSoup(response.content, 'html.parser')
    print(response.text)
    
    # Extract visible text (strips most HTML tags)
    print(soup.get_text(strip=True))
    
    # OR: Get the page title
    print("\nPage Title:", soup.title.string if soup.title else "No title found")

    # OR: Print all H1 headers
    print("\nH1 Tags:")
    for h1 in soup.find_all('h1'):
        print(" -", h1.get_text(strip=True))

else:
    print(f"Request failed with status code: {response.status_code}")
