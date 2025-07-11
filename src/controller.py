import glfw
from pyglm import glm

from window import Window
from camera import Camera

class Controller:
    def __init__(self, window: Window, camera: Camera, cameraSpeed = 2.0, mouseSensitivity = 0.06):
        self.cameraSpeed = cameraSpeed
        self.mouseSensitivity = mouseSensitivity
        self.camera = camera
        self.window = window
        
        self.isMousePressed = False
        self.isFocused = False

        glfw.set_mouse_button_callback(self.window.window, self.mouseButtonCallback)
        glfw.set_key_callback(self.window.window, self.keyCallback)
        glfw.set_time(0)

    def mouseButtonCallback(self, window, button, action, modifiers):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            self.isMousePressed = True
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            glfw.set_cursor_pos(self.window.window, 0, 0)
            self.isFocused = True

        elif action == glfw.RELEASE:
            self.isMousePressed = False

    def keyCallback(self, window, key, scanCode, action, modifiers):
        if key == glfw.KEY_ESCAPE and action == glfw.RELEASE:
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            self.isFocused = False

        if key == glfw.KEY_F11 and action == glfw.RELEASE:
            if self.window.isInFullscreen:
                self.window.switchToWindowed()
            else:
                self.window.switchToFullscreen()

    def rotateCamera(self, mouseDelta: glm.vec2):
        self.camera.yaw += mouseDelta.x * self.mouseSensitivity
        self.camera.pitch -= mouseDelta.y * self.mouseSensitivity

        self.camera.pitch = max(-89.0, min(89.0, self.camera.pitch))

        direction = glm.vec3(
            glm.cos(glm.radians(self.camera.yaw)) * glm.cos(glm.radians(self.camera.pitch)),
            glm.sin(glm.radians(self.camera.pitch)),
            glm.sin(glm.radians(self.camera.yaw)) * glm.cos(glm.radians(self.camera.pitch))
        )

        self.camera.forward = glm.normalize(direction)
        self.camera.update()

    def processMovement(self, deltaTime):
        horizontalForward = glm.normalize(glm.vec3(self.camera.forward.x, 0.0, self.camera.forward.z))

        if glfw.get_key(self.window.window, glfw.KEY_W) == glfw.PRESS:
            self.camera.position += horizontalForward * self.cameraSpeed * deltaTime

        if glfw.get_key(self.window.window, glfw.KEY_S) == glfw.PRESS:
            self.camera.position -= horizontalForward * self.cameraSpeed * deltaTime
        
        if glfw.get_key(self.window.window, glfw.KEY_D) == glfw.PRESS:
            self.camera.position += glm.normalize(glm.cross(horizontalForward, self.camera.up)) * self.cameraSpeed * deltaTime

        if glfw.get_key(self.window.window, glfw.KEY_A) == glfw.PRESS:
            self.camera.position -= glm.normalize(glm.cross(horizontalForward, self.camera.up)) * self.cameraSpeed * deltaTime

        if glfw.get_key(self.window.window, glfw.KEY_SPACE) == glfw.PRESS:
            self.camera.position += self.camera.up * self.cameraSpeed * deltaTime

        if glfw.get_key(self.window.window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
            self.camera.position -= self.camera.up * self.cameraSpeed * deltaTime

    def update(self):
        deltaTime = glfw.get_time()
        glfw.set_time(0)

        if self.isFocused:
            mouseDelta = glm.vec2(glfw.get_cursor_pos(self.window.window))
            glfw.set_cursor_pos(self.window.window, 0, 0)

            self.rotateCamera(mouseDelta)
            self.processMovement(deltaTime)

            self.camera.forward