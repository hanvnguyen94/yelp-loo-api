#!/bin/bash

curl "http://localhost:8000/bathrooms/${ID}/" \
  --include \
  --request DELETE \
  --header "Authorization: Token ${TOKEN}"

echo
