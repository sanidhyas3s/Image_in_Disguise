from tkinter import font as tkFont
from PIL import Image, ImageTk
from tkinter import filedialog, Tk, Button, Label, messagebox
import cv2
import numpy as np
import math

main=Tk()
main.configure(background='lavender')
main.title('Image in Disguise (Encrypter/Decrypter)')
main.geometry('1485x800')
font_def = tkFont.Font(family='lucida', size=20, weight = 'bold')

def encode_text():
    main.destroy()
    
    global path_image

    space = 15
    image_size = 720, 720

    def on_click():
        global path_image
        path_image = filedialog.askopenfilename()
        load_image = Image.open(path_image)
        load_image.thumbnail(image_size, Image.ANTIALIAS)
        np_load_image = np.asarray(load_image)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img = Label(app, image=render)
        img.image = render
        img.place(x=20, y=50)

    def encrypt_data_into_image():
        global path_image
        data = txt.get(1.0, "end-1c")
        img = cv2.imread(path_image)
        data = [format(ord(i), '08b') for i in data]
        _, width, _ = img.shape
        PixReq = len(data) * 3

        RowReq = PixReq/width
        RowReq = math.ceil(RowReq)

        count = 0
        charCount = 0
        for i in range(RowReq + 1):
            while(count < width and charCount < len(data)):
                char = data[charCount]
                charCount += 1
                for index_k, k in enumerate(char):
                    if((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                        img[i][count][index_k % 3] -= 1
                    if(index_k % 3 == 2):
                        count += 1
                    if(index_k == 7):
                        if(charCount*3 < PixReq and img[i][count][2] % 2 == 1):
                            img[i][count][2] -= 1
                        if(charCount*3 >= PixReq and img[i][count][2] % 2 == 0):
                            img[i][count][2] -= 1
                        count += 1
            count = 0
        path_to_save=filedialog.asksaveasfilename(defaultextension=".png",filetypes=(("png file", ".png"),("jpg file", ".jpg"),("All Files", ".")))
        cv2.imwrite(path_to_save, img)
        success_label = Label(app, text="Encryption Successful!",
                    bg='lavender', font=("Cascadia Code", 20))
        success_label.place(x=image_size[0]+200, y=450)


    app = Tk()
    app.configure(background='lavender')
    app.title("Encrypt Text into Image")
    app.geometry('1485x800')
    on_click_button = Button(app, text="Select Image to hide Text into", bg='white', fg='black', command=on_click)
    on_click_button.place(x=2*space-8, y=10, height = 25)

    txt = Text(app, wrap=WORD, width=75, font=("Cascadia Code", 12))
    txt.place(x=image_size[0]+3*space, y=50, height=300)

    encrypt_button = Button(app, text="Encrypt and Save", bg='white', fg='black', command=encrypt_data_into_image)
    encrypt_button.place(x=image_size[0]+310, y=360)

    text_prompt_label = Label(app, text="Enter Text:",
                bg='lavender', font=("Cascadia Code", 15))
    text_prompt_label.place(x=image_size[0]+3*space, y=12)




def decode_text():
    main.destroy()
    image_size = 500,500

    
    def decrypt():

        path_image = filedialog.askopenfilename()
        load = Image.open(path_image)
        load.thumbnail(image_size, Image.ANTIALIAS)
        load = np.asarray(load)
        load = Image.fromarray(np.uint8(load))
        render = ImageTk.PhotoImage(load)
        img = Label(app, image=render)
        img.image = render
        img.place(x=460, y=50)

        img = cv2.imread(path_image)
        data = []
        stop = False
        for index_i, i in enumerate(img):
            i.tolist()
            for index_j, j in enumerate(i):
                if((index_j) % 3 == 2):
                    # first pixel
                    data.append(bin(j[0])[-1])
                    # second pixel
                    data.append(bin(j[1])[-1])
                    # third pixel
                    if(bin(j[2])[-1] == '1'):
                        stop = True
                        break
                else:
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])
                    data.append(bin(j[2])[-1])
            if(stop):
                break

        message = []
        for i in range(int((len(data)+1)/8)):
            message.append(data[i*8:(i*8+8)])
        message = [chr(int(''.join(i), 2)) for i in message]
        message = ''.join(message)
        message = "Encrypted Text : "+message
        message_label = Label(app, text=message, bg='lavender', font=("Cascadia Code", 20))
        message_label.place(x=710-len(message)*7.9, y=570)

    app = Tk()
    app.configure(background='lavender')
    app.title("Decrypt Text from Image")
    app.geometry('1485x800')
    main_button = Button(app, text="Select Image to retrieve Text", bg='white', fg='black', command=decrypt)
    main_button.place(x=650, y=10)


