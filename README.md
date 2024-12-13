# Cervical_cancer_segmentation
project that detect if the provided image contain a cervical cancer or not
# how to use
python3 -m venv dtron2
source dtron2/bin/activate
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
git clone https://github.com/facebookresearch/detectron2.git
cd detectron2
python setup.py build develop
##clone the cervical cancer segmentation repo
cd cervical_backend
python manage.py runserver

