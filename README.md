### Intallation

1. Using your preferred package management tool, create a new virtual env. For example, using `conda`:

    ```bash
    conda create -n <env_name> python=3.11
    ``` 
   
2. Clone repository and install dependencies:

    ```bash
    git clone https://github.com/andriibudzan/ajax-tt.git && cd ajax-tt
   ```

3. Run the application using bash script:

    ```bash
    ./run_api_service.sh
    ```
   
4. After service start, open additional terminal tab an use ```curl``` to test the service.
   Service uses Bearer token authentication. Currently, token is hardcoded, so use `mytoken1` as a token in your 
   requests. For example:

    ```bash
   # will return all list of all employees with all details included.
    curl -X 'GET' 'http://127.0.0.1:5000/users' -H 'accept: application/json' -H 'Authorization: Bearer mytoken1'
      
   # will return data for user with id=1000 (CEO, in this case) and all details about this employee
    curl -X 'GET' 'http://127.0.0.1:5000/users/1000' -H 'accept: application/json' -H 'Authorization: Bearer mytoken1'
    ```

5. To stop service press `Ctrl+C` in terminal where service is running.
