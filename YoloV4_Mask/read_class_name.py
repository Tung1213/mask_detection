def read_class_names(class_file):
	names={}
	with open(class_file,'r') as data:
		for ID,name in enumerate(data):

			names[ID]=name.strip('\n')
	return names




def count_objects(data, by_class = False, allowed_classes = list(read_class_names(r'./yolov4_data/coco.names').values())):
    boxes, scores, classes, num_objects = data
    print(classes)
    #create dictionary to hold count of objects
    counts = dict()

    # if by_class = True then count objects per class
    if by_class:
        class_names = read_class_names(cfg.YOLO.CLASSES)

        # loop through total number of objects found
        for i in range(num_objects):
            # grab class index and convert into corresponding class name
            class_index = int(classes[i])
            class_name = class_names[class_index]
            if class_name in allowed_classes:
                counts[class_name] = counts.get(class_name, 0) + 1
            else:
                continue

    # else count total objects found
    else:
        counts['total object'] = num_objects
    
    return counts




#print(read_class_names(r'./yolov4_data/coco.names'))

