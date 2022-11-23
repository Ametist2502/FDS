import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
from PIL import Image
from numpy import asarray
import cv2

path = "data"
all_files = glob.glob(path + "/*.csv")

# print(all_files)

li = []

for filename in all_files:
  df = pd.read_csv(filename,index_col=None, header=0)
  li.append(df) #append data into li
#print(li)

df = pd.concat(li,axis=0, ignore_index=True) #combine all data into one df
# print(df)

df['Nganh'] = df['Nganh'].replace(['MyThuat'], 'GD')
df['Nganh'] = df['Nganh'].replace(['mkt'], 'MKT')
df['Nganh'] = df['Nganh'].replace(['se'], 'SE')

df['Nganh'].value_counts()
df['Khoa'].value_counts()
df['Option'].value_counts()

# print(df.describe())
# df.info()
#Display mosquito
plt.figure(figsize=(10,8))
sns.countplot(df['Mosquito'], palette=['#ffb6c1','#ffa07a','#87cefa'])
plt.savefig('Mosquito.jpg') 
#Display bee
plt.figure(figsize=(10,8))
palette = sns.color_palette("Spectral", 10).as_hex()
sns.countplot(df['Bee'], palette= ['#ffb6c1','#ffa07a','#87cefa'])
plt.savefig('Bee.jpg') 
#display department
labels = ['K18', 'K17', 'K15', 'K16']
sizes = df['Khoa'].value_counts()
plt.figure(figsize=(10,8))
colors = ["LIGHTPINK", "LightSalmon","LightSkyBlue", "lightseagreen"] #Since we have 6 subjects
explode = (0.25, 0.25, 0.25, 0.25) #Specifying the exploding position of pie element
plt.pie(sizes,labels=labels,explode=explode,autopct='%1.2f%%', shadow=True, colors=colors)
plt.axis('equal')
plt.legend(title='Index', loc='upper right', bbox_to_anchor=(1,0,0.3,1))
plt.title('Department played game')
plt.savefig('Department.jpg') 
# plt.show()
plt.close
#display major
plt.figure(figsize=(10,8))
y=['SE','MKT','GD','AI','HS','IB']
y.reverse()
x=['34','6','6','4','3','2']
x.reverse()
plt.barh(y, x,color=["LIGHTPINK", "LightSalmon","LightSkyBlue", "lightseagreen"])
plt.ylabel("Major")
plt.xlabel("Count")
plt.title("Major played game")
plt.savefig('Major.jpg') 
# plt.show()
plt.close

 
# Read First Image
img1 = cv2.imread('Bee.jpg',cv2.IMREAD_UNCHANGED)
 
# Read Second Image
img2 = cv2.imread('Department.jpg',cv2.IMREAD_UNCHANGED)
img3 = cv2.imread('Major.jpg')
img4 = cv2.imread('Mosquito.jpg')

# concatenate image Horizontally
Hori1 = np.concatenate((img1, img4), axis=1)
Hori2 = np.concatenate((img3, img2), axis=1)
# concatenate image Vertically
Verti = np.concatenate((Hori1,Hori2), axis=0)
 
# cv2_imshow(Hori1)
# cv2_imshow(Hori2)
cv2.imshow('VERTICAL', Verti)
 
cv2.waitKey(0)
cv2.destroyAllWindows()