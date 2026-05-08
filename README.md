
# Fuel Route Optimization API

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoint

POST `/api/optimize-route/`

### Example Request

```json
{
  "start": "Dallas, TX",
  "finish": "Phoenix, AZ"
}
```

## Free Routing API

Use OpenRouteService:
https://openrouteservice.org/

Replace:
`YOUR_OPENROUTESERVICE_API_KEY`

inside:
`routes/services.py`
