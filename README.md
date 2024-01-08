### How to run API-service

1. Using your preferred package management tool, create a new virtual env. For example, using `conda`:

    ```bash
    conda create -n <env_name> python=3.11
    ``` 
   
2. Clone repository and install dependencies:

    ```bash
    git clone https://github.com/andriibudzan/ajax-tt.git && cd ajax-tt
    pip install -r requirements.txt
   ```
   
3. Set environment variables for access to databases. Do it manually or add proper values to template `set_vars.sh` 
   and run `source ./set_vars.sh`. Required variables are:

   - `DBL_URL, DBL_USERNAME, DBL_PASSWORD` for legacy service.
   - `DBE_DATABASE, DBE_USER, DBE_PASSWORD, DBE_HOST` for employees database.

4. Run the application using bash script:

    ```bash
    ./run_api_service.sh
    ```
   
5. After service start, open additional terminal tab an use ```curl``` to test the service.
   Service uses Basic Authentication. Please, use listed credentials for testing:
    - login: `user1`, password: `Password1`
    - login: `user2`, password: `password2`

    ```bash
   # will return all list of all employees with all details included.
    curl -X 'GET' 'http://127.0.0.1:5000/users' -H 'accept: application/json' -u login:password
      
   # will return data for user with id=1000 (CEO, in this case) and all details about this employee
    curl -X 'GET' 'http://127.0.0.1:5000/users/1000' -H 'accept: application/json' -u login:password
    ```

6. To stop service press `Ctrl+C` in terminal where service is running.
