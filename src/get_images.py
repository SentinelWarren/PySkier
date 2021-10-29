import os, time

class GetImages():
	""" Get different images for the skier depending on his direction.

	Takes images file path.
	"""

	def __init__(self, path):
		self.folder = path
		self.image_order = ["skier_down.png", "skier_right1.png", "skier_right2.png", "skier_left2.png", "skier_left1.png"]
		self.order_map = {}
	
	def load_images(self):
		""" Load image files

		Returns a list of image file names.
		"""

		self.image_names = []
		for filename in os.listdir(self.folder):
			if any([filename.endswith(x) for x in ['.png']]):
				img_name = os.path.join(filename)
				if not filename.startswith(('skier_crash.png', 'skier_flag.png', 'skier_tree.png')):
					self.image_names.append(img_name)

		return self.image_names

	def sort_images(self):
		""" Sort loaded images.

		Returns a list of custom sorted image files.
		"""

		for pos, item in enumerate(self.image_order):
			self.order_map[item] = pos

		#self.sorted_images = self.load_images(), self.sorted_images.sort(key=self.order_map.get)
		self.loaded_images = self.load_images()
		self.sorted_images = sorted(self.loaded_images, key=self.order_map.get)

		return self.sorted_images


if __name__ == "__main__":
		# Get skier_images
		skier_images = GetImages('images/')

		start = time.time()

		print(skier_images.load_images())
		print(skier_images.sort_images())

		end = time.time()
		print(end - start)