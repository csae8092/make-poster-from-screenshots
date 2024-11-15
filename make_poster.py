import openai
import os
import requests

# Set your OpenAI API key
openai.api_key = os.environ.get("CHATGPT_API_KEY")

# Folder containing images
image_folder = "screenshots"
# GitHub README URL
readme_url = (
    "https://raw.githubusercontent.com/acdh-oeaw/dse-static-cookiecutter/main/README.md"
)


# Step 1: Load images from folder
def load_images(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(folder_path, filename)
            images.append(file_path)
    return images


# Step 2: Download text from GitHub README
def fetch_readme_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Could not fetch README from GitHub")


# Step 3: Create prompt and send request to OpenAI for poster creation
def create_poster_prompt(title, text, image_urls):
    prompt = f"Create a poster titled '{title}' that visually incorporates the following text:\n\n{text[:500]}...\n\nAnd integrates the following images:\n"
    prompt += "\n".join(image_urls)
    return prompt


def upload_images_and_create_poster():
    # Fetch README text
    readme_text = fetch_readme_text(readme_url)

    # Load images from folder
    images = load_images(image_folder)
    image_urls = []

    # Upload images to OpenAI
    for image_path in images:
        with open(image_path, "rb") as image_file:
            response = openai.Image.create(file=image_file)
            image_urls.append(response["data"]["url"])

    # Create poster with title and README text
    title = "dse-static-cookiecutter"
    prompt = create_poster_prompt(title, readme_text, image_urls)
    poster = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
    return poster["data"][0]["url"]


# Run the script
if __name__ == "__main__":
    poster_url = upload_images_and_create_poster()
    print("Poster created successfully!")
    print("Poster URL:", poster_url)
