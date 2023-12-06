# Verify the Python version
```
python3 --version
```
Python 3.11.5

# Install dependency
pip install flask
pip install googlemaps

# Verify the dependency version installed
pip show flask

# Improve the installation from a requirement file
python install requirement.txt

# Alternative

1. Create the folder to manages the virtual environments

```
mkdir venvs
```

2. Create a virtual environment:

```
python -m venv google-api-venv
```

3. Activate the virtual environment:
    On macOS/Linux:
    ```
    source google-api-venv/bin/activate
    ```

    On Windows:
    ```
    .\google-api-venv\Scripts\activate
    ```

4. Once the virtual environment is activated, you'll see its name in the command prompt or terminal.

5. Install dependencies using the pip command:
```
pip install -r requirements.txt
```


pm2 start api.py --name locations.gomarket.com.uy --interpreter python3