from tkinter import *
import tkinter as tk
from tkinter import ttk 
from tkinter import filedialog
from tkinter import messagebox

from PIL import ImageTk , Image 

import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import seaborn as sns


from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.models import load_model
from keras.optimizers import Adam



# Veri çerçevesini oluşturun
skin_df = pd.read_csv("HAM10000_metadata.csv")

# Veri çerçevesini kullanarak çubuk grafiği çizin
sns.countplot(x="dx", data=skin_df)
#plt.xlabel("Diagnosis")
#plt.ylabel("Count")
#plt.show()

# Resimleri yükleme ve işleme kodları
data_folder_name = "HAM10000_images_part_1/"
ext = ".jpg"
skin_df["path"] = [data_folder_name + i + ext for i in skin_df["image_id"]]
skin_df["image"] = skin_df["path"].map(lambda x: np.asarray(Image.open(x).resize((100, 75))))
# Görüntüyü uygun boyutta göstermek için
#plt.imshow(skin_df["image"][0])
skin_df["dx_idx"]=pd.Categorical(skin_df["dx"]).codes
skin_df.to_pickle("skin_df.pkl")

skin_df=pd.read_pickle("skin_df.pkl")

#standartzation
x_train=np.asarray(skin_df["image"].tolist())
x_train_mean=np.mean(x_train)
x_train_std=np.std(x_train)
x_train=(x_train-x_train_mean)/x_train_std
#one hot encoding
y_train=to_categorical(skin_df["dx_idx"],num_classes=7)

#Evrişimli sinir ağları (Convolutional neural network) // DEEP LEARNING

input_shape=(75,100,3)
num_classes=7
#model=Sequential()
#tasarım ve dropout ile gelenlerin 1/4 ünü eleme overfittingi önlemek için
#future extaion
#model.add(Conv2D(32,kernel_size=(3,3),activation="relu",padding="Same",input_shape=input_shape))
#model.add(Conv2D(32,kernel_size=(3,3),activation="relu",padding="Same"))
#model.add(MaxPool2D(pool_size=(2,2)))
#model.add(Dropout(0.25))

#model.add(Conv2D(64,kernel_size=(3,3),activation="relu",padding="Same"))
#model.add(Conv2D(64,kernel_size=(3,3),activation="relu",padding="Same"))
#model.add(MaxPool2D(pool_size=(2,2)))
#model.add(Dropout(0.5))

#sınıflandırma flatten

##model.add(Flatten())
#model.add(Dense(128,activation="relu"))
#model.add(Dropout(0.5))
#model.add(Dense(num_classes,activation="softmax")) #class sayısı 2 den fazla ise softmax her classın oranını çıkarır en yüksek çıkan odur.
#model.summary()

#optimizer=Adam(learning_rate=0.0001)
#model.compile(optimizer=optimizer,loss="categorical_crossentropy",metrics=["accuracy"])

#epochs=5#verilerin kaç kere train edileceği
#batch_size=25 #aynı anda kaç tanesinin train edileceği

#history=model.fit(x=x_train,y=y_train,batch_size=batch_size,epochs=epochs,verbose=1,shuffle=True)
#loss  azaldıkça train edilmiş modeller elde edicez accuracy ise başarı oranı düştükçe iyi olcak
#model.save("my_model2.h5")


#load kısmı
model1=load_model("my_model1.h5")
model2=load_model("my_model2.h5")

#prediction kısmı

#index=5
#y_pred=model1.predict(x_train[index].reshape(1,75,100,3))

#y_pred_class=np.argmax(y_pred,axis=1)



#TASARIM KISMI

window = tk.Toplevel()
window.geometry("1080x640")
window.title("Deri Kanseri Tespit ve Sınıflandırma")

#global veriables
img_name=""
count=0
img_jpg=""



# Frames
frame_left = tk.Frame(window, width=540, height=640, borderwidth=2)
frame_left.grid(row=0, column=0)

frame_right = tk.Frame(window, width=540, height=640, borderwidth=2)
frame_right.grid(row=0, column=1)

frame1 = tk.LabelFrame(frame_left, text="Resim", width=540, height=500)
frame1.grid(row=0, column=0)

frame2 = tk.LabelFrame(frame_left, text="Model and Save", width=540, height=140)
frame2.grid(row=1, column=0)

frame3 = tk.LabelFrame(frame_right, text="Bireyin Özellikleri", width=270, height=640)
frame3.grid(row=0, column=0)

frame4 = tk.LabelFrame(frame_right, text="Sonuç", width=270, height=640)
frame4.grid(row=0, column=1, padx=10)



