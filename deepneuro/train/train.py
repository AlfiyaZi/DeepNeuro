""" Test Docstring for train!
"""

import math
import os

from functools import partial

from keras.callbacks import ModelCheckpoint, CSVLogger, LearningRateScheduler


def train_model_keras(model, model_filepath, training_generator, n_epochs, steps_per_epoch=10, validation_generator=None, step_per_validation=None, initial_learning_rate=.01, learning_rate_drop=None, epochs_drop=None):
    
    """ A wrapper script for training keras models.
    
        Parameters
        ----------
        model : keras model
            Input keras model object.
        model_filepath : str
            Output filepath to save model.
        training_generator : function
            Generator for streaming training data.
        n_epochs : int
            Number of epochs before model completion.
        steps_per_epoch : int
            Number of steps in each epoch.
        validation_generator : function
            Generator for streaming validation data.
        step_per_validation : int
            Number of steps to yield from validation generator.
        initial_learning_rate : float
            Initial learning rate, if applicable.
        learning_rate_drop : float
            Percentage drop in learning rate every epochs_drop.
        epochs_drop : float
            Learning rate drops by multiplying by learning_rate_drop every epochs_drop.
    """

    model.fit_generator(generator=training_generator, steps_per_epoch=steps_per_epoch, epochs=n_epochs, validation_data=validation_generator, validation_steps=step_per_validation, pickle_safe=True, callbacks=get_keras_callbacks(model_filepath, initial_learning_rate=initial_learning_rate, learning_rate_drop=learning_rate_drop, epochs_drop=epochs_drop))

    model.save(model_filepath)


def get_keras_callbacks(model_file, initial_learning_rate, learning_rate_drop, epochs_drop, logging_dir="."):
    
    """ A wrapper for generating keras callbacks.

        TODO: Specify more callbacks, and optional callbacks.
    
        Parameters
        ----------
        model_file : keras model
            Input keras model object.
        initial_learning_rate : float
            Initial learning rate, if applicable.
        learning_rate_drop : float
            Percentage drop in learning rate every epochs_drop.
        epochs_drop : float
            Learning rate drops by multiplying by learning_rate_drop every epochs_drop.
        logging_dir : str, optional
            The directory where log files are saved.
        
        Returns
        -------
        list
            List of callback objects.
    """

    model_checkpoint = ModelCheckpoint(model_file, monitor="loss", save_best_only=True)
    logger = CSVLogger(os.path.join(logging_dir, "training.log"))
    scheduler = LearningRateScheduler(partial(step_decay, initial_learning_rate=initial_learning_rate, drop=learning_rate_drop, epochs_drop=epochs_drop))
    return [model_checkpoint, logger, scheduler]


def step_decay(epoch, initial_learning_rate, drop, epochs_drop):
    
    """ A simple function to decrease initial_learning_rate by drop every epochs_drop.
        Returns the value of the function at epoch.
    """

    return initial_learning_rate * math.pow(drop, math.floor((1 + epoch) / float(epochs_drop)))
