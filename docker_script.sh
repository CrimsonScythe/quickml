docker image build --no-cache -t quickml_api .
docker run -p 5000:5000 -d quickml_api

ssh into docker container
docker exec -it nostalgic_goldstine bash