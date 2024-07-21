import socket
import threading
import pickle
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

class Voxel(Button):
    def __init__(self, position=(0,0,0), 
                 texture='grass',
                 default_color=color.green):
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture=texture,
            highlight_color=color.red,
            color=default_color,
        )

def update_positions():
    global player
    player_data = {
        'x': player.x,
        'y': player.y,
        'z': player.z
    }
    data = pickle.dumps(player_data)
    client.send(data)

def receive_positions():
    while True:
        try:
            data = client.recv(4096)
            if data:
                player_data = pickle.loads(data)
                # Update other players' positions here
        except:
            break

def input(key):
    global player
    hit_info = raycast(camera.world_position, camera.forward, distance=100)

    if key == 'e' and hit_info.hit:
        player.x = hit_info.entity.position.x
        player.y = hit_info.entity.position.y
        player.z = hit_info.entity.position.z

    if key == 'left mouse down':
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal, 
                  texture='brick',
                  default_color=color.orange,
                )
            
    if key == 'right mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)

    if key == 'escape':
        exit()

# Set up client socket
CLIENT_IP = '127.0.0.1'
CLIENT_PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((CLIENT_IP, CLIENT_PORT))

player = FirstPersonController(gravity=0.5)

def update():
    if player.y < -5:
        player.y = 50

    # Send player position to server
    update_positions()

    # For demonstration, you may want to update other players' positions here

# Start thread for receiving positions
threading.Thread(target=receive_positions, daemon=True).start()

Sky()
app.run()
