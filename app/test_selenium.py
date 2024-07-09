# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        driver.find_element_by_link_text(u"Вопрос из раздела Математика").click()
        driver.find_element_by_id("InputName").click()
        driver.find_element_by_id("InputName").clear()
        driver.find_element_by_id("InputName").send_keys("8")
        driver.find_element_by_id("markQ").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Enter your answer'])[1]/following::button[1]").click()
        driver.find_element_by_link_text("Brainteasers!").click()
        driver.find_element_by_link_text("Find extra word").click()
        driver.find_element_by_link_text(u"Вопрос из раздела Найди лишнее слово").click()
        driver.find_element_by_id("InputName").click()
        driver.find_element_by_id("InputName").clear()
        driver.find_element_by_id("InputName").send_keys(u"пицца")
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Enter your answer'])[1]/following::button[1]").click()
        driver.find_element_by_link_text("Maths").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='(20 - 4) / 2 = ?'])[1]/following::a[1]").click()
        driver.find_element_by_id("InputName").click()
        driver.find_element_by_id("InputName").clear()
        driver.find_element_by_id("InputName").send_keys("12")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Enter your answer'])[1]/following::button[1]").click()
        driver.find_element_by_link_text("Maths").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='Вопрос из раздела Математика'])[2]/following::a[1]").click()
        driver.find_element_by_id("InputName").click()
        driver.find_element_by_id("InputName").clear()
        driver.find_element_by_id("InputName").send_keys("0")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Enter your answer'])[1]/following::button[1]").click()
        driver.find_element_by_link_text("Find extra word").click()
        driver.find_element_by_link_text("Brainteasers!").click()
        driver.find_element_by_link_text("Popular brainteasers").click()
        driver.find_element_by_link_text(u"Вопрос из раздела Переведи!").click()
        driver.find_element_by_id("InputName").click()
        driver.find_element_by_id("InputName").clear()
        driver.find_element_by_id("InputName").send_keys(u"шоолдлд")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Languid'])[1]/following::span[1]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Like!'])[1]/following::div[1]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Enter your answer'])[1]/following::button[1]").click()
        driver.find_element_by_link_text("Brainteasers!").click()
        driver.find_element_by_id("userDropdown").click()
        driver.find_element_by_link_text("Exit").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("yulya")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("yulya12345")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Authorization'])[1]/following::div[2]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Authorization'])[1]/following::div[2]").click()
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Authorization'])[1]/following::div[2]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::div[2]").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()