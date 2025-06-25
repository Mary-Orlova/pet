from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging_config import setup_custom_logger

logger = setup_custom_logger(__name__)

def test_fias_autocomplete_and_search(address: str) -> str:
    """
    Тест на получение FIASid
    :return: FIAS id
    """

    #Проверка, что переданный адрес не пустой, иначе завершение программы с ошибкой
    if address == "":
        logger.error("Отсутствует адрес")
        raise ValueError("Отсутствует адрес")

    driver = webdriver.Chrome()
    driver.maximize_window()


    try:
        driver.get("https://fias.nalog.ru/Search/")
        wait = WebDriverWait(driver, 25)

        # Ввод тестового адреса
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.full-text-search"))
        )
        search_input.clear()
        search_input.send_keys(address)

        # Ожидание появления выпадающего списка и кликаем по первому элементу
        first_option = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "div.k-animation-container div.k-popup div.k-list div.k-list-content ul.k-list-ul li.k-list-item")
            )
        )
        first_option.click()

        # Ожиданием, нажатие кнопки "Найти"
        find_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Найти"]'))
        )
        find_button.click()

        # Ожидание появления поля с id="FiasId", проверка его значение
        fias_id = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ObjInfoPlaceholder dd#FiasId"))
        )
        fias_id_value = fias_id.text.strip()
        assert fias_id_value != "", "FiasId отсутствует!"

        logger.info(f"FIAS найден: {fias_id_value}")

    except ValueError as error:
        logger.error("Возникло исключение, FiasId отсутствует!", error)

    finally:
        driver.quit()

if __name__ == "__main__":
    address=""
    test_fias_autocomplete_and_search(address)
