build:
	docker compose up --build --remove-orphans

up:
	docker compose up

down:
	docker compose down

down-v:
		docker compose down -v

logs:
	docker compose logs

%:
	@:

# $(MAKECMDGOALS) is the list of "targets" i.e. broker
# filter-out is a function that removes some elements from a list
#$(filter-out $@,$(MAKECMDGOALS)) returns the list of targets specified on the command line other than "restore", which in this case is the name of the postgres backup file
args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

restart:
	docker compose restart $(call args,defaultstring)


restart-all:
	docker compose restart


config:
	docker compose config
