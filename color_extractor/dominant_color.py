# +------------+--------------+-----------------------------------------------------------+
# |   Author   |     Date     |                         Changed                           |
# +------------+--------------+-----------------------------------------------------------+
# |  Andrew A. |  2023/10/18  | Initial release                                           |
# +------------+--------------+-----------------------------------------------------------+
# Reference: https://saturncloud.io/blog/extracting-the-most-dominant-color-from-an-rgb-image-using-opencv-numpy-and-python/

import cv2
import numpy as np
from sklearn.cluster import KMeans


class DominantColor:
    def __init__(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = img.reshape((img.shape[0] * img.shape[1], 3))  # 데이터 flatten

        # k-means 클러스터링 --> 색상 3개
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(image)

        self.dominant_colors = kmeans.cluster_centers_
        self.pixel_labels = kmeans.labels_

        # 마스크 색상(파란색)은 제외
        for i in range(3):
            if self.dominant_colors[i][2] > 250 and self.dominant_colors[i][1] < 10:
                np.delete(self.dominant_colors[i])

    def get_dominant_color(self):
        u, count = np.unique(self.pixel_labels, return_counts=True)
        return self.dominant_colors[np.argsort(-count)][0].astype(int)


if __name__ == '__main__':
    d = DominantColor(cv2.imread("../test/face.png"))
    print(d.get_dominant_color())