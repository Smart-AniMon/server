docker run -p 5000:5000 --rm --name animon_application \
--env-file $PWD/env_vars \
-i -t animon/application:1.0.0
