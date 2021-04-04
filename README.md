# Guessing-game
A simple alphabet guessing game web application. Using with Flask and MongoDB

Anusid Wachiracharoenwong

## Installation

Use the git the clone the project

```bash
git clone https://github.com/ttxking/guessing-game.git
```

Install docker => https://docs.docker.com/desktop/

Change directory to the project root. For example
```bash
cd C:\Users\foo\Desktop\workspace\guessing-game
```



## Usage

Building the container for this project to run the guessing game
```bash
docker-compose up -d
```

If you want to displays log output
```bash
docker-compose logs -f --tail 10 web
```
Start the game with localhost => http://localhost/

Close the container for this project
```bash
docker-compose down -v