<h1 align=center>
<img src="yogi_web/static/yogi_web/img/logo/logotype.svglogo/logotype.svg" width=50%>
</h1>

[![Build Status](https://travis-ci.com/triat/yogi-bot.svg?branch=master)](https://travis-ci.com/triat/yogi-bot) [![Coverage Status](https://coveralls.io/repos/github/triat/yogi-bot/badge.svg?branch=master)](https://coveralls.io/github/triat/yogi-bot?branch=master)
# Yogi the bot {•̃_•̃}
Yogi the bot is meant to be the tool that allows you to organize your CS:GO tournament in a LAN and kill the myth of not having a CS:GO LAN without issues.

It is based on what was done with https://github.com/deStrO/eBot-CSGO/ but after facing several critical issues with this tool, I decided to redo something similar with the knowledge of what I don't want to see happening during a LAN.

One of the pain points was also the installation of the whole set of tools with communication between the interface and the servers. With Yogi the bot, I want to provide a set of scripts which will help to simplify the installation of the cluster of game servers and also the web interface.

At best, just a list of few settings will need to be provided to set up and start everything.

# Development planning
Basically, in a mid/long term, the goal is to have most of the interesting feature that eBot has.

## Game server
- Read, parse and send the log of the game
- Receive commands from the web interface and apply them to the server
- The capability to load a config file in the game server
- The capability to load a pending game config on any game server
- Export match replay in a storage server at the end of a match

## Web interface
- Manage a cluster of game server
- Manage a set of matches
- Plan a future set of matches
- Retrieve and load configuration on game servers
- Display game information to players and admin

## Communication Schema

```
             +---------+
             |   Web   |
             |interface|
             +---------+
                  ^
                  |
     +------------|------------+
     |            |            |
     v            v            v
+---------+  +---------+  +---------+
| CS SERV |  | CS SERV |  | CS SERV |
+---------+  +---------+  +---------+

```

## Installation
- Script to install the web interface on a specific server
- Script to install one or more game server on a list of servers

# Expected improvement from other tools
- Better and more consistent documentation on how to install and use the bot
- Less fragile to network issues
- Better management of conflict in match scheduling and configuration
- Export data related to the actual match on a backup server for redundancy
- Load pending game configuration on an other server in case of server issue

# Local development
## local CS:GO server
There is a nice docker image done by @Gonzih that you can find [here: docker-csgo-server](https://github.com/Gonzih/docker-csgo-server)

To use it with Yogi, you'll need docker first ([how to install](https://docs.docker.com/install/)), then you need to build an image to have an updated server with the command `docker build -t csgo github.com/Gonzih/docker-csgo-server`

Now you can run the server using the command `docker run --rm --name csgo-server -d -p 27015:27015 -p 27015:27015/udp csgo`

Check that the container is running with the command `docker ps` and you should see something like that:
```
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                                                NAMES
16f506d3f816        csgo   "./csgo.sh /bin/sh -…"   3 seconds ago       Up 1 second         0.0.0.0:27015->27015/tcp, 0.0.0.0:27015->27015/udp   csgo-server
```
To add your own rcon password: `docker exec -t csgo-server bash -c "echo 'rcon_password 1234' >> csgo/csgo/cfg/server.cfg"`
To get the server config you can use the command `docker exec -t csgo-server cat csgo/csgo/cfg/server.cfg`
