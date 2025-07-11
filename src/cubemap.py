from OpenGL import GL

class Cubemap:
    def __init__(self, glHandle):
        self.glHandle = glHandle

    def use(self, location = 0):
        GL.glBindSampler(location, 0)
        GL.glActiveTexture(GL.GL_TEXTURE0 + location)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, self.glHandle)