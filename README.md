##Installation
If you are MacOS user mount `/vols/dailybriefs` in your Docker preferences (Docker -> Preferences -> File sharing) and make sure that other users have correct permissions to this directory.

Build docker image and run docker-compose
```bash
docker build -t tweetbrief .
docker-compose up
```

##TODO
- tests
- add function to sort via "the number of RTs from the users being followed by the target user"
- improve the visual aspects of pdf