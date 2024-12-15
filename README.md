# Cervical_cancer_segmentation

project that detect if the provided image contain a cervical cancer or not

# How to use<br>

```bash
python3 -m venv dtron2<br>
source dtron2/bin/activate<br>
pip install --upgrade pip<br>
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu<br>
git clone https://github.com/facebookresearch/detectron2.git<br>
cd detectron2<br>
python setup.py build develop<br>
```

## clone the cervical cancer segmentation repo<br>

```bash
cd cervical_backend<br>
python manage.py runserver<br>
try predict endpoint, it will return json reponse with the original image, predicted image, table contain data about the image, and pic chart information<br>
http://127.0.0.1:8000/predict/
<br>
```

## Collaborators

- Juma Rubea
- Meman Awad
- Dama soumana
- Plensia
