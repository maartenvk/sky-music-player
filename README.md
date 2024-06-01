# Sky music player
For Sky: Children of the Light.  
Music can be downloaded as JSON files from [sky-music github](https://sky-music.github.io/index.html)

# Usage
Play a local file:  
`./main.py play [local music file]`  

Search a local file:  
`./main.py list [search query]`  

Automatically play local files in the `musics/` folder:  
`./main.py auto`  

For additional verbose information on notes being played add `--verbose` flag

# Keybindings
Do you have different key bindings for the notes?  
In the `play_key(key)` function is a `bindings` string with default keybindings which can be modified to accommodate to your needs.
