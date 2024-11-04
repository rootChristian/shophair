# SHOP HAIR PROJET: Website for hair sales.

## `BACKEND`
### In the project directory, run this command to initialize the project and install dependencies:
- `python3 -m venv venv`
- `source venv/bin/activate`
- `python3 -m pip install --upgrade pip`
- `pip install -r requirements.txt`  (If the file requirement exists)
- `pip install djangorestframework djangorestframework-simplejwt django-cors-headers python-dotenv django psycopg2 pyotp google-api-python-client`
- `pip freeze > requirements.txt` 
- `rasa init`

### Environment DB PostgreSQL:
- `brew update`
- `brew install postgresql`
- `psql --version`
- `psql postgres`
- `brew services list`
- `brew services start postgresql`
- `psql -U user_admin -d shophair_db_test`

### Environment to get the default domain to expose the application online for a test:
- `brew install ngrok/ngrok/ngrok`
- `ngrok config add-authtoken YOUR_AUTH_TOKEN`
- `ngrok http http://localhost:8080`

### Command to run the project:
- Rasa chatbot  `rasa run`  `rasa run actions`  `rasa run --enable-api`
- MongoDB:  `python manage.py makemigrations`  `python manage.py migrate`
- Backend:  `python manage.py runserver`

### Environment variables:
- Default port server: `(PORT = "XXXX")`
- Default url api: `(API_URL = "XXXX")`
- MongoDB: `(MONGO_IP = "XXXX"; MONGO_PORT = "XXXX"; MONGO_DATABASE = "XXXX")`
- Url RASA Chatbot: `(RASA_URL = "XXXX")`


## `FRONTEND`
### In the project directory, run this command to initialize the project and install dependencies:
- `npx create-react-app .`
- `npm redux react-redux redux-thunk bootstrap axios`

### Command to run the project:
- Frontend:  `npm start`
