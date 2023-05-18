# CLIENT-SIDE SECURITY TESTING

## Messaging System

Javascript injections scripts in the messages.

Performing actions? Critical Operations should not be confortable to make automatically.

Don't make to use that scripts automatically, put the user inside the event loop.

    http://localhost:4000/send_message.php

    msg = Hey+there!&to=ford
    
    INSERT INTO messages VALUES ($_SESSION['username'], $to, $msg)
    
    SELECT * FROM messages WHERE reciever=$_SESSION[‘username’]
    
    Hey+there!

### Stored Cross-Site Scripting

Because the code is stored by the application
- put a script inside the messages and store it
- show the content to arbitrary users

This is another kind of script attack:

    http://localhost:4000/send_message.php
    
    msg=<script>alert(1)</script>&to=ford
    
    INSERT INTO messages VALUES ($_SESSION[‘username’], $to, $msg)
    
    SELECT * FROM messages WHERE receiver=$_SESSION[‘username’]

    <script>alert(1)</script>

To try this use two browser to enter with two different users and send messages throught them