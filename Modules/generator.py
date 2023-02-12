from tensorflow.keras.preprocessing.image import ImageDataGenerator

def preprocess_data(img):
    #Scale images
    img = img / 255. #This can be done in ImageDataGenerator but showing it outside as an example
      
    return img

def trainGenerator(train_img_path, train_mask_path, batch_size, seed):
    
    img_data_gen_args = dict(horizontal_flip=True,
                      vertical_flip=True,
                      fill_mode='reflect')
    
    image_datagen = ImageDataGenerator(**img_data_gen_args)
    mask_datagen = ImageDataGenerator(**img_data_gen_args)
    
    image_generator = image_datagen.flow_from_directory(
        directory=train_img_path,
        class_mode = None,
        color_mode = 'rgb',
        target_size=(384, 640),
        batch_size = batch_size,
        seed = seed)
    
    mask_generator = mask_datagen.flow_from_directory(
        directory=train_mask_path,
        class_mode = None,
        color_mode = 'grayscale',
        target_size=(384, 640),
        batch_size = batch_size,
        seed = seed)
    
    train_generator = zip(image_generator, mask_generator)
    
    for (img, mask) in train_generator:
        img = preprocess_data(img)
        yield (img, mask)
        
