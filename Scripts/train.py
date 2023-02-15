import os
import sys
import tensorflow as tf
import datetime
from keras import callbacks
tf.debugging.set_log_device_placement(False)
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(1)

sys.path.append('..')
import Modules.model as model
import Modules.generator as gen

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Choix des fonctions de perte
#   0 = Binary Cross Entropy
#   1 = Jacard Coefficient

mode = 1

datasets_dir = "C:/Users/Marc/Desktop"

seed = 24
batch_size = 10

train_img_path = os.path.join(datasets_dir, 'DATASET', 'Train', 'Images')
train_mask_path = os.path.join(datasets_dir, 'DATASET', 'Train', 'Masks')
train_num_images = len(os.listdir(os.path.join(train_img_path, 'img')))
print("Nombre total d'images pour l'entraînement : ", train_num_images)

test_img_path = os.path.join(datasets_dir, 'DATASET', 'Test', 'Images')
test_mask_path = os.path.join(datasets_dir, 'DATASET', 'Test', 'Masks')
test_num_images = len(os.listdir(os.path.join(test_mask_path, 'img')))
print("Nombre total d'images pour les tests : ", test_num_images)

train_img_gen = gen.Generator(
    train_img_path, train_mask_path, batch_size, seed)
val_img_gen = gen.Generator(test_img_path, test_mask_path, batch_size, seed)

steps_per_epoch = train_num_images//batch_size
val_steps_per_epoch = test_num_images//batch_size

x, y = train_img_gen.__next__()

IMG_HEIGHT = x.shape[1]
IMG_WIDTH = x.shape[2]
IMG_CHANNELS = x.shape[3]

print("Taille d'une image : ", IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)

metrics = ['accuracy', 'Precision', 'Recall', model.jacard_coef]

tf.debugging.set_log_device_placement(False)
gpus = tf.config.list_logical_devices('GPU')
strategy = tf.distribute.MirroredStrategy(gpus)
with strategy.scope():
    mymodel = model.simpleUNET(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)
    if mode == 0:
        print("Fonction de perte : Entropie Croisée Binaire")
        # Binary Cross Entropy
        mymodel.compile(optimizer='adam',
                        loss='binary_crossentropy', metrics=metrics)
    elif mode == 1:
        print("Fonction de perte : Score de Jacard")
        # Jacard Coefficient
        mymodel.compile(optimizer='adam', loss=[
                        model.jacard_coef_loss], metrics=metrics)

print("Format des données en entrée : ", mymodel.input_shape)
print("Format des données en sortie : ", mymodel.output_shape)

log_dir = os.path.join(
    os.curdir, "Logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=log_dir, histogram_freq=1, profile_batch=0)

checkpoint_filepath = os.path.join(os.curdir, 'Best_Models')

if mode == 0:
    # Binary Cross Entropy
    earlystopping = callbacks.EarlyStopping(monitor='val_binary_crossentropy',
                                            mode="min", patience=20,
                                            restore_best_weights=True)
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor='val_binary_crossentropy',
        mode='min',
        save_freq=15,
        save_best_only=True
    )

elif mode == 1:
    # Jacard Coefficient
    earlystopping = callbacks.EarlyStopping(monitor='val_jacard_coef',
                                            mode="max", patience=20,
                                            restore_best_weights=True)
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor='val_jacard_coef',
        mode='max',
        save_freq=15,
        save_best_only=True
    )

history = mymodel.fit(train_img_gen,
                      steps_per_epoch=steps_per_epoch,
                      epochs=100,
                      verbose=1,
                      validation_data=val_img_gen,
                      validation_steps=val_steps_per_epoch,
                      callbacks=[tensorboard_callback,
                                 earlystopping, model_checkpoint_callback]
                      )

if mode == 0:
    mymodel.save('ENDOMETRIOSIS_UNET_SEG_BC_FINAL.hdf5')
elif mode == 1:
    mymodel.save('ENDOMETRIOSIS_UNET_SEG_JAC_FINAL.hdf5')
