#!/usr/bin/env python3

from struct import pack


class Bitmap():
    def __init__(self, width, height):
        self._bfType = 19778 # Bitmap signature
        self._bfReserved1 = 0
        self._bfReserved2 = 0
        self._bcPlanes = 1
        self._bcSize = 12
        self._bcBitCount = 24
        self._bfOffBits = 26
        self._bcWidth = width
        self._bcHeight = height
        self._bfSize = 26+self._bcWidth*3*self._bcHeight
        self.clear()


    def clear(self):
        self._graphics = [(0,0,0)]*self._bcWidth*self._bcHeight


    def setPixel(self, x, y, color):
        if isinstance(color, tuple):
            if x<0 or y<0 or x>self._bcWidth-1 or y>self._bcHeight-1:
                raise ValueError("Coords out of range")
            if len(color) != 3:
                raise ValueError("Color must be a tuple of 3 elems")
            self._graphics[y*self._bcWidth+x] = (color[2], color[1], color[0])
        else:
            raise ValueError("Color must be a tuple of 3 elems")


    def write(self, file):
        with open(file, "wb") as f:
            f.write(pack("<HLHHL",
                        self._bfType,
                        self._bfSize,
                        self._bfReserved1,
                        self._bfReserved2,
                        self._bfOffBits)) # Writing BITMAPFILEHEADER
            f.write(pack("<LHHHH",
                        self._bcSize,
                        self._bcWidth,
                        self._bcHeight,
                        self._bcPlanes,
                        self._bcBitCount)) # Writing BITMAPINFO
            for px in self._graphics:
                f.write(pack("<BBB", *px))
            for i in range((4 - ((self._bcWidth*3) % 4)) % 4):
                f.write(pack("B", 0))


def main():
    size = 520
    b = Bitmap(size, size)
    for j in range(0, size):
        b.setPixel(j, j, (255, 0, 0))
        b.setPixel(j, size-j-1, (255, 0, 0))
        b.setPixel(j, 0, (255, 0, 0))
        b.setPixel(j, size-1, (255, 0, 0))
        b.setPixel(0, j, (255, 0, 0))
        b.setPixel(size-1, j, (255, 0, 0))
    b.write("file.bmp")


if __name__ == "__main__":
    main()
