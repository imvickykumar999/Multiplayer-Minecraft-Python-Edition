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
        self.disabled = False  # Initialize 'disabled' attribute

def send_data(message):
    data = pickle.dumps(message)
    client.send(data)

def receive_data():
    while True:
        try:
            data = client.recv(4096)
            if data:
                received_data = pickle.loads(data)
                
                if received_data['type'] == 'world_state':  # World state
                    # Clear existing voxels
                    for entity in scene.entities:
                        if isinstance(entity, Voxel):
                            destroy(entity)
                    
                    # Create voxels based on received data
                    for voxel_data in received_data['data']:
                        Voxel(position=voxel_data['position'],
                              texture=voxel_data['texture'],
                              default_color=eval(f'color.{voxel_data["color"]}'))
                
                elif received_data['type'] == 'block_update':  # Block placement/removal
                    action = received_data['action']
                    voxel_data = received_data['data']
                    
                    if action == 'add':
                        Voxel(position=voxel_data['position'],
                              texture=voxel_data['texture'],
                              default_color=eval(f'color.{voxel_data["color"]}'))
                    elif action == 'remove':
                        for entity in scene.entities:
                            if isinstance(entity, Voxel) and entity.position == voxel_data['position']:
                                destroy(entity)
                
                elif received_data['type'] == 'player_position':  # Update other players' positions
                    pass  # Handle other players' positions here
                
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
            block_data = {
                'type': 'block_update',
                'action': 'add',
                'data': {
                    'position': hit_info.entity.position + hit_info.normal,
                    'texture': 'brick',
                    'color': 'orange'
                }
            }
            send_data(block_data)
            
    if key == 'right mouse down' and mouse.hovered_entity:
        block_data = {
            'type': 'block_update',
            'action': 'remove',
            'data': {
                'position': mouse.hovered_entity.position
            }
        }
        send_data(block_data)
        destroy(mouse.hovered_entity)

    if key == 'escape':
        exit()

# Set up client socket
PUBLIC_IP = '192.168.0.106'  # Replace with your public IP
CLIENT_PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((PUBLIC_IP, CLIENT_PORT))

player = FirstPersonController(gravity=0.5)

def update():
    if player.y < -5:
        player.y = 50

    # Send player position to server
    player_data = {
        'type': 'player_position',
        'data': {
            'x': player.x,
            'y': player.y,
            'z': player.z
        }
    }
    send_data(player_data)

# Start thread for receiving data
threading.Thread(target=receive_data, daemon=True).start()

Sky()
app.run()
