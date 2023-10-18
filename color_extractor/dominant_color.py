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
        kmeans = KMeans(n_clusters=4)
        kmeans.fit(image)

        self._dominant_colors = kmeans.cluster_centers_.astype(int)
        self.pixel_labels = kmeans.labels_
        self.dominant_colors = []
        self.forbidden_label = []


        # 마스크 색상(파란색)은 제외
        for i in range(4):
            if not self._dominant_colors[i][2] > 250 and not self._dominant_colors[i][1] < 10:
                self.dominant_colors.append(self._dominant_colors[i])
            else:
                self.forbidden_label.append(i)

        self.dominant_colors = np.array(self.dominant_colors)

    def get_dominant_color(self):
        u, count = np.unique(self.pixel_labels, return_counts=True)
        count = np.delete(count, self.forbidden_label)
        return self.dominant_colors[np.argsort(-count)][0]


if __name__ == '__main__':
    d = DominantColor(cv2.imread("../test/face.png"))
    print(d.get_dominant_color())