In the project directory, you can run:

1. To start the frontend server:

### `cd frontend`

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

2. To start backend server:

### `cd backend`

### `uvicorn fetch_prices:app --reload`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

3. Database Requirements:

The database server running on GCP does not require any authentication, but to run the backend application, your IP Address must be whitelisted on GCP Firewall Rules. You can reach out to Lohith or Toshi to have your IP Address whitelisted.

# CONTRIBUTIONS

## Lohith Nagaraja

1. Database design and implementation on GCP.
2. Scraping GPU data from benchmark site.
3. Debugging Authentication issues.
4. Backend implementation using FastAPI.

## Toshi Bhat

1. Database design.
2. Scraping price data from online shopping portals.
3. Backend implementation using FastAPI.
4. Frontend using ReactJS.

