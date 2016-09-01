# This script will start both elasticsearch and the eval API

echo "Building evaluation API"
./gradlew clean build installApp --daemon

echo "Starting elasticsearch"
elasticsearch & ES_PID=$!

echo "Starting evaluation API"
./build/install/lifelog-eval/bin/lifelog-eval server configuration.yml & EVAL_PID=$!

## call the "handle_kill" function when signals are received.
trap handle_kill SIGINT SIGTERM SIGKILL

function handle_kill() {
    echo ""
    echo "Stopping elasticsearch"
    kill -9 $ES_PID
    echo "Stopping evaluation API"
    kill -9 $EVAL_PID
    exit
}

while :
do
    sleep 5
done