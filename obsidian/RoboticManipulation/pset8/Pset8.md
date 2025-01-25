9.1.b) Each mask of the mustard and cheezit will be unique blobs on our mask if the objects are not overlapping in the view of the camera.  Otherwise the objects will appear as one conglomerate.  If we can use DBSCAN to label each mask pixel with being a part of the mustard bottle, the cheezit box, or both, we can then parse the mask, despite an overlap existing, as two separate masks for training.

9.1.c) This depends on the configuration of the setup.  If there exists any overlap between the objects in the view of the camera, there will not be two unique masks.  Only if there is a separation in view of the camera will we be able to reliably mask the two objects.

9.1.d) With the objects touching each other, there exists no camera angle that will produce an image mask with two unique, nonconnected masks.  Our pipeline will fail to produce reliable masks for the obejcts.

9.1.e)
![[Untitled.png]]

![[Untitled 3.png]]

9.2.b) Two cameras are needed in order to find antipodal grasps.  This is because a pinhole camera is incapable of finding two points whose normals are directly opposite each other with the points also being in view from a single pinhole camera.  Like how the sun can only illuminate a subsection of a hemisphere of the earth, approaching an entire hemisphere as the distance of the sun to the earth approaches infinity.

9.2.c) We might select grasps that were not mustard, or select grasps that are between two different objects.

9.2.d) We might select a grasp trajectory that intersects another object that has been clipped from the point cloud.

Scene Segmentation