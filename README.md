### Installation
Install Docker
```
docker build -t hq-hint .
docker run -it hq-hint
```
### Additional setup
Enter your bearer token and user ID in the conn_settings.txt file.
These values can be found by sniffing the traffic on your phone.
The bearer token should be one line, without the word Bearer.
iOS users can find this using Charles' HTTPS proxy feature.

### Usage
```
docker run -it hq-hint
```

### Cron Settings
```
#0 15 * * 1-5 ./go.sh
#0 21 * * * ./go.sh
```

### Firebase
```
Hosting details and UI description coming soon...
```

### Credits
This application merges and improves on work from a few people. Give them a shout for their inspiration.
* [Toby Mellow](https://medium.com/@tobymellor/hq-trivia-using-bots-to-win-money-from-online-game-shows-ce2a1b11828b) 
-> original bot idea
* [Jake Mor](https://medium.com/@jakemor/hquack-my-public-hq-trivia-bot-is-shutting-down-5d9fcdbc9f6e)
    -> first hosted bot using firebase "HQuack" and designed the UI
* [Mike Almond](https://github.com/mikealmond)
    -> original OCR free implementation in PHP
* [Kevin Wu](https://github.com/Exaphis/HackQ-Trivia)
    -> Another OCR free implementation in Python