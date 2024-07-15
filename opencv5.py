# 人臉辨識
import cv2

img = cv2.imread("img/Fase.jpg")
img = cv2.resize(img, (0,0), fx=1, fy=1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 眼睛辨識
faceCascade = cv2.CascadeClassifier("eyes_detect.xml")

# 使用灰階圖片效果更佳
# 回傳值紀錄為faceRect
# detectMultiScale變數為:圖片,每次縮小倍率,嚴謹度
faceRect = faceCascade.detectMultiScale(gray, 1.1, 1)
print(len(faceRect))

# facerect會包含一個陣列,內含每個矩形的座標及寬高
for i, (x, y, w, h) in enumerate(faceRect):
    cv2.rectangle(gray, (x,y), (x+w, y+h), (255,0,0), 2)
    
    # 寫文字:圖片,內容,內容左下角座標,字型,大小,顏色,粗度
    cv2.putText(gray, str(i+1), (x-20, y+5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

cv2.imshow("Face.jpg", gray)
cv2.waitKey(0)