# ITLAB: COVID-19 Visualisation Dashboard-v3

## Setup

To start working on this project you will need a clean environment to add and delete your own libraries. The files has a <i>requirements.txt</i> file which will contain all the up-to-date libraries being used. make sure you have python install on your machine before proceeding. <b>This setup procedure should only be used if changes are being made on the a machine outside of any of the ITLab servers.</b> 

1. ### Install virtualenv
    1. pip install virtualenv
    2. virtualenv myenv <i>(myenv is the name I chose, any name can be given for the environment)</i>. myenv must be installed in the root directory of this project.
2. ### Activating virtual environment
    <b>If on a MAC/Linux:</b>

    source myenv/bin/activate 

    <b>If using Windows:</b>

    \myenv\Scripts\activate.bat

    <b>Note:</b> these paths will only work if you and the myenv directory are currently in the root directory. 

3. ### Installing libraries

    pip install -r requirements.txt

Once you complete these steps your environment will be ready to run the most recent updates made to the dashboard by the ITLab visualization team.

## Running Flask 

1. To start the flask environment, execute the command <i>"flask run [port]"</i>. The port section can be empty and will default to port 5000. Run the url "https://localhost:[port]" and the main page of the dashboard will open up.

2. Execute command <i>"export FLASK_ENV=development"</i>
3. Execute command <i>"export FLASK_APP=v3"</i>

## Errors

If there are any additional errors after this setup, there will be basic solutions on stack-overflow or any other similar website.