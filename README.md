# Cervical_cancer_segmentation

project that detect if the provided image contain a cervical cancer or not

# How to use

```bash
python3 -m venv dtron2
source dtron2/bin/activate
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
git clone https://github.com/facebookresearch/detectron2.git
cd detectron2
python setup.py build develop
```

## clone the cervical cancer segmentation repo

```bash
cd cervical_backend
python manage.py runserver
try predict endpoint, it will return json reponse with the original image, predicted image, table contain data about the image, and pic chart information
http://127.0.0.1:8000/predict/

```

## Collaborators

- Juma Rubea
- Meman Awad
- Dama soumana
- Plensia
