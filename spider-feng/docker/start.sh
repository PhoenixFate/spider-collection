rm -rf ./code
mkdir -p ./code
\cp  -rf ../code/* ./code
sh ./clear-spider-feng.sh
sh ./build-spider-feng-image.sh
sh ./run-spider-feng-docker.sh
