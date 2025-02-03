import numpy as np
import cv2

ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

#select the ArUCo tag type and ID
aruco_selection = "DICT_4X4_50"
id = 1 #what you can change ^^

arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_selection])

print("[INFO] generating ArUCo tag...")
print("Aruco Selection '{}' with ID '{}'".format(aruco_selection, id))

tag_size = 1000
tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
tag = cv2.aruco.generateImageMarker(arucoDict, id, tag_size)


#save tag enerated
tag_name = "_" + aruco_selection + "_" + str(id) + ".png"
image_path = r'/Users/brandowitabanjo/Documents/DomerRover/Measure' + tag_name
cv2.imwrite(image_path, tag)
cv2.imshow("ArUCo Tag", tag)

#display the ArUCo tag to our screen
cv2.waitKey(0)
cv2.destroyAllWindows()