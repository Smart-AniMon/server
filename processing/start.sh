docker run --rm --name animon_processing \
--env-file $PWD/.env \
--volume $PWD/resources:/animon/processing/resources \
--volume $PWD/../../smart-animon-vision-key.json:/animon/processing/credentials/vision-key.json \
-i -t animon/processing:1.0.1
