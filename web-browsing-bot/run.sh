#java -jar target/build/WebBrowsingBot.jar --time 600 --action google_action.json "https://www.google.com/" --headless
#docker run -it --rm --name browsingbot browsing-bot --action "$(cat json_files/outlook_action.json)" --login "$(cat json_files/outlook_login.json)" "https://outlook.live.com/"
# java -jar target/build/WebBrowsingBot.jar --time 600 --login "$(cat json_files/outlook_login.json)" --action "$(cat json_files/outlook_action.json)" "outlook.live.com"
java -jar target/build/WebBrowsingBot.jar --time 600 --login "$(cat json_files/ctfd_login.json)" --action "$(cat json_files/ctfd_action.json)" "localhost:8000" --test admin
