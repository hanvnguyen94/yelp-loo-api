#!/bin/bash

curl "http://localhost:8000/bathrooms/${ID}/" \
  --include \
  --request PATCH \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "bathroom": {
      "name": "'"${NAME}"'",
      "location": "'"${LOCATION}"'",
      "description": "'"${DESC}"'",
      "photoUrl": "'"${URL}"'"
    }
  }'

echo