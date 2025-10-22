pgdcn=`docker ps -q --filter "ancestor=postgres:17"`
docker exec -it  $pgdcn  psql -U sai_dev -d sha
