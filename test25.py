import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
email = "VasyPupkin@mail.ru"
password = "1q2w3e"


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome()
   pytest.driver = webdriver.Chrome("C:/projects/chrome/chromedriver.exe")
   # Переходим на страницу авторизации
   pytest.driver.get('https://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_show_all_pets():
   pytest.driver.maximize_window()
   # Вводим email
   # email_input.clear()
   pytest.driver.find_element(By.ID, 'email').send_keys(email)
   # Вводим пароль
   # password_input.clear()
   pytest.driver.find_element(By.ID, 'pass').send_keys(password)
   # Нажимаем на кнопку входа в аккаунт
   btn_submit = pytest.driver.find_element(By.XPATH, "//button[@type='submit']").click()
   time.sleep(5)
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   # Настраиваем неявные ожидания:
   pytest.driver.implicitly_wait(5)


   pytest.driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']").click()
   time.sleep(5)
   # Проверяем, что оказались на странице питомцев пользователя
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'


   # Ищем на странице все фотографии, имена, породу (вид) и возраст питомцев:
   images = pytest.driver.find_elements(By.XPATH, '//tbody/tr/th/img')
   names = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr>td[1]')
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr>td[2]' and 'tbody>tr>td[3]')

   # Проверяем, что на странице есть фотографии питомцев, имена, порода (вид) и возраст питомцев не пустые строки:
   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0


def test_show_my_pets():
   pytest.driver.maximize_window()
   # Вводим email, пароль, открываем главную страницу сайта
   pytest.driver.find_element(By.ID, 'email').send_keys(email)
   pytest.driver.find_element(By.ID, 'pass').send_keys(password)
   pytest.driver.find_element(By.XPATH, "//button[@type='submit']").click()

   # Настраиваем переменную явного ожидания:
   wait = WebDriverWait(pytest.driver, 5)

   # Проверяем, что мы оказались на главной странице сайта.
   assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

   pytest.driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']").click()
   time.sleep(5)
   # Проверяем, что оказались на странице с питомцами пользователя
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

   # Ожидаем в течение 5с, что на странице есть тег h2 с текстом "All" -именем пользователя
   # assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "All"))

   # Проверяем, что присутствуют все питомцы, для этого:
   #  находим кол-во питомцев по статистике пользователя и проверяем, что их число
   #  соответствует кол-ву питомцев в таблице
   pets_number = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
   #  pets_count = 25
   pets_count = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
   assert int(pets_number) == len(pets_count)
   print((int(pets_number)), "Питомцев")

   # Ищем в теле таблицы все фотографии питомцев и ожидаем, что все загруженные фото, видны на странице:
   image_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
   for i in range(len(image_my_pets)):
      if image_my_pets[i].get_attribute('src') == '':
         print(len(image_my_pets))
   assert wait.until(EC.visibility_of(image_my_pets[i]))

   # Ищем в теле таблицы все строки с полными данными питомцев (имя, порода, возраст, "х" удаления питомца):
   css_locator = 'tbody>tr'
   data_my_pets = pytest.driver.find_element(By.CSS_SELECTOR, (css_locator))
    # Ожидаем, что данные всех питомцев, найденных локатором css_locator = 'tbody>tr', видны на странице:
   for i in range(len(data_my_pets)):
      assert wait.until(EC.visibility_of(data_my_pets[i]))

   # Ищем в теле таблицы все фотографии питомцев и ожидаем, что все загруженные фото, видны на странице:
   image_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
   for i in range(len(image_my_pets)):
      if image_my_pets[i].get_attribute('src') != '':
         assert wait.until(EC.visibility_of(image_my_pets[i]))

   # Ищем все имена питомцев на странице:
   name_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr>td[1]')
   for i in range(len(name_my_pets)):
      assert wait.until(EC.visibility_of(name_my_pets[i]))

   # Ищем все породы питомцев на странице:
   type_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr>td[2]')
   for i in range(len(type_my_pets)):
      assert wait.until(EC.visibility_of(type_my_pets[i]))

   # Ищем все данные возраста питомцев на странице:
   age_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr>td[3]')
   for i in range(len(age_my_pets)):
      assert wait.until(EC.visibility_of(age_my_pets[i]))

   # Ищем на странице /my_pets всю статистику пользователя,
   # и извлекаем из полученных данных количество питомцев пользователя:
   all_statistics = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
   statistics_pets = all_statistics[1].split(" ")
   all_my_pets = int(statistics_pets[-1])

   # Проверяем, что количество строк в таблице с моими питомцами равно общему количеству питомцев,
   # указанному в статистике пользователя:
   assert(data_my_pets) == all_my_pets
   print(all_my_pets)

   # Проверяем, что хотя бы у половины питомцев есть фото:
   m = 0
   for i in range(len(image_my_pets)):
      if image_my_pets[i].get_attribute('src') != '':
         m += 1
      assert m >= all_my_pets / 2

   # Проверяем, что у всех питомцев есть имя:
   for i in range(len(name_my_pets)):
      assert name_my_pets[i].text != ''

   # Проверяем, что у всех питомцев есть порода:
   for i in range(len(type_my_pets)):
      assert type_my_pets[i].text != ''

   # Проверяем, что у всех питомцев есть возраст:
   for i in range(len(age_my_pets)):
      assert age_my_pets[i].text != ''

   # Проверяем, что у всех питомцев разные имена:
   list_name_my_pets = []
   for i in range(len(name_my_pets)):
      list_name_my_pets.append(name_my_pets[i].text,'')
   set_name_my_pets = set(list_name_my_pets)  # преобразовываем список в множество
   assert len(list_name_my_pets) == len(set_name_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть

   # Проверяем, что в списке нет повторяющихся питомцев:
   list_data_my_pets = []
   for i in range(len(data_my_pets)):
      list_data = data_my_pets[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
      list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем его в список
   set_data_my_pets = set(list_data_my_pets)  # преобразовываем список в множество
   assert len(list_data_my_pets) == len(set_data_my_pets)
