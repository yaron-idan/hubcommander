import json
from rtmbot.bin.run_rtmbot import main

# Extract slack token
with open('/secrets/secrets.json') as secret_json:    
    slack_token = json.loads(secret_json.read())['SLACK']
    print(slack_token)

with open('rtmbot.conf',"w+") as rtmbot_conf:
    rtmbot_conf.write("DEBUG: True\n")
    rtmbot_conf.write("SLACK_TOKEN: %s\n" % (slack_token))
    rtmbot_conf.write("ACTIVE_PLUGINS:\n")
    rtmbot_conf.write("    - hubcommander.hubcommander.HubCommander\n")

main()
# Launch it!
# echo "finished creating rtmbot.conf"
# echo PYTHONIOENCODING="UTF-8"
# echo "not activated venv"
# cd /rtmbot
# echo "printing rtmbot.conf"
# cat rtmbot.conf
# echo "printing secrets.json"
# cat secrets.json
# echo "activating rtmbot"
# rtmbot
# echo "activated rtmbot"
