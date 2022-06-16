### Initial setup
- Install dependencies: `pip install -r requirements.txt`

### Run the app
- `python3 main.py --directory foldername` or `python3 main.py --directory /absolute/path/to/docs`

Note: The command takes an optional `--number` parameter which serves to get the top n most frequest words sorted from highest to lowest of their occurrences. The default value is 20 which means in the terminal(result) we'll always get a table of top 20 most frequent words. Example usage: `python3 main.py --directory docs --number 10`.

- View the generated `result.html` in the browser.