# SWAPI EXPLORER

### Architecture overview
Application has been designed to be open to add a new API's to handle. Each external API is called `integration`.
The main application `datasets` which is responsible for saving/displaying collections knows nothing about connecting 
and interacting the external API and also transforming the data. The whole logic shares the same interface which is 
declared in `core` module. If we want to handle another API we have to create another module, implement the interface
and register that module in the `settings` without touching the `datasets` app. This will work in opposite way: if we
decide to stop to maintain an api anymore, we can just remove whole package.

* added 16.11.2021 (after solution sent):

    a) Current implementation does not require any background tasks etc. but in real life I will suggest to use for example celery workers
    for fetching data. I think that some data which does not change very often should be store in database and reuse. It will save heavy http     requests. Redis should work here as well for caching some 

    b) SWAPI does not require any access keys so I didn't create any auth logic but If some kind of API will require then application
        should has an auth app with permissions and api tokens.
        
    c) I realized that naming convention in some places are really bad. Eg `Dataset.name` should be `Dataset.integration_name` actually.
       I don't want to change anything because you are during review.
 
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
The entry endpoint `https://swapi.co/api/people/` is not working but I figured out that `https://swapi.dev/` is working like
a charm and this endpoint is used by default. If any cases when this service won't be available I prepared forked version
to run locally: `https://github.com/L3str4nge/swapi`.

1. Docker
    ```
    git clone https://github.com/L3str4nge/adv
    cd adv

    # If yo u want to run db+application (not recommended because app can be up before db at the first time)
    make run_all 

    # If you want to run db only
    make run_db
    
    #If you want to run application only
    make run_backend
    ```

2. Without Docker

    ```
    python -m venv adv_venv
    source adv_venv/bin/activate
    git clone https://github.com/L3str4nge/adv
    cd adv
    pip install -r requirements.txt
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

    `make test` This will run pytest in docker container.
    
    Run `pytest` in root directory to run tests locally.
