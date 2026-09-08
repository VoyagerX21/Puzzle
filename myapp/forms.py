from django import forms
from django.core.exceptions import ValidationError
from PIL import Image

MAX_FILE_SIZE_MB = 10
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']


class PhotoUploadForm(forms.Form):
    photo = forms.FileField(
        required=True,
        error_messages={
            'required': 'Please select an image file to upload.'
        }
    )

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            raise ValidationError("No image file provided.")

        # Check file size (max 10MB)
        if photo.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValidationError(f"Image file size cannot exceed {MAX_FILE_SIZE_MB}MB.")

        # Validate with Pillow to ensure it's a genuine readable image
        try:
            img = Image.open(photo)
            img.verify()
            # Seek back to start of file for subsequent processing
            photo.seek(0)
        except Exception:
            raise ValidationError("The uploaded file is not a valid image.")

        return photo
