mkdir -p ~/.streamlit/

#echo "\
#[general]\n\
#email=\"thomasfkns@gmail.com\"\n\
#" > ~/.streamlit/credentials.toml

echo "[server]
headless = true
enableCORS=false
port = $PORT
" > ~/.streamlit/config.toml

