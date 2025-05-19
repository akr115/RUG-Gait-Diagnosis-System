#!/bin/sh

# Load environment variables from .env file
if [ -f /.env ]; then
  . /.env
fi

cat <<EOF > /usr/share/nginx/html/runtime-config.js
window.env = {
  BACKEND_URL: "$BACKEND_URL",
};
EOF

exec "$@"
