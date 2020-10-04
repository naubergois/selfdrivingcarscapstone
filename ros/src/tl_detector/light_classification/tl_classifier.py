from styx_msgs.msg import TrafficLight

import cv2
import numpy as np
import tensorflow as tf
import datetime


import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class TLClassifier(object):
    def __init__(self, is_simulation):

        self.is_simulation=is_simulation

        if is_simulation:
            self.MODEL_NAME = 'light_classification/simulation'
            self.PATH_TO_FROZEN_GRAPH = self.MODEL_NAME + '/frozen_inference_graph.pb'
        else:
            self.MODEL_NAME = 'light_classification/trial'
            self.PATH_TO_FROZEN_GRAPH = self.MODEL_NAME + '/model.pb'





        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_FROZEN_GRAPH, 'rb') as fid:
                ser_graph = fid.read()
                od_graph_def.ParseFromString(ser_graph)
                tf.import_graph_def(od_graph_def, name='')



            self.scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')


        self.session = tf.Session(graph=self.detection_graph)
        self.threshold = 0.5

    def detect_red_and_yellow(self,img, Threshold=0.06):
	    """
	    detect red and yellow
	    :param img:
	    :param Threshold:
	    :return:
	    """

	    desired_dim = (30, 90)  # width, height
	    img = cv2.resize(np.array(img), desired_dim, interpolation=cv2.INTER_LINEAR)
	    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

	    # lower mask (0-10)
	    lower_red = np.array([0, 70, 50])
	    upper_red = np.array([10, 255, 255])
	    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

	    # upper mask (170-180)
	    lower_red1 = np.array([170, 70, 50])
	    upper_red1 = np.array([180, 255, 255])
	    mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)

	    # defining the Range of yellow color
	    lower_yellow = np.array([21, 39, 64])
	    upper_yellow = np.array([40, 255, 255])
	    mask2 = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

	    print(np.count_nonzero(mask0))
	    print(np.count_nonzero(mask1))
	    print(np.count_nonzero(mask2))

	    # red pixels' mask
	    mask = mask0 + mask1 + mask2




	    rospy.loginfo(np.count_nonzero(mask))
	    if np.count_nonzero(mask)> 100:
		          return True
	    else:
		          return False

    def get_classification(self, image):
        """Determines the color of the traffic light in the image
        Args:
            image (cv::Mat): image containing the traffic light
        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)
        """
        print('get classification')

        with self.detection_graph.as_default():
            im_expand = np.expand_dims(image, axis=0)
            class_init_t = datetime.datetime.now()

            (boxes, scores, classes, num_detections) = self.session.run(
                [self.boxes, self.scores, self.classes, self.num_detections],
                feed_dict={self.image_tensor: im_expand})

            # Code for keeping track of the time whenever needed fo debugging
            class_end_t = datetime.datetime.now()
            delta_time = class_end_t - class_init_t

        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)
        max_score=np.argmax(scores)
        print(np.argmax(scores))
        print(scores[max_score])

        if self.is_simulation:
            if scores[0] > self.threshold:
                shape = image.shape
                im_width=shape[0]
                im_height=shape[1]
                rospy.loginfo(shape)
                stop_flag = False
                min_score_thresh=0.5
                for i in range(boxes.shape[0]):
        			if scores[i] > min_score_thresh:
        			    box = boxes[i].tolist()





        		 	    xmin  = box[0]
        			    ymin  = box[1]
        			    xmax  = box[2]
        			    ymax  = box[3]
        			    (left, right, top, bottom) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
        			    a,b,c,d = int(left) , int(right) , int(top) ,int(bottom)
        			    crop_img = image[a:b,c:d]
                if self.detect_red_and_yellow(crop_img):
                            stop_flag = True


                if stop_flag:
                            rospy.loginfo('RED ')
                            rospy.loginfo(TrafficLight.RED)
                            return TrafficLight.RED
                else:

                            return TrafficLight.GREEN

        else:
            rospy.loginfo('site classifier')
            with self.detection_graph.as_default():
                im_expand = np.expand_dims(image, axis=0)
                class_init_t = datetime.datetime.now()

                (boxes, scores, classes, num_detections) = self.session.run(
                    [self.boxes, self.scores, self.classes, self.num_detections],
                    feed_dict={self.image_tensor: im_expand})


                class_end_t = datetime.datetime.now()
                delta_time = class_end_t - class_init_t

                boxes = np.squeeze(boxes)
                scores = np.squeeze(scores)
                classes = np.squeeze(classes).astype(np.int32)
                max_score=np.argmax(scores)

                if scores[0] > 0.9:



                    if classes[0]==3 or classes[0]==2:
                                print('STOP')
                                return TrafficLight.RED
                    else:

                                print('GO')
                                return TrafficLight.GREEN

        return TrafficLight.UNKNOWN
