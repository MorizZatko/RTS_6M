"""Blender UDP receiver.

This module receives coordinates from a sender script via a UDP socket.
It opens a Modal Operator to keep blender responsive while listening on the local adress "127.0.0.1" on port 5005.
It decodes the incoming string data and updates the location of the "Cube" object.
"""

import socket
import bpy

class ModalTrackerOperator(bpy.types.Operator):
    """Listens for incoming UDP coordinate data to update object positions in real time."""
    bl_idname = "object.modal_tracker"
    bl_label = "UDP Tracker"
        
    def modal(self, context, event):
        """Handle incoming data and update the cubes location."""
        # Cancel by pressing 'ESC'
        if event.type == 'ESC':
            return self.cancel(context)

        # Cube location loop
        if event.type == 'TIMER':
            try:
                data, adress = self.sock.recvfrom(1024)
                coords = data.decode('utf-8').split(',')
                x, y = float(coords[0]), float(coords[1])
                obj = bpy.data.objects.get("Cube")
                if obj:
                    obj.location.x = x
                    obj.location.y = y
                    pass
            except BlockingIOError:
                pass
            
        return {'PASS_THROUGH'}
    
    def invoke(self, context, event):
        """Initialize the UDP socket, timer, and register the modal handler."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 5005))
        self.sock.setblocking(False)
        
        context.window_manager.event_timer_add(0.01, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def cancel(self, context):
        """Clean up the timer and close the socket."""
        context.window_manager.event_timer_remove(0.01)
        self.sock.close()
        return {'CANCELLED'}
    
bpy.utils.register_class(ModalTrackerOperator)
bpy.ops.object.modal_tracker('INVOKE_DEFAULT')