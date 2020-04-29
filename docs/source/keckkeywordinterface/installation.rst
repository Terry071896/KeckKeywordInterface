Keck Keyword User Interface
---------------------------

Introduction
~~~~~~~~~~~~

This repository runs a web page that provides a user interface for each
of the Keck Instruments. Each page is to communicate the diagnoses of
the health of the instrument.


Repository Structure
~~~~~~~~~~~~~~~~~~~~
> KeckKeywordsInterface

  - app.py (initiates the app)
  - index.py (runs the app)
  - keywords.py (contains Keywords class to read keywords)
  - apps

    - deimos_ui_dark.py (deimos dark theme structure and callback functions)
    - deimos_ui.py (deimos light theme structure and callback functions)
    - esi_ui_dark.py (esi dark theme structure and callback functions)
    - esi_ui.py (esi light theme structure and callback functions)
    - hires_ui_dark.py (hires dark theme structure and callback functions)
    - hires_ui.py (hires light theme structure and callback functions)
    - kcwi_ui_dark.py (kcwi dark theme structure and callback functions)
    - kcwi_ui.py (kcwi light theme structure and callback functions)
    - lris_ui_dark.py (lris dark theme structure and callback functions)
    - lris_ui.py (lris light theme structure and callback functions)
    - main_page.py (MAIN PAGE layout)
    - mosfire_ui_dark.py (mosfire dark theme structure and callback functions)
    - mosfire_ui.py (mosfire light theme structure and callback functions)
    - nirc2_ui_dark.py (nirc2 dark theme structure and callback functions)
    - nirc2_ui.py (nirc2 light theme structure and callback functions)
    - nires_ui_dark.py (nires dark theme structure and callback functions)
    - nires_ui.py (nires light theme structure and callback functions)
    - nirspec_ui_dark.py (nirspec dark theme structure and callback functions)
    - nirspec_ui.py (nirspec light theme structure and callback functions)
    - osiris_ui_dark.py (osiris dark theme structure and callback functions)
    - osiris_ui.py (osiris light theme structure and callback functions)

  - assets

    - deimos.css (deimos pages style and structure settings)
    - esi.css (esi pages style and structure settings)
    - hires.css (hires pages style and structure settings)
    - kcwi.css (kcwi pages style and structure settings)
    - lris.css (lris pages style and structure settings)
    - main-page.css (main page style and structure settings)
    - mosfire.css (mosfire pages style and structure settings)
    - nirc2.css (nirc2 pages style and structure settings)
    - nires.css (nires pages style and structure settings)
    - nirspec.css (nirspec pages style and structure settings)
    - osiris.css (osiris pages style and structure settings)
    - style.css (all pages basic style and structure settings)


Currently, instruments KCWI, NIRSPEC, ESI, and DEIMOS have fully functional pages once up and running.

NIRC2 and OSIRIS have pages up, but the keywords for these instruments are not up on vm-history-1, but once the global server is up then these instruments can be activated (look and read notes in ``apps/main_page.py``).

As for, HIRES, LRIS, MOSFIRE, and NIRES information is needed to build the page (``apps/kcwi_ui.py`` is the best base to work from)

They're limited differences between the 'light' and 'dark' theme script in the ``apps`` folder. In each script, there are these two dictionaries:

::

  theme = {
          'dark': False,
          'detail': '#007439',
          'primary': '#00EA64',
          'secondary': '#6E6E6E'
      } # overall theme of page, either 'dark' = False or 'dark' = True

  class_theme = {'dark' : ''} # the class theme, either '' or '-dark'

Make 'dark' = True in ``theme`` and 'dark' = '-dark' in ``class_theme`` to turn a page to have a dark theme.

From Docker
~~~~~~~~~~~

Runs from docker container

-  Install
-  Run Options
-  Troubleshooting

Install
^^^^^^^

This should import the container

::

   docker pull terry071896/keck_keyword_interface

This is also the command used to install new updates.

Run Options
^^^^^^^^^^^

Option 1- Basic Run:
''''''''''''''''''''

::

   docker run --publish 8050:8050 terry071896/keck_keyword_interface

This should run the container.

You should see (or similar to)

::

    * Serving Flask app "app" (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://0.0.0.1:8050/ (Press CTRL+C to quit)

open a browser and go to the link specified (for me that is
``localhost:8050/``).

Option 2- Start/Stop Run:
'''''''''''''''''''''''''

::

   docker run --publish 8050:8050 --detach terry071896/keck_keyword_interface

This will run the container in the background without any read out.

In order to stop the container from running,

::

   docker stop terry071896/keck_keyword_interface

and to start

::

   docker start terry071896/keck_keyword_interface

If you are starting and stopping the container many times, it could be
ideal to rename the process. (If there are more updates to be installed,
this is not recommended as you will have to remove the name)

::

   docker run --publish 8050:8050 --detach --name keckUI terry071896/keck_keyword_interface

So then you can start stop using that name,

::

   docker start keckUI
   docker stop keckUI

Troubleshooting
^^^^^^^^^^^^^^^

If you are getting the error ``docker: Command not found.``, then go to
the website https://www.docker.com/products/docker-desktop and follow
the instructions to download docker.

If ``docker pull [...]`` or ``docker run [...]`` are not found, check
for spelling errors (it’s there).

If the container appears to be running, but nothing is showing up on the
localhost. Make sure that you are running from port ``8050:8050``.

If the app is not updating properly, then see the GitHub Troubleshooting
section at the bottom of this page.

If you renamed the docker container (such as “keckUI” above) and you are
trying to update, then

::

   docker container rm --force keckUI
   docker run [...]

If none of these are the issue that you are experiencing, then

::

     git clone https://github.com/KeckObservatory/KeckKeywordInterface/
     cd .../KeckKeywordInterface
     docker build -t terry071896/keck_keyword_interface .
     docker run [...]

From GitHub
~~~~~~~~~~~

Runs from python3

-  Install/Run
-  Troubleshooting

Install/Run
^^^^^^^^^^^

::

     git clone https://github.com/KeckObservatory/KeckKeywordInterface/
     cd .../KeckKeywordInterface
     sudo pip install -r requirements.txt

This should import all the code and python packages necessary.

Then, to run the app

::

     python index.py

You should then see

::

    * Serving Flask app "app" (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://0.0.0.1:8050/ (Press CTRL+C to quit)

open a browser and go to the link specified (for me that is
``http://0.0.0.1:8050/``). If there is a problem, then you are running
python2, so ``python3 index.py`` should work.

Troubleshooting
^^^^^^^^^^^^^^^

If the app is not updating or updating properly: - First, give it a few
seconds as the program could be changing modes or reading in a large
amount of data. - Second, either try refreshing the page or kill/rerun
the program.

If you are getting the error

::

   Error in getting data from the server

over and over, then there is a problem with the script
“simple_server.py”, which should be running from “kroot”.

Given that it is not running, then it can be ran from the home directory
“vm-history-1”.

Once logged in, then

::

   cd KeckKeywords/keyword_server/
   kpython3 simple_server.py
