# Description

On this kind of messaging systems, if the page are not done accurately the kind of attacks could be so useful and so powerful.

Starting from the man in the middle attack going through Cross Site Scripting:

## Stored Based Cross-Site Scripting

If we have a messaging system and we obtain a message containing a script we will se directly when the message is stored to the server and the reciever gets attacked.

## Reflected Cross-Site Scripting

echo-name.php?name=anything

Server recieves a GET request /echo-name.php?name=anything

In this case we might try to insert some html:
echo-name.php?name=<h1>headerText</h1>

And also we can pass script to make no more functional the application to the user of just "disturb" him

How can we attack using this? If this works for me, I can send that link to someone else (storing the payload in the url) and make him visit that link that will reflect the payload to them.

## DOM-based XSS

Server side application is not involved but we use the client side application to do directly in browser and inserting other types of scripts.

## Mitigating XSS

In this case we can avoid this checking if the string contains lt or gt (< o >) we can use:

    htmlspecialchars($_GET[payload])

This makes all the tags html attributes converted in string so doesn't works attacking the scripts to the payload

## Mitigating XSS - Bypass

If we are serching and removing the scripts tags but we organize the payload like the following: `<scri<script>pt>` we can see that we bypass the check because this will remove the internal script and make us use the external corrected script.

