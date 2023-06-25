install:
	@sudo apt update
	@sudo apt install -y python3-pip python3-tk
	@pip3 install pyro5 pillow emoji

run:
	@gnome-terminal -- bash -c "source venv/Scripts/activate && python3 -m Pyro5.nameserver; exec bash" &
	@gnome-terminal -- bash -c "source venv/Scripts/activate && python3 server.py; exec bash" &
	@gnome-terminal -- bash -c "source venv/Scripts/activate && python3 client.py; exec bash" &

.PHONY: install run