def encode_image():
    
    main.destroy()
    load_image1 = None
    load_image2 = None
    size = 720, 720
    space = 15
    width = (2*size[0]+3*space)
    dimensions=str(width)+'x800'

    def on_click1():
        global path_image1
        global load_image1
        path_image1 = filedialog.askopenfilename()
        load_image1 = Image.open(path_image1)
        load_image1 = load_image1.resize(size, Image.ANTIALIAS)
        load_image1.thumbnail(size, Image.ANTIALIAS)
        np_load_image = np.asarray(load_image1)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img = Label(app, image=render)
        img.image = render
        img.place(x=space, y=50)

    def on_click2():
        global path_image2
        global load_image2
        path_image2 = filedialog.askopenfilename()
        load_image2 = Image.open(path_image2)
        load_image2 = load_image2.resize(size, Image.ANTIALIAS)
        load_image2.thumbnail(size, Image.ANTIALIAS)
        np_load_image = np.asarray(load_image2)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img = Label(app, image=render)
        img.image = render
        img.place(x=size[0]+2*space, y=50)

    MAXIMUM_COLOUR_VAL = 256
    MAXIMUM_BIT_SIZE = 8
    n_bits = 2

    def create_image(data, resolution):
        image = Image.new("RGB", resolution)
        image.putdata(data)
        return np.array(image)

    def remove_n_lsb(value, n):
        value = value >> n 
        return value << n

    def obtain_n_lsb(value, n):
        value = value << (MAXIMUM_BIT_SIZE - n)
        value = value % MAXIMUM_COLOUR_VAL
        return value >> (MAXIMUM_BIT_SIZE - n)

    def obtain_n_msb(value, n):
        return value >> (MAXIMUM_BIT_SIZE - n)

    def shift_to_8_bits(value, n):
        return value << (MAXIMUM_BIT_SIZE - n)

    def encode(image_to_hide, image_to_hide_in):

        global n_bits
        width, height = image_to_hide.size

        hide_image = image_to_hide.load()
        hide_in_image = image_to_hide_in.load()

        data = []

        for y in range(height):
            for x in range(width):

                r_hide, g_hide, b_hide = hide_image[x,y][0],hide_image[x,y][1],hide_image[x,y][2]

                r_hide = obtain_n_msb(r_hide, n_bits)
                g_hide = obtain_n_msb(g_hide, n_bits)
                b_hide = obtain_n_msb(b_hide, n_bits)

                r_hide_in, g_hide_in, b_hide_in = hide_in_image[x,y][0],hide_in_image[x,y][1],hide_in_image[x,y][2]

                r_hide_in = remove_n_lsb(r_hide_in, n_bits)
                g_hide_in = remove_n_lsb(g_hide_in, n_bits)
                b_hide_in = remove_n_lsb(b_hide_in, n_bits)

                data.append((b_hide + b_hide_in, 
                            g_hide + g_hide_in,
                            r_hide + r_hide_in))

        img = create_image(data, image_to_hide.size)
        path_to_save=filedialog.asksaveasfilename(defaultextension=".png",filetypes=(("png file", ".png"),("jpg file", ".jpg"),("All Files", ".")))
        cv2.imwrite(path_to_save, img)
        success_label = Label(app, text="Encryption Successful!",
                    bg='lavender', font=("Cascadia Code", 20))
        success_label.place(x=(width/2)+200, y=0)

    app = Tk()
    app.configure(background='lavender')
    app.title("Encrypt")
    app.geometry(dimensions)
    on_click_button1 = Button(app, text="Select image to hide", bg='white', fg='black', command=on_click1)
    on_click_button1.place(x=space, y=10)
    on_click_button2 = Button(app, text="Select image to hide in", bg='white', fg='black', command=on_click2)
    on_click_button2.place(x=space+135, y=10)

    encrypt_button = Button(app, text="ENCRYPT", bg='white', fg='black', width=15, command=lambda : encode(load_image1,load_image2))
    encrypt_button.place(x=width-130, y=10)




