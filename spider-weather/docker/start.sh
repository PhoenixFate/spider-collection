rm -rf ./code
mkdir -p ./code
\cp  -rf ../code/* ./code
sh ./clear-spider-weather.sh
sh ./build-spider-weather-image.sh
sh ./run-spider-weather-docker.sh
