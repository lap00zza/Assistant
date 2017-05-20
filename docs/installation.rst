.. FIXME: for the without docker section, the permalinks are not working as
   expected. Find a way to fix it.
   
Installation
============

It is recommended to run Assistant using docker. It saves you the hassle of 
manually installing dependencies.

------
Docker
------

#. Install `docker <https://www.docker.com/community-edition#/download>`_
#. Install `git <https://git-scm.com/downloads>`_
#. Clone the Assistant github repository:

	.. code-block:: shell

		git clone https://github.com/lap00zza/Assistant.git
		cd Assistant

#. Create an environment variable named ``DOCKER_TOKEN`` and set it to you own 
   token. To find your token, open discord and press ``ctrl+shift+i``. Then go 
   to the **Applications** tab and find the **Key** named ``token``. This is 
   your token.
#. Now build the image and run.

	.. code-block:: shell

		docker-compose build
		docker-compose up

------
Normal
------

#. Install `git <https://git-scm.com/downloads>`_
#. Install `Python 3.6+ <https://www.python.org/downloads/>`_
#. Install `NodeJs 6.7.0+ <https://nodejs.org/en/download/>`_ (*for evaljs*)
#. Clone the Assistant github repository:

	.. code-block:: shell

		git clone https://github.com/lap00zza/Assistant.git
		cd Assistant/bot

#. Install the dependencies
	
	.. code-block:: shell
		
		pip install -r requirements.txt

#. Create an environment variable named ``DOCKER_TOKEN`` and set it to you own 
   token. To find your token, open discord and press ``ctrl+shift+i``. Then go 
   to the **Applications** tab and find the **Key** named ``token``. This is 
   your token.

#. Now run.

	.. code-block:: shell

		py run.py
