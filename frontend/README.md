# Medicare chatbot Frontend

**A react frontend for Medicare chatbot.**

## Folder Structure

- `components` folder will contain page specific, layout and re-usable components.
- `configs` folder will contain configuration settings.
- `api` folder will contain API/database calls.
- `ui` folder will contain theme configuration and material ui style extensions.
- `utils` folder will contain helper functions.
- `views` folder will contain module wise page components.

<br />

## Setup the codebase

**Install all the packages and dependencies:**

`npm install`

Then copy the .env-sample and save it with .env file, and fill in the configuration settings.

<br />

## Run the application

**Run the frontend app: at /frontend**
`npm start`

**Run the backend app: at /backend**

`export FLASK_APP=main.py`
<br />
`flask run --port=PORT_NUMBER`