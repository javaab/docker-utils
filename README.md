# docker-utils
Utility Scripts for Docker

* [`build-tag-push.py`](https://github.com/JTarball/docker-utils/blob/master/bin/build-tag-push.py) - build & tag docker image, push to docker hub or push release to github
* [`check-docker-container.sh`](https://github.com/JTarball/docker-utils/blob/master/bin/check-docker-container.sh) - checks status of docker-compose containers or single container id
* [`docker-stop-all`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-stop-all) - Stops all docker processes
* [`docker-rm-all`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-rm-all) - Kill and remove all docker images and containers
* [`docker-rm-unnamed-images`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-rm-unnamed-images) - Removes un-tagged docker images
* [`docker-into-latest-container`](https://github.com/JTarball/docker-utils/blob/master/bin/docker-into-latest-container) - Attachs to the latest running container


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
