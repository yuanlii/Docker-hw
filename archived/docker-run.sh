# docker run -t --rm --name custom_psql_running -p 5432:5432 yuanlii/custom_psql

# we created a network first: `docker network create -d bridge my-bridge-network`
docker run -t --rm -d -p 5432:5432 --network my-bridge-network --name custom_psql_running yuanlii/custom_psql
