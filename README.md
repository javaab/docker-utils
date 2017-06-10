# docker-utils
Utility Scripts for running Docker

* [`build-tag-push-dockerfile.py`](https://github.com/JTarball/docker-utils/blob/master/bin/build-tag-push-dockerfile.py) - build & tag docker image based on a Dockerfile project, push to docker hub or push release to github
* [`check-docker-container.sh`](https://github.com/JTarball/docker-utils/blob/master/bin/check-docker-container.sh) - checks status of docker-compose containers or single container id

* [`docker-into-most-recent-container`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-into-most-recent-container) - Attachs to the most recent run container
* [`docker-rm-all`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-rm-all) - Kill and remove all docker images and containers
* [`docker-rm-all-stopped-containers`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-rm-all-stopped-containers) - Remove all stopped docker containers
* [`docker-rm-all-force`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-rm-all-force) - Kill and remove all docker images and containers by force
* [`docker-rm-unnamed-images`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-rm-unnamed-images) - Remove all unnamed images
* [`docker-stop-all`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-stop-all) - Stops all docker processes

# How to Use

Add the following to your bash file (could be different depending on your OS):

```
~/.bash_profile
~/.profile
```

```bash
export PATH="~/<LOCATION>/docker-utils/bin:$PATH"
```

Restart bash / open a new terminal and the utility scripts should be in your path and executable 