def decode_image():
    main.destroy()
    load_image1 = None
    size = 720, 720
    space = 15
    width = (2*size[0]+3*space)
    dimensions=str(width)+'x800'

    def on_click1():
        # Step 1.5
        global path_image1
        global load_image1
        path_image1 = filedialog.askopenfilename()
        load_image1 = Image.open(path_image1)
        load_image1.thumbnail(size, Image.ANTIALIAS)
        np_load_image = np.asarray(load_image1)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img = Label(app, image=render)
        img.image = render
        img.place(x=20, y=50)

    def on_click2(path_image2):
        global load_image2
        load_image2 = Image.open(path_image2)
        load_image2 = load_image2.resize(size, Image.ANTIALIAS)
        load_image2.thumbnail(size, Image.ANTIALIAS)
        np_load_image = np.asarray(load_image2)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img = Label(app, image=render)
        img.image = render
        img.place(x=size[0]+2*space, y=50)

    MAXIMUM_COLOUR_VAL = 256
    MAXIMUM_BIT_SIZE = 8
    n_bits = 2

    def create_image(data, resolution):
        image = Image.new("RGB", resolution)
        image.putdata(data)
        return np.array(image)


    def obtain_n_lsb(value, n):
        value = value << (MAXIMUM_BIT_SIZE - n)
        value = value % MAXIMUM_COLOUR_VAL
        return value >> (MAXIMUM_BIT_SIZE - n)

    def shift_to_8_bits(value, n):
        return value << (MAXIMUM_BIT_SIZE - n)

    def decode(enrypted_image):

        global n_bits
        width, height = enrypted_image.size

        image_data = enrypted_image.load()
        '''
        The Encoded image & decoded one (as a result of it) is not carrying as much information as the original files and is somehow compressed
        the reason is the image size defined at the beginning of the code
        '''
        data = []

        for y in range(height):
            for x in range(width):

                r_hiden, g_hiden, b_hiden = image_data[x,y][0],image_data[x,y][1],image_data[x,y][2]

                r_hiden = obtain_n_lsb(r_hiden, n_bits)
                g_hiden = obtain_n_lsb(g_hiden, n_bits)
                b_hiden = obtain_n_lsb(b_hiden, n_bits)

                r_hiden = shift_to_8_bits(r_hiden, n_bits)
                g_hiden = shift_to_8_bits(g_hiden, n_bits)
                b_hiden = shift_to_8_bits(b_hiden, n_bits)

                data.append((b_hiden, 
                            g_hiden,
                            r_hiden))

        img = create_image(data, enrypted_image.size)
        path_to_save=filedialog.asksaveasfilename(defaultextension=".png",filetypes=(("png file", ".png"),("jpg file", ".jpg"),("All Files", ".")))
        cv2.imwrite(path_to_save, img)

        show_label = Label(app, text="Decryption Successful! - Decrypted Image",
                    bg='lavender', font=("Cascadia Code", 20))
        show_label.place(x=(width/2)+430, y=0)
        on_click2(path_to_save)


    app = Tk()
    app.configure(background='lavender')
    app.title("Decrypt")
    app.geometry(dimensions)
    on_click_button1 = Button(app, text="Select Encryted Image", bg='white', fg='black', command=on_click1)
    on_click_button1.place(x=space+5, y=10)

    encrypt_button = Button(app, text="DECRYPT", bg='white', fg='black', command=lambda : decode(load_image1))
    encrypt_button.place(x=space+150, y=10)

head_label = Label(main, text="Image in Disguise - Sorted 100",
            bg='lavender', font=("Segoe UI Semibold", 30))
head_label.place(relx=0.3,rely=0.05)

head_label = Label(main, text='''Important Information:

• Only images encrypted using this application will be decrypted properly

• It is recommended to use same image filetype for encryption

• Only .png and .jpg/.jpeg images are supported

• Encrypted Images are sharable and will hold the encryption unless 
  they are compressed

• Decrypted Image from Image in Image Decryption will not be an 
  exact copy of the original image and will lose some details 
  usually

• An image can posses both hidden Text and Image encryption


Developed by Sanidhya, Sanidhya, Sannidhy, Jatin.
''',
            bg='lavender', font=("lucida", 15),justify='left')
head_label.place(relx=0.48,rely=0.25)

encbuttonTIP=Button(text='Text in Image Encrypter',fg="black",bg="white",width=25,command=encode_text)
encbuttonTIP['font'] =font_def 
encbuttonTIP.place(relx=0.1,rely=0.25)

decbuttonTIP=Button(text='Text in Image Decrypter',fg="black",bg="white",width=25,command=decode_text)
decbuttonTIP['font'] =font_def 
decbuttonTIP.place(relx=0.1,rely=0.39)

encbuttonPIP=Button(text='Image in Image Encrypter',fg="black",bg="white",width=25,command=encode_image)
encbuttonPIP['font'] =font_def 
encbuttonPIP.place(relx=0.1,rely=0.6)

decbuttonPIP=Button(text='Image in Image Decrypter',fg="black",bg="white",width=25,command=decode_text)
decbuttonPIP['font'] =font_def 
decbuttonPIP.place(relx=0.1,rely=0.74)
main.mainloop()