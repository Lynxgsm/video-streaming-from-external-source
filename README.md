# video-streaming-from-external-source

It' s a simple video streaming from one source to many clients using Python

## How to use

Just install dependencies by running this command:

```bash
pip install opencv-python numpy imutils
```

Now run the streamer first to wait for the server, then run the server to wait for the clients:

```bash
python streamer.py
python server.py
python client.py
```

Of course, you can open many clients at a time
