# This script does nothing meaningful

It just presses tab and enter on a random website you can specify and does so in different ways depending on which WLAN you are in.

Example crontab file:

```
0 10 * * 1-5 DISPLAY=:0.0 python3 /home/norman/repos/RandomScriptThatMeansNothingAtAll/main.py --username="irgendeinuser" --password='irgendeinpasswort' --home_network_name=HermannSchmitz --abteilung="VDR" --start_url=https://sharepoint.aufgarkeinenfallirgendeinerealeseite.de/sites/zih/Lists/HomeOffice/AllItems.aspx
```
