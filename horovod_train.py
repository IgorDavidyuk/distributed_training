import numpy as np
import tensorflow as tf
import horovod.tensorflow.keras as hvd

# Horovod: initialize Horovod.
hvd.init()
# Prepare data
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.cifar10.load_data()
batch_size = 32
barches_total = (len(train_images) // batch_size + 1) 
# prepare training subset for a particular worker
train_indeces = np.arange(len(train_images))
training_set = np.random.choice(train_indeces, len(train_images)//hvd.size(), replace=False)
train_images, train_labels = train_images[training_set], train_labels[training_set]
# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0


'''dataset = tf.data.Dataset.from_tensor_slices(
    (tf.cast(mnist_images[..., tf.newaxis] / 255.0, tf.float32),
             tf.cast(mnist_labels, tf.int64))
)
dataset = dataset.repeat().shuffle(10000).batch(128)'''

# Prepare model
from model import create_simple_CNN
model = create_simple_CNN()

# Horovod: adjust learning rate based on number of GPUs.
scaled_lr = 1e-4 * hvd.size()
opt = tf.optimizers.Adam(scaled_lr)

# Horovod: add Horovod DistributedOptimizer.
opt = hvd.DistributedOptimizer(opt)

# Horovod: Specify `experimental_run_tf_function=False` to ensure TensorFlow
# uses hvd.DistributedOptimizer() to compute gradients.
model.compile(loss=tf.losses.SparseCategoricalCrossentropy(),
                    optimizer=opt,
                    metrics=['accuracy'],
                    experimental_run_tf_function=False)

callbacks = [
    # Horovod: broadcast initial variable states from rank 0 to all other processes.
    # This is necessary to ensure consistent initialization of all workers when
    # training is started with random weights or restored from a checkpoint.
    hvd.callbacks.BroadcastGlobalVariablesCallback(0),

    # Horovod: average metrics among workers at the end of every epoch.
    #
    # Note: This callback must be in the list before the ReduceLROnPlateau,
    # TensorBoard or other metrics-based callbacks.
    hvd.callbacks.MetricAverageCallback(),

    # Horovod: using `lr = 1.0 * hvd.size()` from the very beginning leads to worse final
    # accuracy. Scale the learning rate `lr = 1.0` ---> `lr = 1.0 * hvd.size()` during
    # the first three epochs. See https://arxiv.org/abs/1706.02677 for details.
    # hvd.callbacks.LearningRateWarmupCallback(warmup_epochs=1, initial_lr=scaled_lr, verbose=1),
]

# Horovod: save checkpoints only on worker 0 to prevent other workers from corrupting them.
# if hvd.rank() == 0:
#     callbacks.append(tf.keras.callbacks.ModelCheckpoint('./checkpoint-{epoch}.h5'))

# Horovod: write logs on worker 0.
verbose = 1 if hvd.rank() == 0 else 0
validation_data = (test_images, test_labels) if hvd.rank() == 0 else None
validation_data = None

# Train the model.
# Horovod: adjust number of steps based on number of GPUs.
# steps_per_epoch=500 // hvd.size(),
model.fit(train_images, train_labels, validation_data=validation_data, epochs=3, batch_size=batch_size, \
        steps_per_epoch=barches_total // hvd.size(), callbacks=callbacks, verbose=verbose)