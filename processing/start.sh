docker run --rm --name animon_processing \
--env-file $PWD/env_vars \
--volume $PWD/resources:/animon/resources \
--volume $PWD/../../smart-animon-vision-key.json:/animon/credentials/vision-key.json \
-i -t animon/processing:1.0.0
