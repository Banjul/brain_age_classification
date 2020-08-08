import os
import sys
from tqdm import tqdm
import copy
from skimage import morphology
import numpy as np
import deepbrain
import nibabel as nib


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR,'data')
DEMO_DIR = os.path.join(ROOT_DIR,'demographic')

# Step 1. Data preprocessing -- skull stripping
def extract_brain(img):
    def remove_small_objects(img):
        binary = copy.copy(img)
        binary[binary > 0] = 1
        labels = morphology.label(binary)
        labels_num = [len(labels[labels == each]) for each in np.unique(labels)]
        rank = np.argsort(np.argsort(labels_num))
        index = list(rank).index(len(rank) - 2)
        new_img = copy.copy(img)
        new_img[labels != index] = 0
        return new_img

    copy_img = copy.copy(img)
    extractor = deepbrain.Extractor()
    prob = extractor.run(copy_img)
    copy_img[prob < 0.5] = 0
    extracted_brain = remove_small_objects(copy_img)
    return extracted_brain
def extract():
    raw_data_dir = os.path.join(DATA_DIR,'raw')
    if not os.path.exists('data/extracted'):
        os.mkdir('data/extracted/')
    extract_data_dir = os.path.join(DATA_DIR,'extracted')
    file_name_list = [each for each in os.listdir(raw_data_dir) if not each.startswith('.')]

    for n, each in tqdm(enumerate(file_name_list, 1)):
        image_path = os.path.join(raw_data_dir,each)
        proxy = nib.load(image_path, keep_file_open=False)
        three_d_data = np.array(proxy.dataobj)
        extracted_brain = extract_brain(three_d_data)
        nib_obj = nib.nifti1.Nifti1Image(extracted_brain, affine=proxy.affine)
        nib_obj.to_filename(os.path.join(extract_data_dir, each))

        # temp = image_path.joinpath('session_1')
        # mri_path = temp.joinpath('mprage_1')
        # for each_image in os.listdir(mri_path):
        #     if not each_image.startswith('.'):
        #         proxy = nib.load(os.path.join(mri_path, each_image), keep_file_open=False)
        #         three_d_data = np.array(proxy.dataobj)
        #         extracted_brain = extract_brain(three_d_data)
        #         nib_obj = nib.nifti1.Nifti1Image(extracted_brain, affine=proxy.affine)
        #         extract_imamge_name = each + '_' + each_image
        #         nib_obj.to_filename(os.path.join(extract_data_dir, extract_imamge_name))

# Step 2. Data preprocessing -- registration
def registration():
    f = open('enviorment.txt', 'r')
    config_file = f.read()
    f.close()

    config_dict = dict()
    for line in config_file.split('\n'):
        try:
            left, right = line.split('=')
            config_dict[left] = right
        except Exception:
            pass
    os.environ.update(config_dict)

    if not os.path.exists('data/registration'):
        os.mkdir('data/registration/')
    if not os.path.exists('data/affine_matrix'):
        os.mkdir('data/affine_matrix/')

    template_file = os.path.join(ROOT_DIR,'MNI152_T1_1mm_brain.nii.gz')
    from_dir = os.path.join(DATA_DIR,'Extracted')
    output_path = os.path.join(DATA_DIR,'registration')
    matrix_path = os.path.join(DATA_DIR,'affine_matrix')

    if len(sys.argv) == 1:
        files = [each for each in os.listdir(from_dir) if not each.startswith('.')]
    else:
        categories = sys.argv[1:]
    for file in tqdm(files):
        full_path = os.path.join(from_dir, file)
        output_file_path = os.path.join(output_path, file)
        matrix_file_path = os.path.join(matrix_path, '.'.join([file.split('.')[0], 'mat']))
        os.system("flirt -ref {} -in {}  -out {} -omat {}".format(template_file, full_path, output_file_path,
                                                                  matrix_file_path))


extract()
registration()