#frame 1


def ImageResize(img):

    basewidth=500
    wpercent=(basewidth/float(img.size[0]))
    hsize=int((float(img.size[1])*float(wpercent)))
    img=img.resize((basewidth,hsize), Image.Resampling.LANCZOS) #resize işlemi yaparken araları doldurmak için kullanılır antıalıas
    return img

def openImage():
    global img_name
    global count
    global img_jpg


    count+=1
    if count!=1 :
        messagebox.showinfo("title",message="Only one image can be opened")
    else:
        img_name = filedialog.askopenfilename(initialdir="C:\\Users\\Poyraz\\Desktop\\Deri Kanseri", title="Select an image file")
        img_jpg= img_name.split("/")[-1].split(".")[0]
        tk.Label(frame1,text=img_jpg,borderwidth=3).pack(pady=10)
        img=Image.open(img_name)
        img=ImageResize(img)

        img=ImageTk.PhotoImage(img)
        panel=tk.Label(frame1,image=img)
        panel.img=img
        panel.pack(padx=15,pady=10)
        #image feature
        data=pd.read_csv("HAM10000_metadata.csv")
        cancer=data[data.image_id==img_jpg]
        for i in range(cancer.size):
            x=0.4
            y=(i/10)/2
            tk.Label(frame3,font=("Times",12),text=str(cancer.iloc[0,i])).place(relx=x,rely=y)





menubar=tk.Menu(window)
window.config(menu=menubar)
file=tk.Menu(menubar)
menubar.add_cascade(label="File",menu=file)
file.add_command(label="Open",command=openImage)


#frame 3 

def classification():
    if img_name != "" and models.get() != "":
        if models.get()=="Model1":
            classification_model=model1
        else:
            classification_model=model2

        z=skin_df[skin_df.image_id==img_jpg]
        z=z.image.values[0].reshape(1,75,100,3)
        z=(z-x_train_mean)/x_train_std
        h=classification_model.predict(z)[0]
        h_index=np.argmax(h)
        predicted_cancer=list(skin_df.dx.unique())[h_index]
        for i in range(len(h)):
            x=0.5
            y=(i/10)/2
            if i !=h_index:
                tk.Label(frame4,text=str(h[i])).place(relx=x,rely=y)
            else:
                tk.Label(frame4,background="green",text=str(h[i])).place(relx=x,rely=y)
        if chvar.get()==1:
            val=entry.get()
            entry.config(state="disabled") #kaydetme tamamlandıktan sonra değişmez hale getir
            path_name=val+".txt"
            save_txt=img_name+"--"+str(predicted_cancer)

            text_file=open(path_name,"w")
            text_file.write(save_txt)
            text_file.close()
        else:
            print("Kaydet tuşunu seçmeniz lazım !")
    else:
        messagebox.showinfo(title="Uyarı",message="Lütfen ilk olarak resim ve model seçiniz !")
        tk.Label(frame3,text="Lütfen ilk olarak resim ve model seçiniz !").place(relx=0.1,rely=0.6)

columns=["lesion_id","image_id","dx","dx_type","age","sex","localization"]

for i in range(len(columns)):
    x=0.1
    y=(i/10)/2

    tk.Label(frame3,font=("Times",12),text=str(columns[i]) + ": ").place(relx=x,rely=y)

classify_button=tk.Button(frame3,background="red",borderwidth=4,font=("Times",13),activebackground="orange",text="Sınıflandır",command=classification)
classify_button.place(relx=0.1,rely=0.5)


#frame 4 

labels=skin_df.dx.unique()

for i in range(len(labels)):
    x=0.1
    y=(i/10)/2

    tk.Label(frame4,font=("Times",12),text=str(labels[i]) + ": ").place(relx=x,rely=y)






#frame 2 

#combo box

#learning rate e göre iki farklı model hazırladık . onun için model seçtiriyoruz.

model_selection_label=tk.Label(frame2,text="Sınıflandırma modelini seç:")
model_selection_label.grid(row=0,column=0,padx=5)

models=tk.StringVar()
model_selection=ttk.Combobox(frame2,textvariable=models,values=("Model1","Model2"),state="readonly")
model_selection.grid(row=0,column=1,padx=5)

#check box

chvar=tk.IntVar()
chvar.set(0)
xbox=tk.Checkbutton(frame2,text="Sınıflandırma sonucunu kaydet",variable=chvar)
xbox.grid(row=1,column=0,pady=5)


#entry

entry=tk.Entry(frame2,width=23)
entry.insert(string="kayıt adı....",index=0)
entry.grid(row=1,column=1)







window.mainloop()
