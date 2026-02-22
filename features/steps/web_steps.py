######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
######################################################################

import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions

ID_PREFIX = 'product_'

# --------------------------
# Existing Steps
# --------------------------

@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    assert(message in context.driver.title)

@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert(text_string not in element.text)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element(By.ID, element_id))
    assert(element.first_selected_option.text == text)

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert(element.get_attribute('value') == u'')

# --------------------------
# Copy & Paste Steps
# --------------------------

@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

# --------------------------
# NEW STEPS FOR BUTTON CLICK AND TEXT VERIFICATION
# --------------------------

@when('I click the "{button_text}" button')
def step_impl(context, button_text):
    """ Click a button by its text; button id = lowercase text + '-btn' """
    button_id = button_text.lower().replace(' ', '-') + '-btn'
    button = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.element_to_be_clickable((By.ID, button_id))
    )
    button.click()
    logging.info('Clicked button: %s', button_text)

@then('I should see the text "{text_string}"')
def step_impl(context, text_string):
    """ Verify that a text string is present somewhere on the page """
    body_text = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
    ).text
    assert text_string in body_text, f"Expected text '{text_string}' to be present"
    logging.info('Verified text present: %s', text_string)

@then('I should not see the text "{text_string}"')
def step_impl(context, text_string):
    """ Verify that a text string is NOT present on the page """
    body_text = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
    ).text
    assert text_string not in body_text, f"Expected text '{text_string}' to NOT be present"
    logging.info('Verified text not present: %s', text_string)

@then('I should see the message "{message}"')
def step_impl(context, message):
    """ Verify that a message/alert is present """
    message_element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, 'alert'))
    )
    assert message in message_element.text, f"Expected message '{message}' to be displayed"
    logging.info('Verified message displayed: %s', message)

# --------------------------
# Field Verification Steps
# --------------------------

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    assert(found)
    logging.info('Verified field %s contains text: %s', element_name, text_string)

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)
    logging.info('Changed field %s to: %s', element_name, text_string)