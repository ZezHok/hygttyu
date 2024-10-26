import time
import pytest
from home_page import HomePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Сообщения для отправки
text = "Alpine skiing is gorgeous"
text_mention = "I`m fed up with @BEE-diploma#7805"
text_mention_non_existed_user = "@TylerDurden, what`s the first rule?"
text_empty_message = " "



     # ПОЗИТИВНЫЕ ТЕСТЫ
@pytest.mark.usefixtures("init_driver", "base_url")
class TestMessage:

    # Отправка текстового сообщения
    def test_send_message(self, base_url):
        # Инициализация страницы
        home_page = HomePage(self.driver)

        # Отправка сообщения
        home_page.send_message_in_channel(text)

        # Проверка отправки сообщения
        message_send = home_page.is_message_send()
        assert message_send.count(text) == 1, "Сообщение не отправлено"


    # Редактирование текстового сообщения
    def test_edit_message(self,base_url):
        # Инициализация страницы
        home_page = HomePage(self.driver)

        # Редактирование ранее отправленного сообщения
        home_page.edit_message()
        time.sleep(15)

        # Проверка редактирования сообщения  (появилась отметка "изменено")
        new_message = home_page.is_message_send()
        assert new_message.count('изменено') == 1


    # Добавление реакции на сообщение
    def test_add_reaction(self, base_url):
        # Инициализация страницы
        home_page = HomePage(self.driver)

        # Добавление реакции
        home_page.send_reaction()
        time.sleep(10)
        # Проверка наличия реакции под сообщением
        assert home_page.is_reaction_displayed().is_displayed() == True, "Реакция на сообщение отсутствует"


    # Удаление реакции на сообщение
    def test_delete_reaction(self, base_url):
        # Инициализация страницы
        home_page = HomePage(self.driver)

        # Удаление реакции
        home_page.delete_reaction()

        # Проверка удаления реакции
        assert WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(home_page.reaction_locator()))


    # Удаление сообщения
    def test_delete_message(self, base_url):
        # Инициализация страницы
        home_page = HomePage(self.driver)

        # Удаление сообщения
        home_page.delete_message()

        # Проверка удаления сообщения
        assert WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(home_page.form_message_locator()))


    # Проверка, что упомянутый в сообщении пользователь существует
    def test_send_message_with_mention(self, base_url):
        # Инициализация страницы
        home_page = HomePage(self.driver)

        # Отправка сообщения
        home_page.send_message_in_channel(text_mention)
        time.sleep(15)

        # Проверка, что упомянутый пользователь существует
        role = home_page.is_mentioned_user_exists()
        assert role == "button"

        # Удаление сообщения
        home_page.delete_message()
        time.sleep(15)


   # НЕГАТИВНЫЕ ТЕСТЫ
@pytest.mark.usefixtures("init_driver", "base_url")
class TestNegative:

    # Проверка, что упомянутый в сообщении пользователь НЕ существует
    def test_send_message_to_non_exist_user(self, base_url):
        # Инициализация страницы
        home_page = HomePage(self.driver)

        # Отправка сообщения
        home_page.send_message_in_channel(text_mention_non_existed_user)

        # Проверка, что упомянутый пользователь НЕ существует
        assert home_page.is_mentioned_user_non_exists() == None

        # Удаление сообщения
        home_page.delete_message()
        time.sleep(15)

    #  Отправка "пустого сообщения"
    def test_send_empty_message(self, base_url):
        # Инициализация страницы
        home_page = HomePage(self.driver)

        # Отправка сообщения
        home_page.send_message_in_channel(text_empty_message)

        # Проверка НЕ-отправки сообщения
        assert WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(home_page.form_message_locator()))
