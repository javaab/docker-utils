# docker-utils
Utility Scripts for Docker

* [`build-tag-push.py`](https://github.com/JTarball/docker-utils/blob/master/bin/build-tag-push.py) - build & tag docker image, push to docker hub or push release to github
* [`check-docker-container.sh`](https://github.com/JTarball/docker-utils/blob/master/bin/check-docker-container.sh) - checks status of docker-compose containers or single container id

# How to Use

Add the following to your bash file:

This could be different depending on your OS:

```
~/.bash_profile       ~/.profile
```

```bash
export PATH="~/<LOCATION>/docker-utils/bin:$PATH"
```

Restart bash / open a new terminal 

The utility scripts should be in your path and executable 
