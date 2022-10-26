import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/Users/hp_Nataly/PycharmProjects/pythonProject4/chromedriver_win32//chromedriver.exe')
    pytest.driver.get('https://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()

def test_show_my_pets():
    # Email
    pytest.driver.find_element_by_id('email').send_keys('nataly-n77@mail.ru')
    # Пароль
    pytest.driver.find_element_by_id('pass').send_keys('arus2480')
    # Неявное ожидание
    pytest.driver.implicitly_wait(20)
    # Нажать на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Указать переменную явного ожидания:
    wait = WebDriverWait(pytest.driver, 5)
    # Ожидаем в течение 5с, что на странице есть тег h1 с текстом "PetFriends"
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))
    # Нажать на кнопку перехода к выбору списка питомцев
    pytest.driver.find_element_by_xpath('//button[@class="navbar-toggler"]').click()
    # Нажать на кнопку для перехода к списку своих питомцев
    pytest.driver.find_element_by_xpath('//*[@href="/my_pets"]').click()
    # Проверяем, что мы оказались на странице пользователя.
    # Ожидаем в течение 5с, для появления тега h2 с именем пользователя
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "Наталья"))
    # Получаем все фотографии питомцев на странице
    images = pytest.driver.find_elements_by_css_selector('div th > img')
    # Получаем всю информацию о питомцах на странице
    pets_info = pytest.driver.find_elements_by_css_selector('div td')
    # Сортируем информацию о питомцах и записываем в отдельные переменные
    names = pets_info[::4]
    breeds = pets_info[1::4]
    ages = pets_info[2::4]
    # Получаем информацию профиля и записываем в переменную
    amount = pytest.driver.find_elements_by_css_selector('html > body > div > div > div')
    # Создаём переменную для подсчёта количества питомцев с фото
    pets_with_photo = 0
    # Создаём пустой список, в которые будем записывать имена всех питомцев
    list_names = []
    # Создаём пустой список, в который будем записывать всю информацию о каждом питомце
    all_pets = []

    for i in range(len(names)):
        # Проверяем, какое количество питомцев с фотографией и записываем количество в переменную
        if images[i].get_attribute('src') != '':
            pets_with_photo += 1
        # Проверяем, что у всех питомцев присутствует имя
            assert names[i].text != ''
            # Проверяем, что у всех питомцев присутствует порода
            assert breeds[i].text != ''
            # Проверяем, что у всех питомцев присутствует возраст
            assert ages[i].text != ''
            # Добавляем имена питомцев в список
            list_names.append(names[i].text)
            # Добавляем имена + породы + возраст каждого питомца в список
            all_pets.append(names[i].text + breeds[i].text + ages[i].text)

        # Проверяем, что количество строк таблицы соответствует количеству питомцев в блоке статистики пользователя
        assert f"Питомцев: {len(names)}" in amount[0].text

        # Проверяем, что у всех питомцев разные имена:
        list_name_my_pets = []
        for i in range(len(names)):
            list_name_my_pets.append(names[i].text)

        set_name_my_pets = set(list_name_my_pets)  # преобразовываем список в множество
        assert len(list_name_my_pets) == len(set_name_my_pets)  # сравниваем длину списка и множества