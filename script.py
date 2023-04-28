from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from googletrans import Translator
from docx.shared import Inches
from docx import Document
from PIL import Image
import os
import glob
import re
import pyautogui
import threading
import time



# Path to directory containing image files
image_dir = "/home/jonathan/project/photos"

#path to directory to save the word files
txt_dir ="/home/jonathan/project/txt2"

# Find all image files in directory
image_files = glob.glob(os.path.join(image_dir, "*.jpg"))


# Set up the webdriver
driver = webdriver.Chrome()


# Set the browser window size to the maximum screen size
driver.set_window_size(1920, 1080)

# Maximize the browser window
driver.maximize_window()

# Send a GET request to the website and retrieve the HTML content
url = 'https://www.onlineocr.net/'
driver.get(url)

counter =0 

# loop on all image files
for image_file in image_files:

    # Get the name of the image file without the extension
    image_name = os.path.splitext(os.path.basename(image_file))[0]

    
    # Find the input tag by ID
    input_tag = driver.find_element(By.ID, "fileupload")

# Upload the file to the website

    # Get the absolute path of the image file
    file_path = os.path.abspath(image_file)
    input_tag.send_keys(file_path)

    #get the language dropdown menu
    language_dropdown = driver.find_element(By.ID,"MainContent_comboLanguages")

    # Create a Select object from the dropdown element
    dropdown = Select(language_dropdown)

    # Select an option by value
    dropdown.select_by_value("GERMAN")


    # Find the button by ID
    button = driver.find_element(By.ID, "MainContent_btnOCRConvert")

    # Wait for the button to be clickable
    wait = WebDriverWait(driver, 60)
    wait.until(EC.element_to_be_clickable((By.ID, "MainContent_btnOCRConvert")))


    # Click the button
    button.click()

    time.sleep(10)

    # wait for the textarea element to become visible
    wait = WebDriverWait(driver, 100)
    text_area = wait.until(EC.visibility_of_element_located((By.ID, "MainContent_txtOCRResultText")))

    # extract the text from the textarea element
    text = text_area.get_attribute("value")

    #translate the text 

    MAX_RETRIES = 3
    WAIT_TIME = 1
    
    # Create a translator object
    translator = Translator()

    for i in range(MAX_RETRIES):
        try:
            # Translate the text to English
            translate_text = translator.translate(text, dest='en').text
            break
        except Exception as e:
            print(f"Translation failed, retrying ({i+1}/{MAX_RETRIES})...")
            time.sleep(WAIT_TIME)

    # Use regex to match the last numbers in the string
    match = re.search(r'\d+$', translate_text)

    if match:
        # Extract the matched numbers as a string
        numbers = match.group(0)

        page_num = f"Page Number  {numbers} "
        translate_text = translate_text.replace(numbers, '')

        # Combine the original string and the page number
        translate_text = translate_text +'\n' + page_num

    # Print the combined string
    print(translate_text)


    counter = counter+1
    print("counter" , counter)
    
    # Create a Word document with the same name as the image
    doc_file = os.path.join(txt_dir, image_name + ".docx")
    document = Document()

    # Add text to the document
    document.add_paragraph(translate_text)

    # Save the document
    document.save(doc_file)

#Close the webdriver
driver.quit()