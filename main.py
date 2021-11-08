import cv2
from pathlib import Path
import tkinter as tk


class Logic():

    def run(self, imgName):
        global imageName
        imageName = imgName
        img1 = self.create_initial_image()
        img2 = self.detect_edges()
        self.show_results(img1, img2)


    def create_initial_image(self):
        imgI = cv2.imread(imageName)

        return imgI


    def detect_edges(self):
        img = cv2.imread(imageName)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1=30, threshold2=100)

        return edges

    def show_results(self, initImage, edgeImage):
        # Save copy of final image
        res = 'edges_' + imageName
        cv2.imwrite(res, edgeImage)

        # Display the images side by side
        cv2.imshow("Initial", initImage)
        cv2.imshow("Result", edgeImage)


class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):


        self.errorLabel = tk.Label(self, width=30, text="Enter a image name (and extension)")
        self.errorLabel.pack(side=tk.TOP, pady=5)

        frame1 = tk.Frame(self)
        frame1.pack(fill=tk.BOTH, expand=tk.TRUE)


        self.enterButton = tk.Button(frame1, text="Enter", command=self.get_image)
        self.enterButton.pack(side=tk.RIGHT, padx=5)

        self.entryVar = tk.StringVar()
        self.entryVar.set("")
        self.imgEntry = tk.Entry(frame1)
        self.imgEntry["textvariable"] = self.entryVar
        self.imgEntry.bind('<Return>', self.get_image)
        self.imgEntry.pack(fill=tk.BOTH, padx=5, pady=2.5)
        self.imgEntry.focus_set()

        frame2 = tk.Frame(self)
        self.quitButton = tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.pack(pady=5)

    def get_image(self, *args):

        imageName = self.entryVar.get()

        if (self.is_valid(imageName)):
            if (Path(imageName).is_file()):
                self.errorLabel.config(text="Enter a image name (and extension)", fg="black")
                logic = Logic()
                logic.run(imageName)
        else:
            self.errorLabel.config(text="Unable to find image", fg="red")

    def is_valid(self, imageName):
        m = imageName.lower()
        bitmap = m.endswith(('.bmp', '.dib'))  # Bitmaps
        jpeg = m.endswith(('.jpeg', '.jpg', '.jpe', '.jp2'))  # Jpegs
        png = m.endswith(('.png'))  # Portable Newtwork Graphics
        web = m.endswith(('.webp'))  # WebP
        pif = m.endswith(('.pbm', '.pgm', '.ppm', '.pxm', '.pnm'))  # Portable Image FOrmat
        rast = m.endswith(('.sr', '.ras'))  # Sun Rasters
        tif = m.endswith(('.tiff', '.tif'))  # TIFF Files
        exr = m.endswith(('.exr'))  # OpenEXR Image Files
        hdr = m.endswith(('.hdr', '.pic'))  # Radiance HDR

        return bitmap or jpeg or png or web or pif or rast or tif or exr or hdr


app = App()
app.master.title('Edge Finder')
app.mainloop()