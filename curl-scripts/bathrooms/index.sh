#!/bin/bash

curl "http://localhost:8000/bathrooms/" \
  --include \
  --request GET \
  --header "Authorization: Token ${TOKEN}"

echo
