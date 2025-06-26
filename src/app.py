import threading
import time
import glfw

from window import Window
from scene import Scene
from camera import Camera
from object import SingleObject
from mesh import Mesh
from material import Material

class App:
    def __init__(self):
        self.window = Window()
        self.camera = Camera()
        self.scene = Scene()

        self.scene.addObject(SingleObject(Mesh("res/models/monkey.obj"), Material("shaders/basicVertexShader.glsl", "shaders/basicFragmentShader.glsl")))

        self.isRunning = True

    def draw(self):
        self.scene.updateViewTransformUniforms(self.camera.viewTransform)
        self.scene.updatePerspectiveTransformUniforms(self.camera.perspectiveTransform)
        self.scene.draw()

    def renderLoop(self):
        glfw.make_context_current(self.window.window)

        while self.isRunning and not self.window.shouldClose():
            width, height = glfw.get_framebuffer_size(self.window.window)
            self.window.glContext.viewport = (0, 0, width, height)
            self.camera.updateMatrices(width / height)

            self.window.glContext.clear(0.1, 0.1, 0.1)
            self.draw()
            self.window.swapBuffers()
            #time.sleep(1 / 60.0)

        glfw.set_window_should_close(self.window.window, True)

    def eventLoop(self):
        while not self.window.shouldClose():
            self.window.pollEvents()

    def mainLoop(self):
        self.window.glContext.clear(0.1, 0.1, 0.1)
        self.draw()
        self.window.swapBuffers()
        self.window.pollEvents()

    def start(self):
        #while not self.window.shouldClose():
        #    self.mainLoop()

        glfw.make_context_current(None)

        renderThread = threading.Thread(target = self.renderLoop)
        renderThread.start()

        self.eventLoop()

        self.isRunning = False
        renderThread.join()

        glfw.terminate()