import os
import sys

print 'Sizing %s' % sys.argv[1]
GB = 1024 * 1024 * 1024

for root, dirs, files in os.walk(sys.argv[1]):
	# for f in files:
	# 	print os.path.join(root, f)
	for d in dirs:
		currentdir = os.path.join(root, d)
		print currentdirAAAAAAAA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
		# if (os.path.getsize(currentdir) / 1024 / 1024 > 1):
		# 	print '%s, %d' % (os.path.join(root, d), os.path.getsize(os.path.join(root, d)))

	