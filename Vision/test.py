import cv2

vidcap = cv2.VideoCapture('test3.mp4')
success,image = vidcap.read()
print("success")
count = 0
while success:
  if count%10 == 0:
      cv2.imwrite("images4/frame%d.jpg" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
  print("success")