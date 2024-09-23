import time
import json
import pandas as pd
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unicodedata
import random
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

BANG_XOA_DAU = str.maketrans(
    "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴáàảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ",
    "A"*17 + "D" + "E"*11 + "I"*5 + "O"*17 + "U"*11 + "Y"*5 + "a"*17 + "d" + "e"*11 + "i"*5 + "o"*17 + "u"*11 + "y"*5
)
def zoom_out_browser():
    # Đợi một chút để đảm bảo trình duyệt đã mở hoàn toàn
    time.sleep(2)
    
    # Thực hiện thao tác Ctrl và dấu trừ 3 lần để thu nhỏ
    for _ in range(6):
        pyautogui.hotkey('ctrl', '-')
        time.sleep(0.5)
def configure_driver():
    #Configurations

     # Đường dẫn đến WebDriver
    webdriver_path = ".\\chromedriver.exe"
    chrome_options = Options()

    # Tắt thông báo Chrome - chặn pop-up
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument('--window-size=800,600')
    # Đặt vị trí cửa sổ ở ngoài màn hình chính
    #chrome_options.add_argument('--window-position=2000,0')
    #chrome_options.add_extension("F:\GlobalTech\Stands AdBlocker - Chrome Web Store 2.1.24.0.crx")

    # Sử dụng profile đã có sẵn: 
    # để lưu trạng thái đăng nhập + dùng tool chặn quảng cáo set up sẵn trên Chrome
    # user_profile = "C:\\Users\\21521\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 5"
    # chrome_options.add_argument("user-data-dir=" + user_profile)

    # (Tùy chọn) Chạy Chrome ở chế độ không hiển thị giao diện (chạy ngầm)
    #chrome_options.add_argument("--headless")

    # Khởi tạo dịch vụ và trình duyệt
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def fill_in_in4(driver, ele, data):
    try:
        driver.find_element(By.CSS_SELECTOR, ele).send_keys(data)
    except Exception as e:
        print(e)

def click_and_fill_in_text_box(driver, ele, text):
    '''
    Function to click text box and fill in text
    After that, click 'Tab' button

    '''
    ele.click()
    driver.find_element(By.CSS_SELECTOR, "input[class='select2-search__field']").send_keys(text)
    time.sleep(1)
    # Click Tab
    driver.find_element(By.CSS_SELECTOR, "input[class='select2-search__field']").send_keys(Keys.TAB)

def sleep(amount):
    time.sleep(amount)

def create_account(driver, personal_data):
    try:
        # Main container
        
        #register_form = driver.find_element(By.CSS_SELECTOR,"[class=' w-full'][id='shRegisterForm'])"))
        combo_box_eles = driver.find_elements(By.CSS_SELECTOR,"span[class='select2 select2-container select2-container--default']")

        #Define All Elements

        full_name_ele = "input[type='text'][name='fullName']"
        cluster_ele = combo_box_eles[0]
        university_ele = combo_box_eles[1]
        major_ele = "input[type='text'][name='major']"
        graduation_year_ele = combo_box_eles[2]
        desired_career_ele = combo_box_eles[3]
        student_id_ele = "input[type='text'][name='studentId']"
        date_of_birth_ele = "input[type='text'][name='birth']"
        mobile_phone_ele = "input[type='text'][name='phoneNumber']"
        personal_email_ele = "input[type='text'][name='email']"
        password_ele = "input[type='password'][name='password']"
        confirm_password_ele = "input[type='password'][name='passwordConfirm']"
        checkbox_confirm_ele = "input[type='checkbox'][id='agreeTerms']"
        signup_ele = "button[type='submit'][id='shRegisterBtn']"


        # Action
        # Full Name
        fill_in_in4(driver, full_name_ele, personal_data['hoten_upper'])
        #sleep(3)
        # Cluster
        click_and_fill_in_text_box(driver, cluster_ele, 't')
        sleep(5) # Check if internet is slow
        # University
        click_and_fill_in_text_box(driver, university_ele, 'tho')
        #sleep(2)
        # Major - Random Gen
        fill_in_in4(driver, major_ele, personal_data['chuyennganh'])
        # Graduation  - Check MSSV + Random - Graduation - 2 so dau >= 4
        click_and_fill_in_text_box(driver, graduation_year_ele, str(personal_data['namtotnghiep']))
        #sleep(3)
        # Desired career - Random
        click_and_fill_in_text_box(driver, desired_career_ele, personal_data['nganhnghe'])
        # Student ID:
        fill_in_in4(driver, student_id_ele, personal_data['masv'])
        sleep(2)
        # Date of birth - Gen random 'mm/dd/yyyy' - dua vao mssv
        fill_in_in4(driver, date_of_birth_ele, personal_data['ngaysinh'])
        #sleep(2)
        # Mobile phone
        fill_in_in4(driver, mobile_phone_ele, personal_data['sdt'])
        #sleep(3)
        # Personal email - Gen from hoten
        fill_in_in4(driver, personal_email_ele, personal_data['email'])
        #sleep(3)
        # Password and Retype - Ramdomly Gen - At least 8 char
        fill_in_in4(driver, password_ele, personal_data['password'])
        fill_in_in4(driver, confirm_password_ele, personal_data['password'])

        # Agree terms
        driver.find_element(By.CSS_SELECTOR, checkbox_confirm_ele).click()
        sleep(100)
        # Sign Up
        driver.find_element(By.CSS_SELECTOR, signup_ele).click()
        sleep(25) #waiting for create successfully

        # Tmp
        # cluster_ele = "span[class='select2-selection__rendered'][id='select2-clusterId-container']"
        # university_ele = "span[class='select2-selection__rendered'][id='select2-clusterId-container']"
        return True
    except Exception as e:
        #print(e)
        return False
    
