# Domer-Rover-2024-25-Auton-Code

DOWNLOAD PACKAGE:

To download the current version of the Autonomous Code package onto your local machine, please make sure you have Docker installed and set up on your machine as well as VS Code with the Docker extension downloaded.

1. On Github, navigate to Settings->Developer Settings->Personal Access Tokens->Tokens (classic) and click "Generate new token (classic)"
2. In the note section, type in "Domer Rover 2024-25". Set the expiration date to "No expiration" and select the checkbox next to "write:packages".
3. Generate the token and copy the token given (can save if you wish)
4. Open up a terminal in VS Code/your local machine and navigate to the folder where you want to download the package
5. Login to the Docker Registry through the command: docker login
6. Type in your Github username for the username and paste in the token for your password, this will allow you to login to the online Docker Registry
7. [OPTIONAL] Go back to the repo and clone the most recent package into your local folder, you will need to have the Dockerfile uploaded to your local
8. Type docker pull ghcr.io/user_who_made_recent_change/my_bot:latest to get the new image
9. Type docker run -it user_who_made_recent_change/image_name:latest /bin/bash to create a container for that image
10. On the left of VS Code, Navigate to the Docker extension and look for the container you just made. Right click on it and run a new instance of it in a different VS Code window. You should be able to make changes to the package new!

To save changes:

1. Save all your work and exit/turn off the container
2. Type docker commit <container_id> ghcr.io/username/image:latest. This will create a new image with your changes
3. Login to the Docker Registry through the same methodology above
4. Type docker commit <name>
5. Type docker tag <name>  ghcr.io/username/image:latest 
6. Type docker push ghcr.io/username/image:latest
7. [Optional] Make a commit with the changes to the Dockerfile and push the Dockerfile to the repo using Git
