First there are some dependencies you might need

`pip install bs4 lmxl pandas`

Here `username` is your local OS username
`browserapp` 

Run this (chrome or brave have to be fully closed, otherwise the local database is locked)
`python fetch_history.py {username} {browserapp} && python clean_history.py`


and after that (if you want the fulltext of the urls) run:
` && python posts_only.py`


All together now with params:
`python fetch_history.py markus brave && python clean_history.py && python posts_only.py`

# On NixOS

`niv init`

`nix-shell shell.nix`

`python fetch_history.py markus brave && python clean_history.py && python posts_only.py`
