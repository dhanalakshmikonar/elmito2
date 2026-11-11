from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Copy existing local media files to the configured shared S3-compatible storage."

    def handle(self, *args, **options):
        if getattr(settings, "MEDIA_STORAGE", "filesystem") != "s3":
            raise CommandError("Set MEDIA_STORAGE=s3 and configure the bucket before syncing media.")

        media_root = Path(settings.MEDIA_ROOT)
        if not media_root.is_dir():
            raise CommandError(f"Local media directory does not exist: {media_root}")

        files = sorted(path for path in media_root.rglob("*") if path.is_file())
        for index, path in enumerate(files, start=1):
            name = path.relative_to(media_root).as_posix()
            with path.open("rb") as source:
                default_storage.save(name, File(source, name=path.name))
            self.stdout.write(f"Uploaded {name} ({index}/{len(files)})")
        self.stdout.write(self.style.SUCCESS(f"Copied {len(files)} media file(s) to shared storage."))
