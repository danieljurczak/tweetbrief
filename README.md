## Installation
If you are MacOS user mount `/vols/dailybriefs` in your Docker preferences (Docker -> Preferences -> File sharing) and make sure that other users have correct permissions to this directory.

Build docker image and run docker-compose
```bash
docker build -t tweetbrief .
docker-compose up
```

## Configuration
Place your configuration in .env file.
Required:
- TARGET_USERNAME
- BOT_CONSUMER_KEY
- BOT_CONSUMER_SECRET
- BOT_TOKEN_KEY
- BOT_TOKEN_SECRET

Optional:
- BRIEF_PERIOD
- SINGLE_AUTHOR_MAX_TWEETS


## TODO
- tests
- add function to sort via "the number of RTs from the users being followed by the target user"
- improve the visual aspects of pdf