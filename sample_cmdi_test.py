import asyncio
import requests

WHOAMI_ORACLE = "giacomo"
FILE_EXISTS_ORACLE = "ping.php"
SERVER_URL = "http://localhost:9000"

# define test for page containing echo command
test_values_echo = {
    'semicolon': ';whoami',
    'ampersand': '&whoami',
    'logical AND': '&&whoami',
    'pipe': '|whoami',
    'subshell': '$(whoami)',
    'backticks': '`whoami`',
    'blind injection redirection': '; whoami > whoami_echo.txt',
}

# define test for page containing ping command
test_values_ping = {
    'semicolon': 'localhost; whoami',
    'ampersand': 'localhost &whoami',
    'logical AND': 'localhost &&whoami',
    'pipe': 'localhost |whoami',
    'boolean-based': 'localhost; if [ -f ping.php ]; then whoami; fi',
    'boolean-based blind': 'localhost; if [ -f ping.php ]; then whoami > whoami_ping.txt; cat whoami_ping.txt; fi', 
    'boolean-based blind 2': 'localhost; if [ -f {} ]; then whoami < whoami_ping.txt; cat whoami_ping.txt; fi'.format(FILE_EXISTS_ORACLE),
    'blind injection redirection': 'localhost; whoami > whoami_ping.txt; cat whoami_ping.txt',
}

# define test for page containing find command
test_values_find = {
    'semicolon': 'ping.php ; whoami',
    'ampersand': 'ping.php & whoami',
    'logical AND': 'ping.php &&whoami',
    'pipe': 'ping.php |whoami',
    'argument': 'ping.php -exec whoami ;',
    'boolean-based': 'ping.php; if [ -f ping.php ]; then whoami; fi',
    'boolean-based blind': 'ping.php; if [ -f ping.php ]; then whoami > whoami_find.txt; fi', 
    'boolean-based blind 2': 'ping.php; if [ -f {} ]; then whoami; fi'.format(FILE_EXISTS_ORACLE),
    'blind injection redirection': 'ping.php; whoami > whoami_find.txt; cat whoami_find.txt',
}

#assign the tests to the correct pages
test_pages = {
    'echo-name.php': test_values_echo,
    'echo.php': test_values_echo,
    'find-escapeshellcmd.php': test_values_find,
    'ping-escapeshellcmd.php': test_values_ping,
    'ping-no-amp.php': test_values_ping,
    'ping-no-output.php': test_values_ping,
    'ping-no-pipe.php': test_values_ping,
    'ping-no-semicol.php': test_values_ping,
    'ping-no-space.php': test_values_ping,
    'ping.php': test_values_ping,
}

@asyncio.coroutine
def test_step(test_name, test_value, url):
    cookies = {'a': '1'}
    headers = {}
    params = {
        'host': test_value,
        'name': test_value,
        'input': test_value,
    }

    #print(f"\nTest performed on {url}")
    future = loop.run_in_executor(None, requests.get(url, params, cookies, headers))
    response = yield from future1
    
    test_result = WHOAMI_ORACLE not in response.text

    print("{} {}".format("\u2705" if test_result else "\u274c", test_name))

# this for sequential running
#for page, test_values in test_pages.items():
#    url = SERVER_URL + '/' + page
#    print(f"\nTest performed on {url}")
#    for test_name, test_value in test_values.items():
#        test_step(test_name, test_value, url)

async def main():
    tasks = []
    loop = asyncio.get_event_loop()
    for page, test_values in test_pages.items():
        print(f"\nRunning tests for {page}\n")
        url = SERVER_URL + '/' + page
        for test_name, test_value in test_values.items():
            task = asyncio.create_task(test_step(test_name, test_value, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
    
#async def main():
#    async with asyncio.get_event_loop() as loop:
#        tasks = []
#        for page, test_values in test_pages.items():
#            url = SERVER_URL + '/' + page
#            print(f"\nTest performed on {url}")
#            for test_name, test_value in test_values.items():
#                task = asyncio.create_task(test_step(test_name, test_value, url))
#                tasks.append(task)
#            await asyncio.gather(*tasks)
#