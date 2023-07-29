import os
import requests
from jinja2 import Environment, FileSystemLoader

def fetch_data_from_api():
    api_url = "https://www.boredapi.com/api/activity"
    try:
        responses = []
        for _ in range(10): 
            response = requests.get(api_url)
            response.raise_for_status()
            responses.append(response.json())
        return responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []

def generate_pages():
    data = fetch_data_from_api()
    print(data)
    if not data:
        print("Data from API is empty or could not be fetched.")
        return

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    template_dir = os.path.join(script_dir, "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("page_template.html")

    for i, activity_data in enumerate(data):
        rendered_page = template.render(activity_data=activity_data)
        filename = os.path.join(script_dir, f"activity{i + 1}.html")
        with open(filename, "w") as file:
            file.write(rendered_page)

        print(f"Page {i + 1} generated.")

if __name__ == "__main__":
    generate_pages()
