from time import perf_counter

class Debug:
    startTime = perf_counter()
    
    @staticmethod
    def getElapsedTime():
        return perf_counter() - Debug.startTime