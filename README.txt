Put the brain_age_classification project in Pycharm.

Step 1. Obtain data

Unzip raw.zip under brain_age_classification/data directory.
So there will be a fold called raw, holding all the raw image data under 'data' directory.

Step 2. Data Preprocessing including skull stripping and registration

Run PreProcess.py

Step 3. Train a 3D CNN model
Run 3dcnn.py

Every epoch of training and validation process will be print in the console.
The final results of test are evaluated by MAE and MSE.

Variables:
# batch_size = 10
# num_classes = 2 
# epochs = 20
# learning_rate = 0.01
# decay = 1e-6
# validation_split = 0.2

