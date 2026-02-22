Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hat" in the "Name" field
    And I should see "A red fedora" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "CLOTH" in the "Category" dropdown
    And I should see "59.95" in the "Price" field

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I set the "Price" to "49.95"
    And I press the "Update" button
    Then I should see the message "Success"
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "49.95" in the "Price" field

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Delete" button
    Then I should see the message "Success"
    And I press the "Search" button
    Then I should see "No products found"

Scenario: List all Products
    When I visit the "Home Page"
    And I press the "List All" button
    Then I should see "Hat" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results

Scenario: Search Products by Category
    When I visit the "Home Page"
    And I select "FOOD" in the "Category" dropdown
    And I press the "Search" button
    Then I should see "Big Mac" in the results

Scenario: Search Products by Availability
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see "Hat" in the results
    And I should see "Big Mac" in the results

Scenario: Search Products by Name
    When I visit the "Home Page"
    And I set the "Name" to "Sheets"
    And I press the "Search" button
    Then I should see "Sheets" in the results