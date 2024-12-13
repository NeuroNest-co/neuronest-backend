# Cervical_cancer_segmentation
project that detect if the provided image contain a cervical cancer or not
# How to use<br>
python3 -m venv dtron2<br>
source dtron2/bin/activate<br>
pip install --upgrade pip<br>
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu<br>
git clone https://github.com/facebookresearch/detectron2.git<br>
cd detectron2<br>
python setup.py build develop<br>
## clone the cervical cancer segmentation repo<br>
cd cervical_backend<br>
python manage.py runserver<br>

