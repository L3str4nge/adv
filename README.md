# SWAPI EXPLORER

### Architecture overview
Application has been designed to be open to add a new API to handle. Each external API is called `integration`.
The main application `datasets` responsible for saving/displaying collections knows nothing about connecting 
and interacting the external API and also transforming the data. The whole logic shares the same interface which is 
declared in `core` module. If we want to handle another API we have to create another module, implement the interface
and register that module in the `settings` without touching the `datasets` app. This will work in opposite way: if we
decide to stop to maintain an api anymore, we can just remove whole package.

Please don't judge me for HTML and JavaScript... my eyes are still bleeding after creating DOM's dynamically :D But yeah
there is `axios` so it's fancy isn't it?


### Collecting and transforming
Collecting and transforming data is done by streams So basically the data flow is:
1. Get data from an endpoint for page = 1.
2. Transform data.
3. Append to the given storage.
4. Go to 1 with next page else go to 5.
5. Save given storage and object to the database.

`Storage` is also flexible. For now only `csv` is supported but if another one is needed then you have to create 
a new class which implements `Storage` interface.

I wonder if transforming data based on `dict` is good approach (I suppose `petl` has better performance for large amount
of data), but for now I only use `petl` for getting data from the file and make counting for the `Value count` functionality.

### Installation and runnnig
The entry endpoint `https://swapi.co/api/people/` is not working but I figured out that `https://swapi.dev/` working like
a charm and this endpoint is used by default. If any cases when this service won't be available I prepared forked version
to run locally: `https://github.com/L3str4nge/swapi`.

1. Docker
```
git clone https://github.com/L3str4nge/adv
cd adv

# If you want to run db+application
make run_all

# If you want to run db only
make run_db

#If you want to run application only
make run_backend
```

2. Without Docker

```
git clone https://github.com/L3str4nge/adv
cd adv
```

Then you have to set up env variables which are defined in `.env.template`. Do not set db env variables if you want to
set up `sqlite` database.

Run following script:
`scripts/run.sh`

3. Run with Docker and SWAPI locally

If you don't want to use `https://swapi.dev/` or it is not working you can set up project locally:
```
git clone https://github.com/L3str4nge/adv
cd adv

# Create network for separate containers
make network

# Install SWAPI (it will be installed in your /tmp directory)
make swapi

# Make .env.template like this:
#SWAPI_URL="https://swapi.dev/api"
SWAPI_URL="http://swapi:8002/api"

# Run
make run_all
```

4. Run tests

`make test` This will run pytest.