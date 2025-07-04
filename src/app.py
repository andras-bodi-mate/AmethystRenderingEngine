import threading
import glfw

from window import Window
from scene import Scene
from camera import Camera
from material import Material
from gltfLoader import GltfLoader

class App:
    def __init__(self):
        self.window = Window()
        self.camera = Camera(cameraPathMeshPath = "res/models/cameraPath.obj")
        self.gltfLoader = GltfLoader()
        self.scene = self.gltfLoader.loadScene("res/scenes/Sponza/Sponza.gltf")

        self.isRunning = True

    def draw(self):
        Material.updateUniformForAllMaterials("viewTransform", self.camera.viewTransform)
        Material.updateUniformForAllMaterials("perspectiveTransform", self.camera.perspectiveTransform)

        self.scene.render()

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

        glfw.make_context_current(None)
        glfw.set_window_should_close(self.window.window, True)
        print("Window should close soon.")

    def eventLoop(self):
        while not self.window.shouldClose():
            self.window.pollEvents()

    def mainLoop(self):
        self.window.glContext.clear(0.1, 0.1, 0.1)
        self.draw()
        self.window.swapBuffers()
        self.window.pollEvents()

    def start(self):
        glfw.make_context_current(None)

        renderThread = threading.Thread(target = self.renderLoop)
        renderThread.start()

        self.eventLoop()

        self.isRunning = False
        print("Waiting for thread to join...")
        renderThread.join()
        print("Thread successfully joined.")

        print("Terminating GLFW...")
        glfw.terminate()
        print("GLFW terminated.")