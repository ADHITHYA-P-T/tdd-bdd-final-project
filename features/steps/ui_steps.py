from behave import when, then
from selenium.webdriver.common.by import By

@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

@when('I set the "{field}" to "{value}"')
def step_impl(context, field, value):
    input_field = context.driver.find_element(By.ID, field.lower())
    input_field.clear()
    input_field.send_keys(value)

@when('I press the "{button}" button')
def step_impl(context, button):
    context.driver.find_element(By.ID, button.lower()).click()

@then('I should see "{text}" in the results')
def step_impl(context, text):
    assert text in context.driver.page_source



    