# DESCRIPTION

In this assignment, you will build a new test suite that tests the target application for Union-based SQL Injections, similar to the one you built in Assignment 1.

While in Assignment 1 you could use plain Python for your test suite, for this assignment you will use pytest to organize and run your test steps.

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

if the page is working correctly (e.g., for login pages, that the login is working correctly)
if the page is vulnerable to SQL injection.
In particular, you should test the page for Union-based and Error-based SQL Injections (but you can also have additional steps if you want).

Tests should take into account all possible variants of syntax and insufficient sanitization that could be applied to the page.


Confirmation step
One easy way to confirm that the attack was successful is to retrieve the MySQL version via the VERSION() SQL function, or the user for the current connection, which can be retrieved via the USER() function. Of course, you can use any other value you prefer to confirm the exploit.