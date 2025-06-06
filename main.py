import openai
import pyautogui
from time import sleep 
import requests
import os
import shutil


# Variables and API keys: 

# Set your API key here
openai.api_key = 'sk-proj-lNdUARSwqlfOEmWScKuJT3BlbkFJpPA0ljM0bnDDrNmUnrsh'
PEXELS_API_KEY = 'hDRHxDV8nBC29pk2Q76sG2ucY1awuF5m50gEN6wocSv3F0dP13Cu6pei'

# Amount of videos the API Returns
NUMBER_OF_VIDEOS = 5

# ChatGPT
def generate_response_script(prompt):
    # Generates a response from chatGPT for a script
    try: 
        response = openai.chat.completions.create(

            model="gpt-4o",  # Custom model name
            messages=[
                {"role": "system", "content": "You are a scriptwriter for a youtube shorts channel called personality pops. Your job is to create a script and theme based on psychological typologies and personality frameworks. In brackets include the type of picture you want in the background. Keep it 20 seconds long and try to engage feeling to the listener and keep ideas"},
                {"role": "user", "content": prompt}], max_tokens=250
    )  
         # Extract and return the generated message content
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
def generate_response_theme(prompt):
    # Returns One word for a theme
    try: 
        Rules = openai.chat.completions.create(

            model="gpt-4o",  # Custom model name
            messages=[
                {"role": "system", "content": "You are in a program. You're job is to return one word for a theme kinda summarizing"},
                {"role": "user", "content": content}], max_tokens=25)  
     # Extract and return the generated message content
        return Rules.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
    

# Pixea
def download_pixeas_video(url, dest_folder='videos'):
    # Downloads the video onto your computer

    os.makedirs(dest_folder, exist_ok=True)
    response = requests.get(url, stream=True)
    file_name = os.path.join(dest_folder, url.split('/')[-1])
    
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return file_name

def search_pexels_videos(query, num_videos=5):
    # Searches the Internet On pixea for the video
    url = f'https://api.pexels.com/videos/search?query={query}&per_page={num_videos}'
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_pexels_videos(query, num_videos=5):
    videos_info = search_pexels_videos(query, num_videos)
    video_files = []
    
    for video in videos_info['videos']:
        video_url = video['video_files'][0]['link']
        video_file = download_pixeas_video(video_url)
        video_files.append(video_file)
        print(f"Downloaded {video_file}")
    return video_files
# PyAutoGUI for automation: 

def open_clipchamps(text): 
    # Open ClipChamps
    pyautogui.press('win')
    pyautogui.typewrite("Clipcha")
    pyautogui.press('enter')
    sleep(8.5)
    # Creates new Project when open
    pyautogui.moveTo(500, 240)
    pyautogui.click()
    sleep(2)
    # Open folder in clip champs
    pyautogui.moveTo(225, 110)
    pyautogui.click()
    sleep(2)

    pyautogui.moveTo(470, 300)
    pyautogui.click()


    # Select all and put it inside media library
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press("enter")

def delete_videos(folder='videos'):
    # Check if the folder exists
    if os.path.exists(folder):
        # Iterate over all the files in the folder
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                # Check if it's a file and then delete it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
                # Check if it's a directory and then delete it
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted directory: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The folder '{folder}' does not exist.")

   
    
def main(): 
    script = generate_response_script(prompt="Create a Video about the 16 personality Types")
    theme = generate_response_theme(script)
    video_file = get_pexels_videos(theme, NUMBER_OF_VIDEOS)
    open_clipchamps(script)

    try: 
        Answer = input("When Finished Say Yes or No: ")
        if Answer.lower() == "yes":
            delete_videos()
        else: 
            raise ValueError
    except ValueError: 
           print(f"Try Again")

    


    COORDINATES = False
    while COORDINATES: 
        current_mouse_x, current_mouse_y = pyautogui.position()
        print(f"Current mouse position: ({current_mouse_x}, {current_mouse_y})")


if __name__ == '__main__':
    main()