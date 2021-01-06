First there are some dependencies you might need

`pip install bs4 lmxl pandas`

Here `username` is your local OS username
`browserapp` 

Run this
`python fetch_history.py {username} {browserapp} && python clean_history.py && python posts_only.py`

with params something like:
`python fetch_history.py markus brave && python clean_history.py && python posts_only.py`

