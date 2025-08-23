#!/bin/sh

set -e

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py seed
python manage.py collectstatic --noinput

# SOCKET_DIR="/data/tmp"
# SOCKET_PATH="$SOCKET_DIR/daphne.sock"
# SOCKET_PATH_LOCK="$SOCKET_DIR/daphne.sock.lock"

# echo "🔹 Garantindo que o diretório $SOCKET_DIR existe..."
# mkdir -p "$SOCKET_DIR"
# chmod 777 "$SOCKET_DIR"

# echo "🔹 Limpando socket antigo, se existir..."
# rm -f "$SOCKET_PATH"
# rm -f "$SOCKET_PATH_LOCK"

# echo "🔹 Verificando se Daphne está rodando..."
# if pgrep daphne; then
#   echo "🔸 Daphne já está rodando! Matando..."
#   pkill -9 daphne
# fi

# echo "🔹 Checando se o socket $SOCKET_PATH ainda existe após o kill..."
# if [ -e "$SOCKET_PATH" ]; then
#   echo "🧹 Removendo novamente: $SOCKET_PATH"
#   rm -f "$SOCKET_PATH"
#   rm -f "$SOCKET_PATH_LOCK"
# fi

# echo "🚀 Iniciando Daphne no socket $SOCKET_PATH"
# exec daphne -v 2 -u "$SOCKET_PATH" core.asgi:application
daphne -b 0.0.0.0 -p ${API_PORT:-8000} core.asgi:application