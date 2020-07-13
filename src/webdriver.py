import time
import pyautogui
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from src.skribbl_specific import *
from src.image import load_image, SCALE, process_color

# Prevent driver from being garbage collected when return from function
web_driver = None
search_str1 = "https://www.google.com/search?q="
search_str2 = "&tbm=isch&tbs=itp%3Aclipart"


class WebDriver:
    def __init__(self, empty=False, **kw):
        self.kw = kw
        if empty:
            self.driver = None
        else:
            try:
                self.driver = webdriver.Chrome()
            except WebDriverException as wde:
                print('Error: {}'.format(wde))
                print('Installing ChromeDriver...')
                from webdriver_manager.chrome import ChromeDriverManager
                self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def answer_cookies(self, cookies):
        if cookies:
            # accept cookies
            _wait_click(self.driver, xPaths['acp_cookie'])
        else:
            # deny cookies
            _wait_click(self.driver, xPaths['dny_cookie'])

    def input_profile(self, **kw):
        _fill_text(self.driver, xPaths['login_name'], self.kw.get('name'))
        _select_option(self.driver, xPaths['login_lang'], self.kw.get('language'))

    def click_play(self):
        _click_xpath(self.driver, xPaths['login_play'])

    def click_create(self):
        _click_xpath(self.driver, xPaths['create'])

    def auto_fill_create(self, **kw):
        startGameBtn = _wait(self.driver, xPaths['lobby_play'])
        _select_option(self.driver, xPaths['set_rounds'], str(10))
        _select_option(self.driver, xPaths['set_times'], str(180))
        _select_option(self.driver, xPaths['lobby_lang'], self.kw.get('language'))
        _fill_text(self.driver, xPaths['custom_wds'], '')
        _checkbox(self.driver, xPaths['cus_wds_ex'], check=False)
        return startGameBtn

    def close_all(self):
        self.driver.close()


def open_skribbl(url="https://skribbl.io/", accept_cookie=False, **kw):
    global web_driver
    web_driver = WebDriver(empty=False, **kw)
    web_driver.driver.get(url)
    web_driver.answer_cookies(cookies=accept_cookie)
    web_driver.input_profile()
    return web_driver


# play a random game
def play_random_game(**kw):
    global web_driver
    web_driver = open_skribbl(**kw)
    web_driver.click_play()
    return web_driver


# private room create
def create_private_game(**kw):
    global web_driver
    web_driver = open_skribbl(**kw)
    web_driver.click_create()
    web_driver.auto_fill_create()
    return web_driver


# private room join
def join_private_game(url, **kw):
    global web_driver
    web_driver = open_skribbl(url, **kw)
    web_driver.click_play()
    return web_driver


def draw_image(img):
    global web_driver
    if web_driver is None:
        web_driver = WebDriver(empty=True)
        return
    driver = web_driver.driver
    x0, y0 = draw_pad_loc['x0'], draw_pad_loc['y0']
    rows, cols = img[0].shape
    driver.maximize_window()
    # tools/size selection
    _click_xpath(driver, xPaths['pen'])
    _click_xpath(driver, xPaths['size16'])
    # click to focus on game window
    pyautogui.click(x=430, y=20)
    # scroll to bottom
    pyautogui.click(x=1891, y=117)
    html = driver.find_element_by_xpath(xPaths['html'])
    html.send_keys(Keys.PAGE_DOWN)
    for (key, color) in color_xPath.items():
        _click_xpath(driver, color)
        last = False
        for row in range(rows):
            for col in range(cols):
                if img[key][row, col] and not last:
                    pyautogui.moveTo(x=((col*SCALE)+x0), y=(row*SCALE)+y0)
                    pyautogui.mouseDown()
                    last = True
                elif not img[key][row, col] and last:
                    pyautogui.moveTo(x=(((col-1)*SCALE)+x0), y=(row*SCALE)+y0)
                    pyautogui.mouseUp()
                    last = False


def search_image(item):
    image = None
    temp_driver = WebDriver()
    temp_driver.driver.get(search_str1 + str(item) + search_str2)
    img = WebDriverWait(temp_driver.driver, 20).until(ec.visibility_of_element_located((
        By.XPATH, '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')))
    # attrs = temp_driver.driver.execute_script(
    #     'var items = {}; '
    #     'for (index = 0; index < arguments[0].attributes.length; ++index) '
    #     '{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; '
    #     'return items;', img)
    # print(attrs)
    for i in range(20):
        try:
            src = str(img.get_attribute('src'))
            print(src)
            if src.find('http') == -1:
                time.sleep(1)
                continue
                # # will get image from base64
                # encoded_src = src.split("base64,", 1)[1]
                # decoded_src = base64.b64decode(encoded_src)
                # image = Image.open(BytesIO(decoded_src))
            else:
                image = load_image(src, (780 / SCALE, 600 / SCALE))
                # image.show()
                break
        except (TypeError, RequestException) as e:
            print(f'{i}. Error: {e}')
    temp_driver.driver.quit()
    if image is not None:
        image_dict = process_color(image)
        return image_dict
    return None


def _click_xpath(driver, xpath):
    driver.find_element_by_xpath(xpath).click()


def _fill_text(driver, xpath, text):
    if text is not None:
        element = driver.find_element_by_xpath(xpath)
        element.clear()
        element.send_keys(text)


def _select_option(driver, xpath, option):
    element = Select(driver.find_element_by_xpath(xpath))
    element.select_by_visible_text(option)


def _wait_click(driver, xpath):
    _wait(driver, xpath).click()


def _wait(driver, xpath):
    return WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, xpath)))


def _checkbox(driver, xpath, check):
    checkbox = driver.find_element_by_xpath(xpath)
    if check:
        if not checkbox.is_selected():
            checkbox.click()
    else:
        if checkbox.is_selected():
            checkbox.click()