def xoa_dau(txt: str) -> str:
    if not unicodedata.is_normalized("NFC", txt):
        txt = unicodedata.normalize("NFC", txt)
    return txt.translate(BANG_XOA_DAU)

def generate_email(text, num):
    # Xóa khoảng trắng và chuyển thành chữ thường
    text = xoa_dau(text)
    text = text.replace(" ", "").lower()
    num = str(num)[5:]
    # Ghép chuỗi và số để tạo email
    email = f"{text}{num}@gmail.com"
    return email

def add_0_sdt(sdt):
    if not str(sdt).startswith('0'):
        sdt = str('0') + str(sdt)
    return sdt

def login(driver, email, password):
    domain = "https://starawards.vn/login"
    driver.get(domain)

    #fill in email
    driver.find_element(By.CSS_SELECTOR, "input[type='text'][name='email']").send_keys(email)

    #fill in password
    driver.find_element(By.CSS_SELECTOR, "input[type='password'][name='password']").send_keys(password)
    #click login
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit'][name='loginBtnSubmit']").click()

def join_competition(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "div.rulesWrapper.containerV2.show div div:nth-child(2) a").click()
    except:
        return None

def random_answer():
    return random.randint(1, 4)

def go_next_quiz(driver, next_quiz_number):
    driver.find_element(By.CSS_SELECTOR, f"span[id='laraQuestionItemDot-{next_quiz_number}']").click()

def answer_quiz(driver, quiz_number):

    # Wait for the quiz container to be present
    # Wait for the quiz container to be present
    ele = f"div[id='laraQuestionItem-{quiz_number}']"
    wait = WebDriverWait(driver, 10)
    main_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ele)))

    # Find all label elements containing the radio buttons
    labels = main_container.find_elements(By.CSS_SELECTOR, "div.formRadioAnswers label")

    if not labels:
        print(f"No radio buttons found for quiz {quiz_number}")
        return

    # Choose a random label
    chosen_label = random.choice(labels)

    # Scroll the page to bring the element into view
    actions = ActionChains(driver)
    actions.move_to_element(chosen_label).perform()

    # Wait for a short time to ensure the page has settled after scrolling
    time.sleep(1)

    # Wait for the label to be clickable
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div[id='laraQuestionItem-{quiz_number}'] div.formRadioAnswers label")))

    # Try to click the label
    try:
        chosen_label.click()
    except Exception as e:
        #print(f"Failed to click label directly: {e}")
        # If direct click fails, try clicking the radio button inside the label
        try:
            radio_button = chosen_label.find_element(By.TAG_NAME, "input")
            radio_button.click()
        except Exception as e:
            print(f"Failed to click radio button: {e}")
            # If both attempts fail, try using JavaScript to click
            driver.execute_script("arguments[0].click();", chosen_label)

    #print(f"Answered quiz {quiz_number}")

def final_submit(driver):
    driver.find_element(By.CSS_SELECTOR, "div.flex.w-full.justify-center.items-center a").click()
    driver.find_element(By.CSS_SELECTOR, "button[id='testFormBtn']").click()

def pipeline(driver, email, password):
    try:
        login(driver, email, password)
    except Exception:
        return 'Login False'
    
    try:
        join_competition(driver)
        enough = "You have completed 3 examinations"
        time.sleep(3)
        if driver.find_element(By.CSS_SELECTOR,
           "div[class='flex flex-col md:flex-row items-center justify-center gap-[15px] md:gap-[30px] mx-[20px]'] a").text.strip()==enough:
            return -1
        for quiz_number in range(1, 41):
            answer_quiz(driver,quiz_number)
            if quiz_number < 40:
                go_next_quiz(driver,quiz_number+1)
        time.sleep(400)
        final_submit(driver)
        print('Done')
        return 1
    except:
        return 'Take Test Failed'