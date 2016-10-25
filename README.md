# bi-automation

This is a very simple installable project to simplify deployment automation. 
Private projects on Github can be accessed with ssh keys or a Github token. 

This repo provides a function that resolves github URLs, depending on whether there is a github token defined in an 
environment variable (HELLOFRESH_TOKEN), or not. This avoids the need to place ssh keys on servers where we wish to deploy projects.
