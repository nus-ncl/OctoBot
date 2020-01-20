#java -jar target/build/WebBrowsingBot.jar --time 600 --action google_action.json "https://www.google.com/" --headless
#docker run -itv $(pwd):/utils --rm --name browsingbot browsing-bot --action /utils/google_action.json "https://www.google.com/"
java -jar target/build/WebBrowsingBot.jar --time 600 --login "$(cat json_files/outlook_login.json)" --action "$(cat json_files/outlook_action.json)" "outlook.live.com"
