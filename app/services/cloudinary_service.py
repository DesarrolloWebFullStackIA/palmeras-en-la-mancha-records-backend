import cloudinary
import cloudinary.uploader

from fastapi import UploadFile

from app.core.config import settings


class CloudinaryService:
    """Service responsible for uploading images to Cloudinary."""

    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )

    async def upload_image(self, file: UploadFile) -> str:
        """Upload an image to Cloudinary and return its URL."""

        contents = await file.read()

        result = cloudinary.uploader.upload(
            contents,
            folder=settings.CLOUDINARY_FOLDER,
            resource_type="image",
        )

        return result["secure_url"]